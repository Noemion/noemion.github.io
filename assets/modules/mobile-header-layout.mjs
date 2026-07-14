const MOBILE_LAYOUT = "(max-width: 999px)";

const numberValue = (value) => Number.parseFloat(value) || 0;

const intrinsicChildrenWidth = (element) => {
  const style = getComputedStyle(element);
  const children = Array.from(element.children);
  const childrenWidth = children.reduce(
    (total, child) => total + Math.max(child.scrollWidth, child.getBoundingClientRect().width),
    0
  );
  const gaps = Math.max(0, children.length - 1) * numberValue(style.columnGap);
  return childrenWidth + gaps
    + numberValue(style.paddingLeft) + numberValue(style.paddingRight)
    + numberValue(style.borderLeftWidth) + numberValue(style.borderRightWidth);
};

export const shouldStackMobileDirectory = ({ availableWidth, brandWidth, timelineWidth, directoryWidth }) => (
  Math.ceil(brandWidth + timelineWidth + directoryWidth) > Math.floor(availableWidth)
);

export class MobileHeaderLayout {
  constructor(header, media = matchMedia(MOBILE_LAYOUT)) {
    this.header = header;
    this.media = media;
    this.inner = header?.querySelector(".global-header-inner");
    this.brand = header?.querySelector(".global-brand");
    this.timeline = header?.querySelector(".global-timeline-link");
    this.directory = header?.querySelector(".global-directory-panel");
    this.summary = this.directory?.querySelector(":scope > summary");
    this.frame = 0;
    this.observer = null;
  }

  connect() {
    if (!this.inner || !this.brand || !this.timeline || !this.directory || !this.summary) return this;
    const schedule = () => this.schedule();
    if (typeof ResizeObserver === "function") {
      this.observer = new ResizeObserver(schedule);
      this.observer.observe(this.inner);
      for (const child of this.brand.children) this.observer.observe(child);
      this.observer.observe(this.timeline.firstElementChild || this.timeline);
      this.observer.observe(this.summary);
    } else {
      addEventListener("resize", schedule, { passive: true });
    }
    this.media.addEventListener("change", schedule);
    document.fonts?.ready.then(schedule);
    this.update();
    return this;
  }

  schedule() {
    if (this.frame) return;
    this.frame = requestAnimationFrame(() => this.update());
  }

  update() {
    this.frame = 0;
    const portal = document.body.dataset.pageRole === "portal";
    const eligible = this.media.matches && !portal;
    const stacked = eligible && shouldStackMobileDirectory({
      availableWidth: this.inner.clientWidth,
      brandWidth: intrinsicChildrenWidth(this.brand),
      timelineWidth: Math.max(this.timeline.scrollWidth, this.timeline.getBoundingClientRect().width),
      directoryWidth: Math.max(this.summary.scrollWidth, this.summary.getBoundingClientRect().width)
    });
    document.body.toggleAttribute("data-mobile-directory-stacked", stacked);
    this.header.dataset.mobileDirectoryPlacement = !this.media.matches
      ? "desktop"
      : (portal ? "portal" : (stacked ? "stacked" : "inline"));
  }
}
