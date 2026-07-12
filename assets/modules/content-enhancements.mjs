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
    label.textContent = "Sections";
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
  const main = document.querySelector('body[data-page-role="content"]:not([data-docs-layout="true"]) main');
  if (main) new PageOutline(main).render();
};
