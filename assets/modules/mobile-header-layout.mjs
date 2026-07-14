const MOBILE_LAYOUT = "(max-width: 999px)";

const version = new URL(import.meta.url).search;
const { LayoutObserver } = await import(
  new URL(`layout-observer.mjs${version}`, import.meta.url)
);

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
    this.layoutObserver = null;
  }

  connect() {
    if (!this.inner || !this.brand || !this.timeline || !this.directory || !this.summary) return this;
    this.layoutObserver = new LayoutObserver(() => this.update(), {
      elements: [
        this.inner,
        ...this.brand.children,
        this.timeline.firstElementChild || this.timeline,
        this.summary
      ],
      media: [this.media]
    }).connect();
    return this;
  }

  update() {
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

  disconnect() {
    this.layoutObserver?.disconnect();
  }
}
