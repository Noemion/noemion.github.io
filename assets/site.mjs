const scriptUrl = new URL(import.meta.url);
const siteRoot = new URL("../", scriptUrl);
const version = scriptUrl.search;
const moduleUrl = (name) => new URL(`modules/${name}.mjs${version}`, scriptUrl);
const dataUrl = new URL(`navigation-data.json${version}`, scriptUrl);
const coverUrl = new URL("nav-covers.svg", scriptUrl).href;
const { RouteModel } = await import(moduleUrl("route-model"));
const routeModel = new RouteModel(siteRoot, window.location.href);

let storePromise;
const loadStore = async () => {
  if (!storePromise) {
    storePromise = import(moduleUrl("navigation-store"))
      .then(({ NavigationStore }) => new NavigationStore(dataUrl).load());
  }
  return storePromise;
};

const globalRoot = document.querySelector("[data-global-nav]");
let globalControllerPromise;
const ensureGlobalNavigation = async (item) => {
  if (!globalRoot) return;
  if (!globalControllerPromise) {
    globalControllerPromise = Promise.all([
      import(moduleUrl("global-navigation")),
      loadStore()
    ]).then(([{ GlobalNavigation }, data]) => {
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
globalRoot?.addEventListener("pointerover", requestGlobalNavigation, { once: true });
globalRoot?.addEventListener("focusin", requestGlobalNavigation, { once: true });

const directoryRoot = document.querySelector("[data-directory]");
const directoryPanel = directoryRoot?.closest(".directory-panel");
let directoryPromise;
const ensureDirectory = async () => {
  if (!directoryRoot) return;
  if (!directoryPromise) {
    directoryPromise = import(moduleUrl("directory-navigation")).then(async (module) => {
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

const desktopDirectory = matchMedia("(min-width: 1000px)");
if (desktopDirectory.matches) ensureDirectory();
desktopDirectory.addEventListener("change", (event) => {
  if (event.matches) ensureDirectory();
});
directoryPanel?.querySelector(":scope > summary")?.addEventListener("pointerdown", ensureDirectory, { once: true });
directoryPanel?.querySelector(":scope > summary")?.addEventListener("keydown", ensureDirectory, { once: true });
directoryPanel?.addEventListener("noemion:directoryrequest", ensureDirectory);
if (directoryPanel?.hasAttribute("data-mobile-directory-pending-open")) ensureDirectory();

const needsTableScroller = Boolean(document.querySelector(".manual-article table"));
const longContent = document.querySelectorAll('body[data-page-role="content"]:not([data-docs-layout="true"]) main > section > h2').length >= 6;
if (needsTableScroller || longContent) {
  import(moduleUrl("content-enhancements"))
    .then(({ enhanceContent }) => enhanceContent())
    .catch((error) => console.warn("Optional content enhancements are unavailable.", error));
}
