(() => {
  "use strict";

  const isDirectoryItemActive = (itemHref, target, current) => {
    if (current === target) return true;

    if (/^[^/]+\/index\.html$/.test(itemHref)) {
      return current.startsWith(`${target}/`);
    }
    return false;
  };

  const resolveDirectoryModule = (route) => {
    if (route.startsWith("endem/")) return "endem";
    if (route.startsWith("docs/")) return "docs";
    if (/^(architecture|specifications|components)\//.test(route)) return "architecture";
    if (/^(downloads|faq)\//.test(route)) return "resources";
    if (/^(development|news)\//.test(route)) return "development";
    return "project";
  };

  const createManualDirectory = (payload, route) => {
    const currentPage = payload.pages.find((page) => page.route === route);
    const manual = currentPage && payload.manuals[currentPage.manualId];
    if (!currentPage || !manual) return null;

    const groups = Object.entries(manual.groups)
      .sort(([, left], [, right]) => left.order - right.order)
      .map(([groupKey, group]) => ({
        label: group.label,
        items: payload.pages
          .filter((page) => page.manualId === currentPage.manualId && page.group === groupKey)
          .sort((left, right) => left.order - right.order)
          .map((page) => ({ href: page.route, label: page.label }))
      }))
      .filter((group) => group.items.length > 0);

    return {
      moduleKey: `manual-${currentPage.manualId}`,
      directory: {
        kicker: manual.kicker,
        title: manual.title,
        root: { href: manual.root.replace(/^\//, ""), label: manual.title },
        parent: {
          href: manual.parent_url.replace(/^\//, ""),
          label: manual.parent_label
        },
        groups
      }
    };
  };

  const directoryApi = Object.freeze({
    isDirectoryItemActive,
    resolveDirectoryModule,
    createManualDirectory
  });

  if (
    typeof document === "undefined"
    && typeof module !== "undefined"
    && module.exports
  ) {
    module.exports = directoryApi;
    return;
  }

  document.querySelectorAll(".manual-article table").forEach((table) => {
    if (table.parentElement?.classList.contains("table-wrap")) return;
    const wrapper = document.createElement("div");
    wrapper.className = "table-wrap manual-table-wrap";
    table.before(wrapper);
    wrapper.append(table);
  });

  const contentMain = document.querySelector('body[data-page-role="content"]:not([data-docs-layout="true"]) main');
  const contentHeadings = contentMain
    ? Array.from(contentMain.querySelectorAll(":scope > section > h2"))
    : [];
  if (contentMain && contentHeadings.length >= 6) {
    const outline = document.createElement("nav");
    outline.className = "page-outline";
    outline.setAttribute("aria-label", "章节导航");
    const label = document.createElement("strong");
    label.textContent = "Sections";
    outline.append(label);
    contentHeadings.forEach((heading, index) => {
      if (!heading.id) heading.id = `section-${String(index + 1).padStart(2, "0")}`;
      const link = document.createElement("a");
      link.href = `#${heading.id}`;
      link.textContent = heading.textContent.trim();
      outline.append(link);
    });
    contentMain.querySelector(":scope > .hero")?.insertAdjacentElement("afterend", outline);
  }

  const DIRECTORY_MODULES = Object.freeze({
    project: {
      kicker: "Project",
      title: "项目导航",
      root: { href: "index.html", label: "项目首页" },
      groups: [
        {
          label: "项目",
          items: [
            { href: "index.html", label: "项目首页" },
            { href: "about/index.html", label: "项目背景" },
            { href: "about/background.html", label: "背景与边界" },
            { href: "about/intellectual-foundations.html", label: "思想与方法基础" }
          ]
        },
        {
          label: "架构设计",
          items: [
            { href: "architecture/index.html", label: "架构设计" },
            { href: "specifications/index.html", label: "规范" },
            { href: "components/index.html", label: "组件" }
          ]
        },
        {
          label: "资源",
          items: [
            { href: "endem/index.html", label: "Endem 应用" },
            { href: "docs/index.html", label: "指南与参考" },
            { href: "downloads/index.html", label: "下载与资源" },
            { href: "faq/index.html", label: "常见问题" }
          ]
        },
        {
          label: "开发",
          items: [
            { href: "development/index.html", label: "开发与贡献" },
            { href: "news/index.html", label: "项目动态" }
          ]
        }
      ]
    },
    architecture: {
      kicker: "Architecture",
      title: "架构设计与基础对象",
      root: { href: "architecture/index.html", label: "架构设计首页" },
      parent: { href: "index.html", label: "返回项目首页" },
      groups: [
        {
          label: "架构设计",
          items: [
            { href: "architecture/index.html", label: "架构设计总览" },
            { href: "architecture/endem-lifecycle.html", label: "Endem 生命周期" },
            { href: "architecture/decisions.html", label: "架构决策" },
            { href: "architecture/adr-0008-endem-system.html", label: "ADR-0008 · Endem 体系" },
            { href: "architecture/open-questions.html", label: "开放问题" }
          ]
        },
        {
          label: "对象规范",
          items: [
            { href: "specifications/index.html", label: "规范与成熟度" },
            { href: "specifications/endem.html", label: "Endem" },
            { href: "specifications/weave.html", label: "Weave" },
            { href: "specifications/witness.html", label: "Witness" }
          ]
        },
        {
          label: "系统组件",
          items: [
            { href: "components/index.html", label: "组件总览" },
            { href: "components/core.html", label: "Core" },
            { href: "components/reader.html", label: "Reader" },
            { href: "components/runner.html", label: "Runner" }
          ]
        }
      ]
    },
    docs: {
      kicker: "Guides / Reference",
      title: "指南与参考",
      root: { href: "docs/index.html", label: "指南首页" },
      parent: { href: "index.html", label: "返回项目首页" },
      groups: [
        {
          label: "快速开始",
          items: [
            { href: "docs/index.html", label: "指南首页" },
            { href: "docs/getting-started.html", label: "入门指南" },
            { href: "docs/installation-and-usage.html", label: "获取与使用指南" }
          ]
        },
        {
          label: "专题指南",
          items: [
            { href: "docs/architecture-guide.html", label: "架构设计指南" },
            { href: "docs/development-guide.html", label: "开发指南" }
          ]
        },
        {
          label: "参考指南",
          items: [
            { href: "docs/endem-reference.html", label: "Endem 应用参考" },
            { href: "docs/specifications-reference.html", label: "规范参考指南" }
          ]
        }
      ]
    },
    resources: {
      kicker: "Resources",
      title: "资源与支持",
      root: { href: "downloads/index.html", label: "资源首页" },
      parent: { href: "index.html", label: "返回项目首页" },
      groups: [
        {
          label: "获取资源",
          items: [
            { href: "downloads/index.html", label: "下载与资源" },
            { href: "docs/index.html", label: "指南与参考" }
          ]
        },
        {
          label: "支持",
          items: [
            { href: "faq/index.html", label: "常见问题" },
            { href: "development/index.html", label: "开发与贡献" }
          ]
        }
      ]
    },
    development: {
      kicker: "Development",
      title: "开发与贡献",
      root: { href: "development/index.html", label: "开发与贡献" },
      parent: { href: "index.html", label: "返回项目首页" },
      groups: [
        {
          label: "开发",
          items: [
            { href: "development/index.html", label: "开发概览" },
            { href: "development/current-stage.html", label: "当前项目阶段" },
            { href: "development/implementation-roadmap.html", label: "开发路线图" },
            { href: "development/testing.html", label: "测试与验证" }
          ]
        },
        {
          label: "项目状态",
          items: [
            { href: "news/index.html", label: "项目动态" },
            { href: "architecture/open-questions.html", label: "开放问题" }
          ]
        }
      ]
    },
    endem: {
      kicker: "Application",
      title: "Endem",
      root: { href: "endem/index.html", label: "Endem 应用" },
      parent: { href: "index.html", label: "返回项目首页" },
      groups: [
        {
          label: "应用入口",
          items: [
            { href: "endem/index.html", label: "Endem 应用" },
            { href: "endem/docs/index.html", label: "Endem 使用手册" }
          ]
        },
        {
          label: "形成与绑定",
          items: [
            { href: "endem/docs/format.html", label: "格式与形成" },
            { href: "endem/docs/binding.html", label: "绑定与闭包" }
          ]
        },
        {
          label: "安全与运行",
          items: [
            { href: "endem/docs/safety.html", label: "安全与证据" },
            { href: "endem/docs/running.html", label: "装载与运行" },
            { href: "endem/docs/reference.html", label: "动作与诊断参考" }
          ]
        },
        {
          label: "职责边界",
          items: [
            { href: "components/core.html", label: "Core" },
            { href: "components/reader.html", label: "Reader" },
            { href: "components/runner.html", label: "Runner" }
          ]
        }
      ]
    },
  });

  const GLOBAL_NAV_GROUPS = Object.freeze([
    {
      href: "about/index.html",
      label: "项目",
      kicker: "建立共同语境",
      description: "从项目背景、架构设计和方法边界理解 Noemion 为什么存在。",
      items: [
        { href: "about/background.html", label: "背景与边界", description: "为什么目标语义需要成为工程对象", cover: "background", coverLabel: "EXPRESSION ≠ IDENTITY" },
        { href: "architecture/index.html", label: "架构设计", description: "从编译、链接到可信装载的职责分层", cover: "architecture", coverLabel: "TRUST PIPELINE" },
        { href: "about/intellectual-foundations.html", label: "思想与方法", description: "区分思想启发、工程类比与可验证结论", cover: "foundations", coverLabel: "METHOD / BOUNDARY" },
        { href: "faq/index.html", label: "常见问题", description: "直接回答项目范围、状态与非目标", cover: "faq", coverLabel: "SCOPE CHECK" }
      ]
    },
    {
      href: "specifications/index.html",
      label: "规范",
      kicker: "定义权威边界",
      description: "查看 Endem、组合闭包、范围证据和组件契约。",
      items: [
        { href: "specifications/endem.html", label: "Endem", description: "最小自然语言目标对象与规范字段", cover: "endem-spec", coverLabel: "SAY → DONE" },
        { href: "specifications/weave.html", label: "Weave", description: "已解析、可封装的组合闭包", cover: "weave", coverLabel: "RESOLVED CLOSURE" },
        { href: "specifications/witness.html", label: "Witness", description: "范围声明、来源、完整性与验收证据", cover: "witness", coverLabel: "SCOPED EVIDENCE" },
        { href: "components/index.html", label: "系统组件", description: "Core、Reader 与 Runner 的权限和失败边界", cover: "components", coverLabel: "SYSTEM BOUNDARIES" }
      ]
    },
    {
      href: "endem/index.html",
      label: "Endem",
      kicker: "形成、检查与运行",
      description: "通过一个公开命令面进入确定性对象工程和受限运行。",
      items: [
        { href: "endem/index.html", label: "Endem 应用", description: "查看唯一公开 CLI 与八个动作的边界", cover: "endem", coverLabel: "ONE COMMAND" },
        { href: "endem/docs/format.html", label: "格式与形成", description: "定义规范字段、编码与确定性形成", cover: "format", coverLabel: "FORM / CHECK" },
        { href: "endem/docs/safety.html", label: "安全与证据", description: "检查有界读取、独立观察与签名边界", cover: "see", coverLabel: "CHECK / SEE" },
        { href: "endem/docs/running.html", label: "装载与运行", description: "理解 Frame、能力、观察与验收", cover: "run", coverLabel: "SEAL / RUN" }
      ]
    },
    {
      href: "docs/index.html",
      label: "指南",
      kicker: "选择阅读路径",
      description: "按入门、架构设计、开发、应用和规范主题选择指南或参考资料。",
      items: [
        { href: "docs/getting-started.html", label: "入门指南", description: "从问题背景和核心对象开始", cover: "getting-started", coverLabel: "START PATH" },
        { href: "docs/architecture-guide.html", label: "架构设计指南", description: "理解生命周期、边界与失败路径", cover: "architecture-guide", coverLabel: "BOUNDARY GUIDE" },
        { href: "docs/endem-reference.html", label: "Endem 应用参考", description: "查找 Endem 动作与组件职责", cover: "application-reference", coverLabel: "ACTION MAP" },
        { href: "docs/specifications-reference.html", label: "规范参考指南", description: "查找权威来源、成熟度和 ADR 阅读顺序", cover: "spec-reference", coverLabel: "SPEC AUTHORITY" },
        { href: "endem/docs/index.html", label: "Endem 使用手册", description: "查找格式、绑定、安全、运行和参考主题", cover: "endem-manual", coverLabel: "ENDEM MANUAL" }
      ]
    },
    {
      href: "development/index.html",
      label: "开发",
      kicker: "以证据推进",
      description: "查看当前进展、验证策略、后续规划和可下载资源状态。",
      items: [
        { href: "development/current-stage.html", label: "当前项目阶段", description: "已完成工作、正在推进内容与后续规划", cover: "current-stage", coverLabel: "ACTIVE WORK" },
        { href: "development/implementation-roadmap.html", label: "开发路线图", description: "阶段安排、应用职责与完成标准", cover: "roadmap", coverLabel: "DELIVERY PATH" },
        { href: "development/testing.html", label: "测试与验证", description: "确定性、模糊测试、威胁与一致性验证", cover: "testing", coverLabel: "REJECT MATRIX" },
        { href: "news/index.html", label: "项目动态", description: "只登记可核对的项目进展", cover: "news", coverLabel: "VERIFIED SIGNAL" },
        { href: "downloads/index.html", label: "资源状态", description: "版本、签名和发布资源的真实状态", cover: "downloads", coverLabel: "SIGNED PACKAGE" }
      ]
    }
  ]);

  const script = document.currentScript;
  if (!script) return;

  const siteRoot = new URL("../", script.src);
  const nav = document.querySelector("[data-directory]");
  if (!nav) return;

  const canonical = (url) => {
    const value = new URL(url, siteRoot);
    let path = decodeURIComponent(value.pathname);
    if (path.endsWith("/index.html")) path = path.slice(0, -10);
    return `${value.origin}${path.replace(/\/$/, "")}`;
  };

  const currentRoute = (() => {
    const page = new URL(window.location.href);
    const rootPath = decodeURIComponent(siteRoot.pathname);
    let route = decodeURIComponent(page.pathname);
    if (route.startsWith(rootPath)) route = route.slice(rootPath.length);
    route = route.replace(/^\//, "");
    if (!route || route.endsWith("/")) route += "index.html";
    return route;
  })();

  const readManualDirectory = () => {
    const source = document.querySelector("[data-manual-directory-source]");
    if (!source) return null;

    try {
      const payload = JSON.parse(source.textContent);
      return createManualDirectory(payload, currentRoute);
    } catch (error) {
      console.warn("Manual directory data could not be read.", error);
      return null;
    }
  };

  const manualDirectory = readManualDirectory();
  const moduleKey = manualDirectory?.moduleKey || resolveDirectoryModule(currentRoute);
  const directory = manualDirectory?.directory || DIRECTORY_MODULES[moduleKey];
  const current = canonical(window.location.href);

  const globalNav = document.querySelector("[data-global-nav]");
  if (globalNav) {
    const globalItems = GLOBAL_NAV_GROUPS.map((group) => {
      const item = document.createElement("div");
      item.className = "global-nav-item";

      const trigger = document.createElement("a");
      trigger.className = "global-nav-trigger";
      trigger.href = new URL(group.href, siteRoot).href;
      trigger.innerHTML = `<span>${group.label}</span><span class="global-nav-caret" aria-hidden="true">⌄</span>`;
      trigger.setAttribute("aria-haspopup", "true");
      trigger.setAttribute("aria-expanded", "false");

      const menu = document.createElement("div");
      menu.className = "global-nav-menu";
      menu.setAttribute("aria-label", `${group.label}导航`);

      const intro = document.createElement("div");
      intro.className = "global-nav-menu-intro";
      intro.innerHTML = `<small>${group.kicker}</small><strong>${group.description}</strong>`;
      menu.append(intro);

      group.items.forEach((entry, entryIndex) => {
        const link = document.createElement("a");
        link.className = "global-nav-card";
        link.href = new URL(entry.href, siteRoot).href;
        link.style.setProperty("--nav-order", entryIndex);
        const coverHref = new URL(`assets/nav-covers.svg#nav-cover-${entry.cover}`, siteRoot).href;
        link.innerHTML = `<span class="global-nav-visual" data-nav-cover="${entry.cover}" aria-hidden="true"><svg viewBox="0 0 116 82" focusable="false"><use href="${coverHref}"></use></svg><em>${entry.coverLabel}</em></span><span class="global-nav-card-copy"><strong>${entry.label}</strong><span>${entry.description}</span></span><i aria-hidden="true">↗</i>`;
        if (canonical(link.href) === current) link.setAttribute("aria-current", "page");
        menu.append(link);
      });

      let openTimer = 0;
      let closeTimer = 0;
      const setExpanded = (expanded) => {
        if (expanded) {
          globalNav.querySelectorAll(".global-nav-item.is-menu-open").forEach((openItem) => {
            if (openItem === item) return;
            openItem.classList.remove("is-menu-open");
            openItem.querySelector(".global-nav-trigger")?.setAttribute("aria-expanded", "false");
          });
        }
        item.classList.toggle("is-menu-open", expanded);
        trigger.setAttribute("aria-expanded", String(expanded));
      };
      const scheduleOpen = () => {
        window.clearTimeout(closeTimer);
        window.clearTimeout(openTimer);
        openTimer = window.setTimeout(() => setExpanded(true), 40);
      };
      const scheduleClose = () => {
        window.clearTimeout(openTimer);
        window.clearTimeout(closeTimer);
        closeTimer = window.setTimeout(() => setExpanded(false), 120);
      };
      item.addEventListener("mouseenter", scheduleOpen);
      item.addEventListener("mouseleave", scheduleClose);
      item.addEventListener("focusin", () => {
        window.clearTimeout(openTimer);
        window.clearTimeout(closeTimer);
        setExpanded(true);
      });
      item.addEventListener("focusout", () => {
        window.requestAnimationFrame(() => {
          if (!item.contains(document.activeElement)) setExpanded(false);
        });
      });

      item.append(trigger, menu);
      return item;
    });
    globalNav.replaceChildren(...globalItems);
  }

  const docsRail = document.querySelector("[data-docs-rail]");
  if (docsRail) {
    const railHeader = document.createElement("div");
    railHeader.className = "docs-rail-header";
    const railKicker = document.createElement("span");
    railKicker.textContent = directory.kicker;
    const railTitle = document.createElement("a");
    railTitle.href = new URL(directory.root.href, siteRoot).href;
    railTitle.textContent = directory.title;
    railHeader.append(railKicker, railTitle);

    const railGroups = directory.groups.map((group, groupIndex) => {
      const details = document.createElement("details");
      details.className = "docs-rail-group";
      details.open = true;

      const summary = document.createElement("summary");
      summary.innerHTML = `<small>${String(groupIndex + 1).padStart(2, "0")}</small><strong>${group.label}</strong><span>${group.items.length}</span>`;
      const links = document.createElement("div");
      links.className = "docs-rail-links";
      group.items.forEach((entry) => {
        const link = document.createElement("a");
        link.href = new URL(entry.href, siteRoot).href;
        link.textContent = entry.label;
        if (canonical(link.href) === current) {
          link.classList.add("active");
          link.setAttribute("aria-current", "page");
        }
        links.append(link);
      });
      details.append(summary, links);
      return details;
    });
    docsRail.replaceChildren(railHeader, ...railGroups);
  }

  nav.dataset.directoryModule = moduleKey;
  nav.setAttribute("aria-label", `${directory.title}目录`);

  const context = document.createElement("div");
  context.className = "directory-context";

  const kicker = document.createElement("span");
  kicker.className = "directory-kicker";
  kicker.textContent = directory.kicker;
  context.append(kicker);

  const title = document.createElement("a");
  title.className = "directory-title";
  title.href = new URL(directory.root.href, siteRoot).href;
  title.textContent = directory.title;
  context.append(title);

  if (directory.parent) {
    const parent = document.createElement("a");
    parent.className = "directory-parent";
    parent.href = new URL(directory.parent.href, siteRoot).href;
    parent.textContent = `← ${directory.parent.label}`;
    context.append(parent);
  }

  const sections = [];
  let activeSection = -1;

  directory.groups.forEach((group, groupIndex) => {
    const section = document.createElement("section");
    section.className = "nav-section";

    const headingId = `directory-${moduleKey}-${groupIndex}-heading`;
    const panelId = `directory-${moduleKey}-${groupIndex}-panel`;
    const button = document.createElement("button");
    button.type = "button";
    button.id = headingId;
    button.className = "nav-section-toggle";
    button.setAttribute("aria-controls", panelId);

    const marker = document.createElement("span");
    marker.className = "nav-section-marker";
    marker.textContent = String(groupIndex + 1).padStart(2, "0");
    marker.setAttribute("aria-hidden", "true");

    const label = document.createElement("span");
    label.className = "nav-section-label";
    label.textContent = group.label;

    const count = document.createElement("span");
    count.className = "nav-section-count";
    count.textContent = String(group.items.length);
    count.setAttribute("aria-label", `${group.items.length} 个入口`);

    const caret = document.createElement("span");
    caret.className = "nav-section-caret";
    caret.textContent = "›";
    caret.setAttribute("aria-hidden", "true");

    button.append(marker, label, count, caret);

    const panel = document.createElement("div");
    panel.id = panelId;
    panel.className = "nav-section-panel";
    panel.setAttribute("role", "region");
    panel.setAttribute("aria-labelledby", headingId);

    const links = document.createElement("div");
    links.className = "nav-section-links";

    group.items.forEach((item) => {
      const link = document.createElement("a");
      link.href = new URL(item.href, siteRoot).href;
      link.textContent = item.label;

      if (canonical(link.href) === current) {
        activeSection = groupIndex;
        link.classList.add("active");
        link.setAttribute("aria-current", "page");
      }

      links.append(link);
    });

    panel.append(links);
    section.append(button, panel);
    sections.push({ section, button, panel });
  });

  const setSectionState = (entry, open) => {
    entry.section.classList.toggle("is-open", open);
    entry.button.setAttribute("aria-expanded", String(open));
    entry.panel.setAttribute("aria-hidden", String(!open));
    entry.panel.toggleAttribute("inert", !open);
  };

  const initialSection = activeSection >= 0 ? activeSection : 0;
  sections.forEach((entry, index) => {
    setSectionState(entry, index === initialSection);
    entry.button.addEventListener("click", () => {
      const nextOpen = entry.button.getAttribute("aria-expanded") !== "true";
      sections.forEach((candidate) => setSectionState(candidate, false));
      if (nextOpen) setSectionState(entry, true);
    });
  });

  nav.replaceChildren(context, ...sections.map((entry) => entry.section));

  const brand = document.querySelector("[data-site-root]");
  if (brand) brand.href = new URL("index.html", siteRoot).href;

  const panel = nav.closest(".directory-panel");
  const media = window.matchMedia("(max-width: 999px)");
  const interactiveMobileMenu = window.matchMedia("(max-width: 839px)");
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let closeTimer = 0;
  let lockedScrollY = 0;

  const setPageScrollLock = (locked) => {
    const shouldLock = locked && interactiveMobileMenu.matches;
    if (shouldLock && !document.documentElement.classList.contains("mobile-directory-open")) {
      lockedScrollY = window.scrollY;
      document.documentElement.style.setProperty("--mobile-directory-scroll-top", `${-lockedScrollY}px`);
      document.documentElement.classList.add("mobile-directory-open");
      return;
    }
    if (!shouldLock && document.documentElement.classList.contains("mobile-directory-open")) {
      document.documentElement.classList.remove("mobile-directory-open");
      document.documentElement.style.removeProperty("--mobile-directory-scroll-top");
      window.scrollTo(0, lockedScrollY);
    }
  };

  const finishPanelClose = () => {
    if (!panel) return;
    window.clearTimeout(closeTimer);
    panel.open = false;
    panel.classList.remove("is-closing");
    setPageScrollLock(false);
  };

  const closePanel = () => {
    if (!panel?.open || panel.classList.contains("is-closing")) return;
    panel.classList.add("is-closing");
    if (reducedMotion.matches) {
      finishPanelClose();
      return;
    }
    closeTimer = window.setTimeout(finishPanelClose, 180);
  };

  const summary = panel?.querySelector(":scope > summary");
  summary?.addEventListener("click", (event) => {
    if (!interactiveMobileMenu.matches) return;
    event.preventDefault();
    if (panel.open) {
      closePanel();
      return;
    }
    window.clearTimeout(closeTimer);
    panel.classList.remove("is-closing");
    panel.open = true;
    setPageScrollLock(true);
  });

  document.addEventListener("pointerdown", (event) => {
    if (interactiveMobileMenu.matches && panel?.open && !panel.contains(event.target)) closePanel();
  });
  const containOpenMenuGesture = (event) => {
    if (!interactiveMobileMenu.matches || !panel?.open || panel.classList.contains("is-closing")) return;
    if (nav.contains(event.target)) return;
    event.preventDefault();
    closePanel();
  };
  document.addEventListener("wheel", containOpenMenuGesture, { passive: false });
  document.addEventListener("touchmove", containOpenMenuGesture, { passive: false });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && interactiveMobileMenu.matches && panel?.open) {
      closePanel();
      summary?.focus();
    }
  });

  let previousScrollY = window.scrollY;
  window.addEventListener("scroll", () => {
    const nextScrollY = window.scrollY;
    if (interactiveMobileMenu.matches && panel?.open && nextScrollY > previousScrollY + 8) closePanel();
    previousScrollY = nextScrollY;
  }, { passive: true });

  const syncPanel = (event) => {
    if (!panel) return;
    window.clearTimeout(closeTimer);
    panel.classList.remove("is-closing");
    panel.open = !event.matches;
    setPageScrollLock(false);
  };

  syncPanel(media);
  media.addEventListener("change", syncPanel);
})();
