const version = new URL(import.meta.url).search;
const { LayoutObserver, cssNumber } = await import(
  new URL(`layout-observer.mjs${version}`, import.meta.url)
);

export const shouldSplitSummaryRail = ({ availableWidth, railWidth, mainMinWidth, gap = 0 }) =>
  availableWidth >= railWidth + mainMinWidth + gap;

export class SummaryRailLayout {
  constructor(root) {
    this.root = root;
    this.layoutObserver = null;
  }

  connect() {
    this.root.dataset.summaryLayout = "stacked";
    this.layoutObserver = new LayoutObserver(() => this.update(), {
      elements: [this.root]
    }).connect();
    return this;
  }

  update() {
    const styles = getComputedStyle(this.root);
    const split = shouldSplitSummaryRail({
      availableWidth: this.root.clientWidth,
      railWidth: cssNumber(styles, "--summary-rail-width", 284),
      mainMinWidth: cssNumber(styles, "--summary-main-min-width", 700),
      gap: cssNumber(styles, "--summary-layout-gap")
    });
    this.root.dataset.summaryLayout = split ? "split" : "stacked";
  }

  disconnect() {
    this.layoutObserver?.disconnect();
  }
}

export const connectSummaryRailLayouts = (scope = document) =>
  [...scope.querySelectorAll("[data-summary-rail-layout]")].map((root) => new SummaryRailLayout(root).connect());
