(() => {
  "use strict";

  const isDirectoryItemActive = (itemHref, target, current) => {
    if (current === target) return true;

    if (/^[^/]+\/index\.html$/.test(itemHref) && itemHref !== "tools/index.html") {
      return current.startsWith(`${target}/`);
    }

    if (!/^tools\/[^/]+\/index\.html$/.test(itemHref)) return false;

    const docsRoot = `${target}/docs`;
    return current === docsRoot || current.startsWith(`${docsRoot}/`);
  };

  const resolveDirectoryModule = (route) => {
    if (route.startsWith("tools/noemld/docs/")) return "noemldDocs";
    if (route.startsWith("tools/noemld/")) return "noemld";
    if (route.startsWith("tools/")) return "tools";
    if (route.startsWith("docs/")) return "docs";
    if (/^(architecture|specifications|components)\//.test(route)) return "architecture";
    if (/^(downloads|faq)\//.test(route)) return "resources";
    if (/^(development|news)\//.test(route)) return "development";
    return "project";
  };

  const directoryApi = Object.freeze({
    isDirectoryItemActive,
    resolveDirectoryModule
  });

  if (
    typeof document === "undefined"
    && typeof module !== "undefined"
    && module.exports
  ) {
    module.exports = directoryApi;
    return;
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
          label: "架构与设计",
          items: [
            { href: "architecture/index.html", label: "架构" },
            { href: "specifications/index.html", label: "规范" },
            { href: "components/index.html", label: "组件" }
          ]
        },
        {
          label: "资源",
          items: [
            { href: "tools/index.html", label: "工具目录" },
            { href: "docs/index.html", label: "文档中心" },
            { href: "downloads/index.html", label: "下载与资源" },
            { href: "faq/index.html", label: "FAQ" }
          ]
        },
        {
          label: "开发",
          items: [
            { href: "development/index.html", label: "开发入口" },
            { href: "news/index.html", label: "新闻与进展" }
          ]
        }
      ]
    },
    architecture: {
      kicker: "Architecture",
      title: "架构与对象",
      root: { href: "architecture/index.html", label: "架构首页" },
      parent: { href: "index.html", label: "返回项目目录" },
      groups: [
        {
          label: "系统架构",
          items: [
            { href: "architecture/index.html", label: "架构总览" },
            { href: "architecture/object-lifecycle.html", label: "对象生命周期" },
            { href: "architecture/open-questions.html", label: "开放问题" }
          ]
        },
        {
          label: "对象规范",
          items: [
            { href: "specifications/index.html", label: "规范登记" },
            { href: "specifications/gsir.html", label: "GSIR" },
            { href: "specifications/gobj.html", label: "GOBJ" },
            { href: "specifications/sso.html", label: "SSO" }
          ]
        },
        {
          label: "系统组件",
          items: [
            { href: "components/index.html", label: "组件总览" },
            { href: "components/compiler-core.html", label: "Compiler Core" },
            { href: "components/linker-loader.html", label: "Linker、Loader 与 Runtime" },
            { href: "components/nsfe.html", label: "NSFE" }
          ]
        }
      ]
    },
    docs: {
      kicker: "Documentation",
      title: "文档中心",
      root: { href: "docs/index.html", label: "文档首页" },
      parent: { href: "index.html", label: "返回项目目录" },
      groups: [
        {
          label: "开始",
          items: [
            { href: "docs/index.html", label: "文档首页" },
            { href: "docs/getting-started.html", label: "入门指南" },
            { href: "docs/installation-and-usage.html", label: "使用与获取" }
          ]
        },
        {
          label: "指南",
          items: [
            { href: "docs/architecture-guide.html", label: "架构指南" },
            { href: "docs/development-guide.html", label: "开发指南" }
          ]
        },
        {
          label: "参考",
          items: [
            { href: "docs/tools-reference.html", label: "工具参考" },
            { href: "docs/specifications-reference.html", label: "规范参考" }
          ]
        }
      ]
    },
    resources: {
      kicker: "Resources",
      title: "资源与支持",
      root: { href: "downloads/index.html", label: "资源首页" },
      parent: { href: "index.html", label: "返回项目目录" },
      groups: [
        {
          label: "获取资源",
          items: [
            { href: "downloads/index.html", label: "下载与资源" },
            { href: "docs/index.html", label: "文档中心" }
          ]
        },
        {
          label: "支持",
          items: [
            { href: "faq/index.html", label: "FAQ" },
            { href: "development/index.html", label: "开发与贡献" }
          ]
        }
      ]
    },
    development: {
      kicker: "Development",
      title: "开发与进展",
      root: { href: "development/index.html", label: "开发首页" },
      parent: { href: "index.html", label: "返回项目目录" },
      groups: [
        {
          label: "开发",
          items: [
            { href: "development/index.html", label: "开发入口" },
            { href: "development/implementation-roadmap.html", label: "实施路线图" },
            { href: "development/testing.html", label: "测试策略" }
          ]
        },
        {
          label: "进展",
          items: [
            { href: "news/index.html", label: "新闻与进展" },
            { href: "architecture/open-questions.html", label: "开放问题" }
          ]
        }
      ]
    },
    tools: {
      kicker: "Toolchain",
      title: "工具目录",
      root: { href: "tools/index.html", label: "工具总览" },
      parent: { href: "index.html", label: "返回项目目录" },
      groups: [
        {
          label: "工具链",
          items: [
            { href: "tools/index.html", label: "工具总览" }
          ]
        },
        {
          label: "合规套件",
          items: [
            { href: "tools/noemconform/index.html", label: "noemconform · 合规套件" }
          ]
        },
        {
          label: "对象工具",
          items: [
            { href: "tools/noemobj/index.html", label: "noemobj · 对象查看" },
            { href: "tools/noemverify/index.html", label: "noemverify · 对象验证" },
            { href: "tools/noemcopy/index.html", label: "noemcopy · 对象变换" },
            { href: "tools/noemsize/index.html", label: "noemsize · 尺寸分析" }
          ]
        },
        {
          label: "文本 IR",
          items: [
            { href: "tools/noemas/index.html", label: "noemas · IR 汇编" },
            { href: "tools/noemdis/index.html", label: "noemdis · IR 反汇编" },
            { href: "tools/noemfmt/index.html", label: "noemfmt · 文本规范化" },
            { href: "tools/noemdiff/index.html", label: "noemdiff · 语义差异" }
          ]
        },
        {
          label: "编译与链接",
          items: [
            { href: "tools/noemc/index.html", label: "noemc · 编译器" },
            { href: "tools/noemlint/index.html", label: "noemlint · 语义检查" },
            { href: "tools/noemar/index.html", label: "noemar · 对象归档" },
            { href: "tools/noemnm/index.html", label: "noemnm · 符号检查" },
            { href: "tools/noemld/index.html", label: "noemld · 链接器" }
          ]
        },
        {
          label: "发布与运行",
          items: [
            { href: "tools/noemstrip/index.html", label: "noemstrip · 调试剥离" },
            { href: "tools/noemcov/index.html", label: "noemcov · 覆盖审计" },
            { href: "tools/noempack/index.html", label: "noempack · 发布打包" },
            { href: "tools/noemrun/index.html", label: "noemrun · 可信执行" },
            { href: "tools/noemtrace/index.html", label: "noemtrace · 运行追踪" }
          ]
        },
        {
          label: "模型工程",
          items: [
            { href: "tools/noemdata/index.html", label: "noemdata · 数据工程" },
            { href: "tools/noemtrain/index.html", label: "noemtrain · 训练编排" },
            { href: "tools/noemeval/index.html", label: "noemeval · 模型评估" },
            { href: "tools/noemquant/index.html", label: "noemquant · 量化部署" }
          ]
        }
      ]
    },
    noemld: {
      kicker: "Tool Project",
      title: "noemld",
      root: { href: "tools/noemld/index.html", label: "noemld 项目页" },
      parent: { href: "tools/index.html", label: "返回工具目录" },
      groups: [
        {
          label: "项目入口",
          items: [
            { href: "tools/noemld/index.html", label: "noemld 项目页" },
            { href: "tools/noemld/docs/index.html", label: "noemld 文档" }
          ]
        },
        {
          label: "关键文档",
          items: [
            { href: "tools/noemld/docs/contract.html", label: "工具契约" },
            { href: "tools/noemld/docs/inputs-outputs.html", label: "输入与输出" },
            { href: "tools/noemld/docs/pipeline.html", label: "处理流程" },
            { href: "tools/noemld/docs/loader-security.html", label: "装载与安全" }
          ]
        },
        {
          label: "相关入口",
          items: [
            { href: "specifications/index.html", label: "对象规范" },
            { href: "components/linker-loader.html", label: "Linker、Loader 与 Runtime" }
          ]
        }
      ]
    },
    noemldDocs: {
      kicker: "Tool Documentation",
      title: "noemld 文档",
      root: { href: "tools/noemld/docs/index.html", label: "文档首页" },
      parent: { href: "tools/noemld/index.html", label: "返回 noemld 项目页" },
      groups: [
        {
          label: "开始",
          items: [
            { href: "tools/noemld/docs/index.html", label: "文档首页" },
            { href: "tools/noemld/docs/contract.html", label: "工具契约" },
            { href: "tools/noemld/docs/inputs-outputs.html", label: "输入与输出" },
            { href: "tools/noemld/docs/invocation.html", label: "命令行调用" }
          ]
        },
        {
          label: "链接流程",
          items: [
            { href: "tools/noemld/docs/pipeline.html", label: "处理流程" },
            { href: "tools/noemld/docs/symbol-resolution.html", label: "符号解析" },
            { href: "tools/noemld/docs/relocations.html", label: "重定位与 ID 重映射" },
            { href: "tools/noemld/docs/sso-linking.html", label: "SSO 链接" }
          ]
        },
        {
          label: "安全与质量",
          items: [
            { href: "tools/noemld/docs/loader-security.html", label: "装载与安全" },
            { href: "tools/noemld/docs/diagnostics.html", label: "诊断与失败边界" },
            { href: "tools/noemld/docs/testing.html", label: "测试与放行门" }
          ]
        },
        {
          label: "参考",
          items: [
            { href: "tools/noemld/docs/dependencies.html", label: "上下游依赖" },
            { href: "tools/noemld/docs/reference-index.html", label: "参考索引" }
          ]
        }
      ]
    }
  });

  const PORTAL_NAV_ITEMS = Object.freeze([
    { href: "about/background.html", label: "为什么" },
    { href: "architecture/object-lifecycle.html", label: "如何工作" },
    { href: "specifications/index.html", label: "规范" },
    { href: "tools/index.html", label: "工具" },
    { href: "docs/index.html", label: "文档" }
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

  const moduleKey = resolveDirectoryModule(currentRoute);
  const directory = DIRECTORY_MODULES[moduleKey];
  const current = canonical(window.location.href);

  const portalNav = document.querySelector("[data-portal-nav]");
  if (portalNav) {
    const portalLinks = PORTAL_NAV_ITEMS.map((item) => {
      const link = document.createElement("a");
      link.className = "portal-nav-link";
      link.href = new URL(item.href, siteRoot).href;
      link.textContent = item.label;
      return link;
    });
    portalNav.replaceChildren(...portalLinks);
  }

  const portalStage = document.querySelector("[data-portal-stage]");
  if (portalStage) portalStage.href = new URL("development/index.html", siteRoot).href;

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
  const syncPanel = (event) => {
    if (panel) panel.open = !event.matches;
  };

  syncPanel(media);
  media.addEventListener("change", syncPanel);
})();
