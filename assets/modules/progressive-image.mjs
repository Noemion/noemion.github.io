export class ProgressiveImageStage {
  constructor(stage) {
    this.stage = stage;
    this.image = stage.querySelector("[data-progressive-image-source]");
  }

  connect() {
    if (!this.image) return;

    const reveal = () => {
      if (this.stage.dataset.imageState !== "loading") {
        this.stage.dataset.imageState = "loaded";
        return;
      }
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          this.stage.dataset.imageState = "loaded";
        });
      });
    };

    if (this.image.complete && this.image.naturalWidth > 0) {
      reveal();
      return;
    }

    this.image.addEventListener("load", reveal, { once: true });
    this.image.addEventListener("error", () => {
      this.stage.dataset.imageState = "error";
    }, { once: true });
  }
}

export const connectProgressiveImages = (roots = document.querySelectorAll("[data-progressive-image]")) => {
  Array.from(roots).forEach((root) => {
    root.querySelectorAll("[data-progressive-image-stage]").forEach((stage) => {
      new ProgressiveImageStage(stage).connect();
    });
  });
};
