(() => {
  "use strict";

  const mobileViewport = window.matchMedia("(max-width: 839px)");
  const pendingPanel = () => document.querySelector(
    ".global-directory-panel[open][data-mobile-directory-pending-open]"
  );

  const containPendingGesture = (event) => {
    if (mobileViewport.matches && pendingPanel()) event.preventDefault();
  };

  document.addEventListener("wheel", containPendingGesture, { passive: false });
  document.addEventListener("touchmove", containPendingGesture, { passive: false });

  document.addEventListener("click", (event) => {
    const summary = event.target.closest?.(".global-directory-panel > summary");
    if (!summary || !mobileViewport.matches) return;
    const panel = summary.parentElement;
    if (!panel || panel.dataset.mobileDirectoryReady === "true") return;

    event.preventDefault();
    const pendingOpen = !panel.hasAttribute("data-mobile-directory-pending-open");
    panel.toggleAttribute("data-mobile-directory-pending-open", pendingOpen);
    panel.open = pendingOpen;
    document.documentElement.classList.toggle("mobile-directory-open", pendingOpen);
    panel.querySelector("[data-directory]")?.toggleAttribute("aria-busy", pendingOpen);
    panel.dispatchEvent(new CustomEvent("noemion:directoryrequest"));
  }, true);
})();
