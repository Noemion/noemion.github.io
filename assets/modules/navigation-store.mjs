export class NavigationStore {
  #request;

  constructor(dataUrl) {
    this.dataUrl = new URL(dataUrl);
  }

  load() {
    if (!this.#request) this.#request = this.#fetchAndValidate();
    return this.#request;
  }

  async #fetchAndValidate() {
    const response = await fetch(this.dataUrl, { credentials: "same-origin" });
    if (!response.ok) throw new Error(`Navigation data request failed: ${response.status}`);
    const data = await response.json();
    if (!Array.isArray(data.global) || !data.modules || typeof data.modules !== "object") {
      throw new TypeError("Navigation data does not match the required shape.");
    }
    return deepFreeze(data);
  }
}

const deepFreeze = (value) => {
  Object.values(value).forEach((entry) => {
    if (entry && typeof entry === "object" && !Object.isFrozen(entry)) deepFreeze(entry);
  });
  return Object.freeze(value);
};
