export class TableScroller {
  static enhance(root = document) {
    root.querySelectorAll(".manual-article table").forEach((table) => {
      if (table.parentElement?.classList.contains("table-wrap")) return;
      const wrapper = document.createElement("div");
      wrapper.className = "table-wrap manual-table-wrap";
      table.before(wrapper);
      wrapper.append(table);
    });
  }
}

export class ScrollFocusRegion {
  static enhance(root = document) {
    const regions = Array.from(root.querySelectorAll(".table-wrap, pre"));
    if (!regions.length) return;

    const contextLabel = (region) => {
      const caption = region.querySelector(":scope > table > caption")?.textContent.trim();
      const heading = region.closest("section")?.querySelector("h2, h3")?.textContent.trim();
      const kind = region.matches("pre") ? "代码" : "表格";
      return `${kind}横向滚动区域${caption || heading ? `：${caption || heading}` : ""}`;
    };

    const update = (region) => {
      const overflows = region.scrollWidth > region.clientWidth + 1;
      if (overflows) {
        if (!region.hasAttribute("tabindex")) {
          region.tabIndex = 0;
          region.dataset.scrollFocusTabindex = "managed";
        }
        if (!region.hasAttribute("role")) {
          region.setAttribute("role", "region");
          region.dataset.scrollFocusRole = "managed";
        }
        if (!region.hasAttribute("aria-label")) {
          region.setAttribute("aria-label", contextLabel(region));
          region.dataset.scrollFocusLabel = "managed";
        }
        return;
      }

      if (region.dataset.scrollFocusTabindex === "managed") {
        region.removeAttribute("tabindex");
        delete region.dataset.scrollFocusTabindex;
      }
      if (region.dataset.scrollFocusRole === "managed") {
        region.removeAttribute("role");
        delete region.dataset.scrollFocusRole;
      }
      if (region.dataset.scrollFocusLabel === "managed") {
        region.removeAttribute("aria-label");
        delete region.dataset.scrollFocusLabel;
      }
    };

    const updateAll = () => regions.forEach(update);
    updateAll();
    window.addEventListener("resize", updateAll, { passive: true });
    document.fonts?.ready.then(updateAll);
    if ("ResizeObserver" in window) {
      const observer = new ResizeObserver(updateAll);
      regions.forEach((region) => observer.observe(region));
    }
  }
}

export class PageOutline {
  constructor(main) {
    this.main = main;
    this.headings = Array.from(main.querySelectorAll(":scope > section > h2"));
  }

  render() {
    if (this.headings.length < 6) return;
    const outline = document.createElement("nav");
    outline.className = "page-outline";
    outline.setAttribute("aria-label", "章节导航");
    const label = document.createElement("strong");
    label.textContent = "章节";
    outline.append(label);
    this.headings.forEach((heading, index) => {
      if (!heading.id) heading.id = `section-${String(index + 1).padStart(2, "0")}`;
      const link = document.createElement("a");
      link.href = `#${heading.id}`;
      link.textContent = heading.textContent.trim();
      outline.append(link);
    });
    this.main.querySelector(":scope > .content-introduction")?.insertAdjacentElement("afterend", outline);
  }
}

export const enhanceContent = () => {
  TableScroller.enhance();
  ScrollFocusRegion.enhance();
  const main = document.querySelector('body[data-page-role="content"]:not([data-docs-layout="true"]) main');
  if (main) new PageOutline(main).render();
};
