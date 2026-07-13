const version = new URL(import.meta.url).search;
const { createElement, createLink } = await import(
  new URL(`dom-factory.mjs${version}`, import.meta.url)
);

export const shouldContainScrollGesture = (scrollContainer, deltaY) => {
  const maximumScrollTop = Math.max(
    0,
    scrollContainer.scrollHeight - scrollContainer.clientHeight
  );
  if (maximumScrollTop <= 1) return true;
  if (deltaY < 0) return scrollContainer.scrollTop <= 1;
  if (deltaY > 0) return scrollContainer.scrollTop >= maximumScrollTop - 1;
  return false;
};

export const directoryFromDocsRail = (rail) => {
  if (!rail) return null;
  const groups = Array.from(rail.querySelectorAll("[data-directory-group]")).map((group) => ({
    label: group.querySelector("summary strong")?.textContent.trim() || "",
    items: Array.from(group.querySelectorAll(".docs-rail-links a")).map((link) => ({
      href: link.getAttribute("href"),
      label: link.textContent.trim()
    }))
  }));
  return {
    moduleKey: `manual-${rail.dataset.manualId}`,
    directory: {
      kicker: rail.dataset.directoryKicker,
      title: rail.dataset.directoryTitle,
      root: { href: rail.dataset.directoryRoot, label: rail.dataset.directoryTitle },
      parent: {
        href: rail.dataset.directoryParentHref,
        label: rail.dataset.directoryParentLabel
      },
      groups
    }
  };
};

export class DirectoryNavigation {
  constructor(root, routeModel, moduleKey, directory) {
    this.root = root;
    this.routeModel = routeModel;
    this.moduleKey = moduleKey;
    this.directory = directory;
  }

  render() {
    this.root.dataset.directoryModule = this.moduleKey;
    this.root.setAttribute("aria-label", `${this.directory.title}目录`);
    const context = createElement("div", { className: "directory-context" });
    context.append(
      createElement("span", { className: "directory-kicker", text: this.directory.kicker }),
      createLink("directory-title", this.routeModel.absolute(this.directory.root.href), this.directory.title)
    );
    if (this.directory.parent) {
      context.append(createLink(
        "directory-parent",
        this.routeModel.absolute(this.directory.parent.href),
        `← ${this.directory.parent.label}`
      ));
    }

    let activeSection = -1;
    const sections = this.directory.groups.map((group, groupIndex) => {
      const section = createElement("section", { className: "nav-section" });
      const headingId = `directory-${this.moduleKey}-${groupIndex}-heading`;
      const panelId = `directory-${this.moduleKey}-${groupIndex}-panel`;
      const button = createElement("button", {
        className: "nav-section-toggle",
        attributes: { type: "button", id: headingId, "aria-controls": panelId }
      });
      button.append(
        createElement("span", { className: "nav-section-marker", text: String(groupIndex + 1).padStart(2, "0"), attributes: { "aria-hidden": "true" } }),
        createElement("span", { className: "nav-section-label", text: group.label }),
        createElement("span", { className: "nav-section-count", text: group.items.length, attributes: { "aria-label": `${group.items.length} 个入口` } }),
        createElement("span", { className: "nav-section-caret", text: "›", attributes: { "aria-hidden": "true" } })
      );
      const panel = createElement("div", {
        className: "nav-section-panel",
        attributes: { id: panelId, role: "region", "aria-labelledby": headingId }
      });
      const links = createElement("div", { className: "nav-section-links" });
      group.items.forEach((item) => {
        const link = createLink("", this.routeModel.absolute(item.href), item.label);
        if (this.routeModel.isCurrent(item.href)) {
          activeSection = groupIndex;
          link.classList.add("active");
          link.setAttribute("aria-current", "page");
        }
        links.append(link);
      });
      panel.append(links);
      section.append(button, panel);
      return { section, button, panel };
    });

    const setState = (entry, open) => {
      entry.section.classList.toggle("is-open", open);
      entry.button.setAttribute("aria-expanded", String(open));
      entry.panel.setAttribute("aria-hidden", String(!open));
      entry.panel.toggleAttribute("inert", !open);
    };
    const initialSection = activeSection >= 0 ? activeSection : 0;
    sections.forEach((entry, index) => {
      setState(entry, index === initialSection);
      entry.button.addEventListener("click", () => {
        const nextOpen = entry.button.getAttribute("aria-expanded") !== "true";
        sections.forEach((candidate) => setState(candidate, false));
        if (nextOpen) setState(entry, true);
      });
    });
    this.root.replaceChildren(context, ...sections.map((entry) => entry.section));
  }
}

