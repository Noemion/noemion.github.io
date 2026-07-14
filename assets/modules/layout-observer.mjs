export const cssNumber = (styles, name, fallback = 0) => {
  const value = Number.parseFloat(styles.getPropertyValue(name));
  return Number.isFinite(value) ? value : fallback;
};

export class LayoutObserver {
  constructor(update, { elements = [], media = [] } = {}) {
    this.update = update;
    this.elements = elements.filter(Boolean);
    this.media = media.filter(Boolean);
    this.frame = 0;
    this.resizeObserver = null;
    this.schedule = this.schedule.bind(this);
  }

  connect() {
    if (typeof ResizeObserver === "function") {
      this.resizeObserver = new ResizeObserver(this.schedule);
      this.elements.forEach((element) => this.resizeObserver.observe(element));
    } else {
      addEventListener("resize", this.schedule, { passive: true });
    }
    this.media.forEach((query) => query.addEventListener("change", this.schedule));
    document.fonts?.ready.then(this.schedule);
    this.schedule();
    return this;
  }

  schedule() {
    if (this.frame) return;
    this.frame = requestAnimationFrame(() => {
      this.frame = 0;
      this.update();
    });
  }

  disconnect() {
    cancelAnimationFrame(this.frame);
    this.frame = 0;
    this.resizeObserver?.disconnect();
    if (!this.resizeObserver) removeEventListener("resize", this.schedule);
    this.media.forEach((query) => query.removeEventListener("change", this.schedule));
  }
}
