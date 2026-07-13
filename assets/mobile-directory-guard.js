(() => {
  "use strict";

  const mobileViewport = window.matchMedia("(max-width: 839px)");
  const root = document.documentElement;
  const scrollPositionAttribute = "data-mobile-directory-scroll-y";
  const scrollOffsetProperty = "--mobile-directory-scroll-offset";

  const lockPageScroll = () => {
    if (root.classList.contains("mobile-directory-open")) return;
    const scrollY = window.scrollY || root.scrollTop || 0;
    root.setAttribute(scrollPositionAttribute, String(scrollY));
    root.style.setProperty(scrollOffsetProperty, `${-scrollY}px`);
    root.classList.add("mobile-directory-open");
  };

  const unlockPageScroll = () => {
    if (!root.classList.contains("mobile-directory-open")) return;
    const scrollY = Number(root.getAttribute(scrollPositionAttribute)) || 0;
    root.classList.remove("mobile-directory-open");
    root.style.removeProperty(scrollOffsetProperty);
    root.removeAttribute(scrollPositionAttribute);
    root.scrollTop = scrollY;
    document.body.scrollTop = scrollY;
  };

  window.noemionMobileDirectoryScroll = Object.freeze({
    lock: lockPageScroll,
    unlock: unlockPageScroll
  });

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
    if (pendingOpen) lockPageScroll();
    else unlockPageScroll();
    panel.querySelector("[data-directory]")?.toggleAttribute("aria-busy", pendingOpen);
    panel.dispatchEvent(new CustomEvent("noemion:directoryrequest"));
  }, true);
})();
