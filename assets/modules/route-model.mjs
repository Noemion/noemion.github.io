const DIRECTORY_RULES = Object.freeze([
  [/^endem\//, "endem"],
  [/^docs\//, "docs"],
  [/^(architecture|specifications|spec|components)\//, "architecture"],
  [/^(downloads|faq)\//, "resources"],
  [/^(development|news)\//, "development"]
]);

export const resolveDirectoryModule = (route) => {
  const match = DIRECTORY_RULES.find(([pattern]) => pattern.test(route));
  return match?.[1] || "project";
};

export class RouteModel {
  constructor(siteRoot, currentUrl) {
    this.siteRoot = new URL(siteRoot);
    this.currentUrl = new URL(currentUrl);
  }

  absolute(href) {
    const value = String(href);
    if (value.startsWith(this.siteRoot.pathname)) {
      return new URL(value, this.siteRoot.origin).href;
    }
    return new URL(value.replace(/^\//, ""), this.siteRoot).href;
  }

  canonical(href) {
    const value = new URL(href, this.siteRoot);
    let path = decodeURIComponent(value.pathname);
    if (path.endsWith("/index.html")) path = path.slice(0, -10);
    return `${value.origin}${path.replace(/\/$/, "")}`;
  }

  currentRoute() {
    const rootPath = decodeURIComponent(this.siteRoot.pathname);
    let route = decodeURIComponent(this.currentUrl.pathname);
    if (route.startsWith(rootPath)) route = route.slice(rootPath.length);
    route = route.replace(/^\//, "");
    if (!route || route.endsWith("/")) route += "index.html";
    return route;
  }

  currentCanonical() {
    return this.canonical(this.currentUrl);
  }

  moduleKey() {
    return resolveDirectoryModule(this.currentRoute());
  }

  isCurrent(href) {
    return this.canonical(this.absolute(href)) === this.currentCanonical();
  }
}
