(() => {
  "use strict";

  const STORAGE_KEY = "noemion-theme";
  const MODES = ["light", "dark", "system"];
  const MODE_LABELS = { light: "浅色", dark: "深色", system: "跟随系统" };
  const root = document.documentElement;
  const systemTheme = window.matchMedia("(prefers-color-scheme: dark)");

  const readPreference = () => {
    try {
      const stored = window.localStorage.getItem(STORAGE_KEY);
      return MODES.includes(stored) ? stored : "system";
    } catch (_error) {
      return "system";
    }
  };

  const resolvedTheme = (mode) => (
    mode === "system" ? (systemTheme.matches ? "dark" : "light") : mode
  );

  const applyTheme = (mode, persist = false) => {
    const selected = MODES.includes(mode) ? mode : "system";
    const resolved = resolvedTheme(selected);
    root.dataset.theme = selected;
    root.dataset.resolvedTheme = resolved;
    root.style.colorScheme = resolved;
    if (persist) {
      try {
        window.localStorage.setItem(STORAGE_KEY, selected);
      } catch (_error) {
        // The selected theme still applies when storage is unavailable.
      }
    }
    root.dispatchEvent(new CustomEvent("noemion:themechange", {
      detail: { selected, resolved },
    }));
  };

  applyTheme(readPreference());
  systemTheme.addEventListener("change", () => {
    if (root.dataset.theme === "system") applyTheme("system");
  });

  const initializePicker = () => {
    const picker = document.querySelector("[data-theme-picker]");
    if (!picker) return;
    const trigger = picker.querySelector("[data-theme-trigger]");
    const menu = picker.querySelector("[data-theme-menu]");
    const name = picker.querySelector("[data-theme-name]");
    const options = [...picker.querySelectorAll("[data-theme-option]")];
    if (!trigger || !menu || !name || options.length !== MODES.length) return;

    let closeTimer = 0;
    const updateState = () => {
      const selected = root.dataset.theme || "system";
      name.textContent = MODE_LABELS[selected];
      trigger.setAttribute("aria-label", `主题：${name.textContent}`);
      options.forEach((option) => {
        const active = option.dataset.themeOption === selected;
        option.setAttribute("aria-checked", String(active));
        option.classList.toggle("is-active", active);
      });
    };

    const setOpen = (open, focusOption = false) => {
      window.clearTimeout(closeTimer);
      trigger.setAttribute("aria-expanded", String(open));
      if (open) {
        menu.hidden = false;
        window.requestAnimationFrame(() => {
          menu.dataset.state = "open";
          if (focusOption) {
            (options.find((option) => option.classList.contains("is-active")) || options[0]).focus();
          }
        });
      } else {
        menu.dataset.state = "closed";
        closeTimer = window.setTimeout(() => {
          if (menu.dataset.state === "closed") menu.hidden = true;
        }, 150);
      }
    };

    trigger.addEventListener("click", () => {
      setOpen(trigger.getAttribute("aria-expanded") !== "true");
    });
    trigger.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && trigger.getAttribute("aria-expanded") === "true") {
        event.preventDefault();
        setOpen(false);
        return;
      }
      if (event.key === "ArrowDown" || event.key === "ArrowUp") {
        event.preventDefault();
        setOpen(true, true);
      }
    });
    options.forEach((option, index) => {
      option.addEventListener("click", () => {
        applyTheme(option.dataset.themeOption, true);
        updateState();
        setOpen(false);
        trigger.focus();
      });
      option.addEventListener("keydown", (event) => {
        let targetIndex = null;
        if (event.key === "ArrowDown") targetIndex = (index + 1) % options.length;
        if (event.key === "ArrowUp") targetIndex = (index - 1 + options.length) % options.length;
        if (event.key === "Home") targetIndex = 0;
        if (event.key === "End") targetIndex = options.length - 1;
        if (targetIndex !== null) {
          event.preventDefault();
          options[targetIndex].focus();
        }
      });
    });
    menu.addEventListener("keydown", (event) => {
      if (event.key === "Escape") {
        event.preventDefault();
        setOpen(false);
        trigger.focus();
      }
    });
    document.addEventListener("pointerdown", (event) => {
      if (!picker.contains(event.target)) setOpen(false);
    });
    root.addEventListener("noemion:themechange", updateState);
    updateState();
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializePicker, { once: true });
  } else {
    initializePicker();
  }
})();