export class MobileDirectoryController {
  constructor(panel, root) {
    this.panel = panel;
    this.root = root;
    this.summary = panel?.querySelector(":scope > summary");
    this.interactive = matchMedia("(max-width: 839px)");
    this.reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
    this.touchY = null;
    this.closeTimer = 0;
  }

  connect() {
    if (!this.panel || !this.summary) return;
    this.summary.addEventListener("click", (event) => this.#toggle(event));
    document.addEventListener("pointerdown", (event) => {
      if (this.interactive.matches && this.panel.open && !this.panel.contains(event.target)) this.close();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && this.interactive.matches && this.panel.open) {
        this.close();
        this.summary.focus();
      }
    });
    document.addEventListener("wheel", (event) => this.#containWheel(event), { passive: false });
    this.root.addEventListener("touchstart", (event) => this.#rememberTouch(event), { passive: true });
    document.addEventListener("touchmove", (event) => this.#containTouch(event), { passive: false });
    document.addEventListener("touchend", () => this.#forgetTouch(), { passive: true });
    document.addEventListener("touchcancel", () => this.#forgetTouch(), { passive: true });
    this.interactive.addEventListener("change", () => this.#syncLock());
    this.#syncLock();
  }

  close() {
    if (!this.panel.open || this.panel.classList.contains("is-closing")) return;
    this.panel.classList.add("is-closing");
    if (this.reducedMotion.matches) return this.#finishClose();
    this.closeTimer = setTimeout(() => this.#finishClose(), 180);
  }

  open() {
    if (!this.interactive.matches || this.panel.open) return;
    clearTimeout(this.closeTimer);
    this.panel.classList.remove("is-closing");
    this.panel.open = true;
    this.#forgetTouch();
    this.#setScrollLock(true);
  }

  #toggle(event) {
    if (!this.interactive.matches) return;
    event.preventDefault();
    if (this.panel.open) return this.close();
    this.open();
  }

  #finishClose() {
    clearTimeout(this.closeTimer);
    this.panel.open = false;
    this.panel.classList.remove("is-closing");
    this.#forgetTouch();
    this.#setScrollLock(false);
  }

  #containWheel(event) {
    if (!this.#isOpenMobileMenu()) return;
    if (!this.root.contains(event.target) || shouldContainScrollGesture(this.root, event.deltaY)) {
      event.preventDefault();
    }
  }

  #rememberTouch(event) {
    if (!this.#isOpenMobileMenu() || !this.root.contains(event.target)) return;
    this.touchY = event.touches[0]?.clientY ?? null;
  }

  #containTouch(event) {
    if (!this.#isOpenMobileMenu()) return;
    const currentY = event.touches[0]?.clientY;
    if (!this.root.contains(event.target)) {
      event.preventDefault();
      this.touchY = currentY ?? null;
      return;
    }
    if (currentY === undefined) {
      event.preventDefault();
      return;
    }
    if (this.touchY === null) {
      this.touchY = currentY;
      return;
    }
    const deltaY = this.touchY - currentY;
    this.touchY = currentY;
    if (shouldContainScrollGesture(this.root, deltaY)) event.preventDefault();
  }

  #forgetTouch() {
    this.touchY = null;
  }

  #isOpenMobileMenu() {
    return this.interactive.matches && this.panel.open;
  }

  #syncLock() {
    this.#setScrollLock(this.panel.open && this.interactive.matches);
  }

  #setScrollLock(locked) {
    const scrollLock = window.noemionMobileDirectoryScroll;
    if (locked) scrollLock?.lock();
    else scrollLock?.unlock();
  }
}
