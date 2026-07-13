(() => {
  "use strict";

  const mobileViewport = window.matchMedia("(max-width: 999px)");
  const root = document.documentElement;
  const scrollPositionAttribute = "data-mobile-directory-scroll-y";
  const scrollOffsetProperty = "--mobile-directory-scroll-offset";
  let touchY = null;

  const shouldContainScrollGesture = (scrollContainer, deltaY) => {
    const maximumScrollTop = Math.max(
      0,
      scrollContainer.scrollHeight - scrollContainer.clientHeight
    );
    if (maximumScrollTop <= 1) return true;
    if (deltaY < 0) return scrollContainer.scrollTop <= 1;
    if (deltaY > 0) return scrollContainer.scrollTop >= maximumScrollTop - 1;
    return false;
  };

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
    const previousScrollBehavior = root.style.scrollBehavior;
    root.style.scrollBehavior = "auto";
    root.classList.remove("mobile-directory-open");
    root.style.removeProperty(scrollOffsetProperty);
    root.removeAttribute(scrollPositionAttribute);
    root.scrollTop = scrollY;
    document.body.scrollTop = scrollY;
    root.style.scrollBehavior = previousScrollBehavior;
  };

  window.noemionMobileDirectoryScroll = Object.freeze({
    lock: lockPageScroll,
    unlock: unlockPageScroll,
    shouldContainScrollGesture
  });

  const openPanel = () => document.querySelector(".global-directory-panel[open]");
  const openScrollContainer = () => openPanel()?.querySelector("[data-directory]");

  const rememberTouch = (event) => {
    if (!mobileViewport.matches || !openPanel()) return;
    const scrollContainer = openScrollContainer();
    if (!scrollContainer?.contains(event.target)) {
      touchY = null;
      return;
    }
    touchY = event.touches[0]?.clientY ?? null;
  };

  const containWheel = (event) => {
    if (!mobileViewport.matches || !openPanel()) return;
    const scrollContainer = openScrollContainer();
    if (
      !scrollContainer?.contains(event.target) ||
      shouldContainScrollGesture(scrollContainer, event.deltaY)
    ) {
      event.preventDefault();
    }
  };

  const containTouch = (event) => {
    if (!mobileViewport.matches || !openPanel()) return;
    const scrollContainer = openScrollContainer();
    const currentY = event.touches[0]?.clientY;
    if (!scrollContainer?.contains(event.target) || currentY === undefined) {
      event.preventDefault();
      touchY = currentY ?? null;
      return;
    }
    if (touchY === null) {
      event.preventDefault();
      touchY = currentY;
      return;
    }
    const deltaY = touchY - currentY;
    touchY = currentY;
    if (shouldContainScrollGesture(scrollContainer, deltaY)) event.preventDefault();
  };

  const forgetTouch = () => {
    touchY = null;
  };

  document.addEventListener("wheel", containWheel, { passive: false });
  document.addEventListener("touchstart", rememberTouch, { passive: true });
  document.addEventListener("touchmove", containTouch, { passive: false });
  document.addEventListener("touchend", forgetTouch, { passive: true });
  document.addEventListener("touchcancel", forgetTouch, { passive: true });

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
