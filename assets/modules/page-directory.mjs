const normalize = (value) => String(value)
  .normalize("NFKC")
  .toLocaleLowerCase("zh-CN")
  .replace(/\s+/g, " ")
  .trim();

export const connectPageDirectory = (root) => {
  const controls = root?.querySelector("[data-page-directory-controls]");
  const query = root?.querySelector("[data-page-directory-query]");
  const groupSelect = root?.querySelector("[data-page-directory-group-select]");
  const count = root?.querySelector("[data-page-directory-count]");
  const empty = root?.querySelector("[data-page-directory-empty]");
  const items = Array.from(root?.querySelectorAll("[data-page-directory-item]") || []);
  if (!controls || !query || !groupSelect || !count || !empty || !items.length) return;

  const groups = new Map();
  items.forEach((item) => {
    const key = item.dataset.routeGroup;
    if (!groups.has(key)) {
      groups.set(key, {
        key,
        label: item.dataset.routeGroupLabel,
        order: Number(item.dataset.routeGroupOrder || 99)
      });
    }
    item.dataset.pageDirectorySearch = normalize(item.textContent);
  });

  Array.from(groups.values())
    .sort((left, right) => left.order - right.order || left.label.localeCompare(right.label, "zh-CN"))
    .forEach((group) => {
      const option = document.createElement("option");
      option.value = group.key;
      option.textContent = group.label;
      groupSelect.append(option);
    });

  const update = () => {
    const terms = normalize(query.value).split(" ").filter(Boolean);
    const activeGroup = groupSelect.value;
    let visible = 0;
    items.forEach((item) => {
      const matchesGroup = activeGroup === "all" || item.dataset.routeGroup === activeGroup;
      const matchesTerms = terms.every((term) => item.dataset.pageDirectorySearch.includes(term));
      const matches = matchesGroup && matchesTerms;
      item.hidden = !matches;
      if (matches) visible += 1;
    });
    count.textContent = String(visible);
    empty.hidden = visible !== 0;
  };

  query.addEventListener("input", update);
  groupSelect.addEventListener("change", update);
  controls.hidden = false;
  groupSelect.hidden = false;
  update();
};
