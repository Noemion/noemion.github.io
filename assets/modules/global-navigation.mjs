const version = new URL(import.meta.url).search;
const { createElement, createLink, createSvgElement } = await import(
  new URL(`dom-factory.mjs${version}`, import.meta.url)
);

export class GlobalNavigation {
  constructor(root, routeModel, groups, coverUrl) {
    this.root = root;
    this.routeModel = routeModel;
    this.groups = groups;
    this.coverUrl = coverUrl;
    this.openTimers = new WeakMap();
    this.closeTimers = new WeakMap();
  }

  hydrate() {
    const groupsByKey = new Map(this.groups.map((group) => [group.key, group]));
    this.root.querySelectorAll("[data-global-nav-item]").forEach((item) => {
      const group = groupsByKey.get(item.dataset.globalNavItem);
      const trigger = item.querySelector(":scope > .global-nav-trigger");
      if (!group || !trigger) return;
      item.append(this.#buildMenu(group));
      this.#connectItem(item, trigger);
    });
  }

  openByKey(key) {
    const item = this.root.querySelector(`[data-global-nav-item="${CSS.escape(key)}"]`);
    if (item) this.#setExpanded(item, true);
  }

  #buildMenu(group) {
    const menu = createElement("div", {
      className: "global-nav-menu",
      attributes: { "aria-label": `${group.label}导航` }
    });
    const intro = createElement("div", { className: "global-nav-menu-intro" });
    intro.append(
      createElement("small", { text: group.kicker }),
      createElement("strong", { text: group.description })
    );
    menu.append(intro);

    group.items.forEach((entry, index) => {
      const link = createLink("global-nav-card", this.routeModel.absolute(entry.href), "");
      link.style.setProperty("--nav-order", index);
      if (this.routeModel.isCurrent(entry.href)) link.setAttribute("aria-current", "page");

      const visual = createElement("span", {
        className: "global-nav-visual",
        attributes: { "data-nav-cover": entry.cover, "aria-hidden": "true" }
      });
      const svg = createSvgElement("svg", { viewBox: "0 0 116 82", focusable: "false" });
      const use = createSvgElement("use", { href: `${this.coverUrl}#nav-cover-${entry.cover}` });
      svg.append(use);
      visual.append(svg, createElement("em", { text: entry.cover_label }));

      const copy = createElement("span", { className: "global-nav-card-copy" });
      copy.append(
        createElement("strong", { text: entry.label }),
        createElement("span", { text: entry.description })
      );

      const arrow = createElement("span", {
        className: "global-nav-card-arrow",
        attributes: { "aria-hidden": "true" }
      });
      const arrowRing = createSvgElement("svg", {
        class: "global-nav-card-arrow-ring",
        viewBox: "0 0 36 36",
        focusable: "false"
      });
      arrowRing.append(
        createSvgElement("circle", {
          class: "global-nav-card-arrow-progress",
          cx: "18",
          cy: "18",
          r: "15",
          pathLength: "100"
        })
      );
      arrow.append(arrowRing, createElement("i", { text: "→" }));
      link.append(visual, copy, arrow);
      menu.append(link);
    });
    return menu;
  }

  #connectItem(item, trigger) {
    item.addEventListener("mouseenter", () => this.#scheduleOpen(item));
    item.addEventListener("mouseleave", () => this.#scheduleClose(item));
    item.addEventListener("focusin", () => this.#setExpanded(item, true));
    item.addEventListener("focusout", () => {
      requestAnimationFrame(() => {
        if (!item.contains(document.activeElement)) this.#setExpanded(item, false);
      });
    });
    trigger.setAttribute("aria-expanded", "false");
  }

  #scheduleOpen(item) {
    clearTimeout(this.closeTimers.get(item));
    clearTimeout(this.openTimers.get(item));
    this.openTimers.set(item, setTimeout(() => this.#setExpanded(item, true), 40));
  }

  #scheduleClose(item) {
    clearTimeout(this.openTimers.get(item));
    clearTimeout(this.closeTimers.get(item));
    this.closeTimers.set(item, setTimeout(() => this.#setExpanded(item, false), 120));
  }

  #setExpanded(item, expanded) {
    if (expanded) {
      this.root.querySelectorAll(".global-nav-item.is-menu-open").forEach((candidate) => {
        if (candidate === item) return;
        candidate.classList.remove("is-menu-open");
        candidate.querySelector(":scope > .global-nav-trigger")?.setAttribute("aria-expanded", "false");
      });
    }
    item.classList.toggle("is-menu-open", expanded);
    item.querySelector(":scope > .global-nav-trigger")?.setAttribute("aria-expanded", String(expanded));
  }
}
