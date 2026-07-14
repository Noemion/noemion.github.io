const numberFromProperty = (styles, name, fallback = 0) => {
  const value = Number.parseFloat(styles.getPropertyValue(name));
  return Number.isFinite(value) ? value : fallback;
};

export const shouldSplitSummaryRail = ({ availableWidth, railWidth, mainMinWidth, gap = 0 }) =>
  availableWidth >= railWidth + mainMinWidth + gap;

export class SummaryRailLayout {
  constructor(root) {
    this.root = root;
    this.frame = 0;
    this.resizeObserver = new ResizeObserver(() => this.schedule());
  }

  connect() {
    this.root.dataset.summaryLayout = "stacked";
    this.resizeObserver.observe(this.root);
    document.fonts?.ready.then(() => this.schedule());
    this.schedule();
    return this;
  }

  schedule() {
    cancelAnimationFrame(this.frame);
    this.frame = requestAnimationFrame(() => this.update());
  }

  update() {
    const styles = getComputedStyle(this.root);
    const split = shouldSplitSummaryRail({
      availableWidth: this.root.clientWidth,
      railWidth: numberFromProperty(styles, "--summary-rail-width", 284),
      mainMinWidth: numberFromProperty(styles, "--summary-main-min-width", 700),
      gap: numberFromProperty(styles, "--summary-layout-gap")
    });
    this.root.dataset.summaryLayout = split ? "split" : "stacked";
  }

  disconnect() {
    cancelAnimationFrame(this.frame);
    this.resizeObserver.disconnect();
  }
}

export const connectSummaryRailLayouts = (scope = document) =>
  [...scope.querySelectorAll("[data-summary-rail-layout]")].map((root) => new SummaryRailLayout(root).connect());
