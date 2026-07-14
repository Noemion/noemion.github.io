const scriptUrl = new URL(import.meta.url);
const siteRoot = new URL("../", scriptUrl);
const version = scriptUrl.search;
const moduleUrl = (name) => new URL(`modules/${name}.mjs${version}`, scriptUrl);
const dataUrl = new URL(`navigation-data.json${version}`, scriptUrl);
const mobileLayout = matchMedia("(max-width: 999px)");
const desktopLayout = matchMedia("(min-width: 1000px)");
const precisePointer = matchMedia("(hover: hover) and (pointer: fine)");
let keyboardNavigation = false;
document.addEventListener("keydown", (event) => {
  if (event.key === "Tab") keyboardNavigation = true;
}, { capture: true });
document.addEventListener("pointerdown", () => {
  keyboardNavigation = false;
}, { capture: true });

let routeModelPromise;
const loadRouteModel = () => {
  if (!routeModelPromise) {
    routeModelPromise = import(moduleUrl("route-model"))
      .then(({ RouteModel }) => new RouteModel(siteRoot, window.location.href));
  }
  return routeModelPromise;
};

let navigationDataPromise;
const loadStore = () => {
  if (!navigationDataPromise) {
    navigationDataPromise = import(moduleUrl("navigation-store"))
      .then(({ NavigationStore }) => new NavigationStore(dataUrl).load());
  }
  return navigationDataPromise;
};

const globalRoot = document.querySelector("[data-global-nav]");
let globalControllerPromise;
const ensureGlobalNavigation = async (item) => {
  if (!globalRoot || !desktopLayout.matches) return;
  if (!globalControllerPromise) {
    globalControllerPromise = Promise.all([
      import(moduleUrl("global-navigation")),
      loadRouteModel(),
      loadStore()
    ]).then(([{ GlobalNavigation }, routeModel, data]) => {
      const coverUrl = new URL("nav-covers.svg", scriptUrl).href;
      const controller = new GlobalNavigation(globalRoot, routeModel, data.global, coverUrl);
      controller.hydrate();
      return controller;
    });
  }
  try {
    const controller = await globalControllerPromise;
    controller.openByKey(item?.dataset.globalNavItem || "");
  } catch (error) {
    console.warn("Enhanced global navigation is unavailable; primary links remain usable.", error);
  }
};

const requestGlobalNavigation = (event) => {
  const item = event.target.closest?.("[data-global-nav-item]");
  if (item && globalRoot?.contains(item)) ensureGlobalNavigation(item);
};
globalRoot?.addEventListener("pointerover", (event) => {
  if (precisePointer.matches) requestGlobalNavigation(event);
});
globalRoot?.addEventListener("focusin", (event) => {
  if (precisePointer.matches || keyboardNavigation) requestGlobalNavigation(event);
});
globalRoot?.addEventListener("click", (event) => {
  if (!desktopLayout.matches || precisePointer.matches) return;
  const trigger = event.target.closest?.(".global-nav-trigger");
  const item = trigger?.closest("[data-global-nav-item]");
  if (!item || item.classList.contains("is-menu-open")) return;
  event.preventDefault();
  ensureGlobalNavigation(item);
});

const directoryRoot = document.querySelector("[data-directory]");
const directoryPanel = directoryRoot?.closest(".directory-panel");
const mobileHeader = document.querySelector(".global-header");
let mobileHeaderLayoutPromise;
const ensureMobileHeaderLayout = () => {
  if (!mobileHeader) return;
  if (!mobileHeaderLayoutPromise) {
    mobileHeaderLayoutPromise = import(moduleUrl("mobile-header-layout"))
      .then(({ MobileHeaderLayout }) => new MobileHeaderLayout(mobileHeader).connect())
      .catch((error) => console.warn("Responsive header placement is unavailable.", error));
  }
  return mobileHeaderLayoutPromise;
};
let directoryPromise;
const ensureDirectory = async () => {
  if (!directoryRoot) return;
  if (!directoryPromise) {
    directoryPromise = Promise.all([
      import(moduleUrl("directory-navigation")),
      loadRouteModel()
    ]).then(async ([module, routeModel]) => {
      const manual = module.directoryFromDocsRail(document.querySelector("[data-docs-rail]"));
      const moduleKey = manual?.moduleKey || routeModel.moduleKey();
      const directory = manual?.directory || (await loadStore()).modules[moduleKey];
      if (!directory) throw new Error(`No directory model for ${moduleKey}.`);
      new module.DirectoryNavigation(directoryRoot, routeModel, moduleKey, directory).render();
      const mobile = new module.MobileDirectoryController(directoryPanel, directoryRoot);
      mobile.connect();
      directoryPanel.dataset.mobileDirectoryReady = "true";
      const pendingOpen = directoryPanel.hasAttribute("data-mobile-directory-pending-open");
      directoryPanel.removeAttribute("data-mobile-directory-pending-open");
      directoryRoot.removeAttribute("aria-busy");
      if (pendingOpen) mobile.open();
      return mobile;
    });
  }
  try {
    return await directoryPromise;
  } catch (error) {
    console.warn("Enhanced directory navigation is unavailable.", error);
    directoryPanel.dataset.mobileDirectoryReady = "true";
    if (directoryPanel.hasAttribute("data-mobile-directory-pending-open")) {
      directoryPanel.removeAttribute("data-mobile-directory-pending-open");
      directoryRoot.removeAttribute("aria-busy");
      window.noemionMobileDirectoryScroll?.unlock();
      directoryPanel.open = true;
    }
  }
};

if (mobileLayout.matches) ensureDirectory();
if (mobileLayout.matches) ensureMobileHeaderLayout();
mobileLayout.addEventListener("change", (event) => {
  if (event.matches) ensureDirectory();
  if (event.matches) ensureMobileHeaderLayout();
});
directoryPanel?.addEventListener("noemion:directoryrequest", ensureDirectory);
if (directoryPanel?.hasAttribute("data-mobile-directory-pending-open")) ensureDirectory();

const needsTableScroller = Boolean(document.querySelector(".manual-article table"));
const longContent = document.querySelectorAll('body[data-page-role="content"]:not([data-docs-layout="true"]) main > section > h2').length >= 6;
if (needsTableScroller || longContent) {
  import(moduleUrl("content-enhancements"))
    .then(({ enhanceContent }) => enhanceContent())
    .catch((error) => console.warn("Optional content enhancements are unavailable.", error));
}
