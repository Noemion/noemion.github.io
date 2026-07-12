(() => {
  "use strict";

  const catalog = document.querySelector("[data-catalog]");
  if (!catalog) return;

  const search = catalog.querySelector("[data-catalog-search]");
  const controls = catalog.querySelector(".catalog-controls");
  const filters = [...catalog.querySelectorAll("[data-catalog-filter]")];
  const groups = [...catalog.querySelectorAll("[data-catalog-group]")];
  const empty = catalog.querySelector("[data-catalog-empty]");
  let activeGroup = "all";

  if (controls) controls.hidden = false;

  const normalize = (value) => value.trim().toLocaleLowerCase("zh-CN");

  const applyFilter = () => {
    const query = normalize(search?.value || "");
    let visibleItems = 0;

    groups.forEach((group) => {
      const groupMatches = activeGroup === "all" || group.dataset.catalogGroup === activeGroup;
      let groupVisibleItems = 0;

      group.querySelectorAll("[data-catalog-item]").forEach((item) => {
        const itemMatches = groupMatches && normalize(item.textContent || "").includes(query);
        item.hidden = !itemMatches;
        if (itemMatches) groupVisibleItems += 1;
      });

      group.hidden = groupVisibleItems === 0;
      visibleItems += groupVisibleItems;
    });

    if (empty) empty.dataset.visible = String(visibleItems === 0);
  };

  filters.forEach((filter) => {
    filter.addEventListener("click", () => {
      activeGroup = filter.dataset.catalogFilter || "all";
      filters.forEach((item) => item.setAttribute("aria-pressed", String(item === filter)));
      applyFilter();
    });
  });

  search?.addEventListener("input", applyFilter);
})();
