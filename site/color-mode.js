/* Set the palette before styles load; keep the owner's explicit choice on this device. */
(function () {
  'use strict';
  var root = document.documentElement;
  if (!root) return;
  var key = 'calx-color-mode-v1';
  var preference = null;
  var current = 'light';
  var system = null;
  try { system = window.matchMedia('(prefers-color-scheme: dark)'); } catch (_) {}
  try {
    var saved = window.localStorage.getItem(key);
    if (saved === 'light' || saved === 'dark') preference = saved;
  } catch (_) {}

  function systemTheme() { return system && system.matches ? 'dark' : 'light'; }
  function paintControls() {
    var buttons = document.querySelectorAll('[data-theme-toggle]');
    for (var i = 0; i < buttons.length; i++) {
      var button = buttons[i];
      button.setAttribute('aria-checked', String(current === 'dark'));
      button.setAttribute('title', current === 'dark' ? 'Turn off dark mode' : 'Turn on dark mode');
      var icon = button.querySelector('[data-theme-icon]');
      if (icon) icon.setAttribute('d', current === 'dark'
        ? 'M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8ZM12 2v2m0 16v2M2 12h2m16 0h2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4'
        : 'M20.2 15.5A8.5 8.5 0 0 1 8.5 3.8a8.5 8.5 0 1 0 11.7 11.7Z');
    }
  }
  function apply(theme) {
    current = theme;
    root.setAttribute('data-theme', theme);
    root.style.colorScheme = theme;
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', theme === 'dark' ? '#111922' : '#f36a5d');
    paintControls();
  }
  apply(preference || systemTheme());
  document.addEventListener('click', function (event) {
    var target = event.target && event.target.closest ? event.target.closest('[data-theme-toggle]') : null;
    if (!target) return;
    preference = current === 'dark' ? 'light' : 'dark';
    try { window.localStorage.setItem(key, preference); } catch (_) {}
    apply(preference);
  });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', paintControls, { once: true });
  else paintControls();

  function onSystemChange() { if (!preference) apply(systemTheme()); }
  if (system) {
    if (typeof system.addEventListener === 'function') system.addEventListener('change', onSystemChange);
    else if (typeof system.addListener === 'function') system.addListener(onSystemChange);
  }
  window.addEventListener('storage', function (event) {
    if (event.storageArea) {
      try { if (event.storageArea !== window.localStorage) return; } catch (_) { return; }
    }
    if (event.key !== key && event.key !== null) return;
    preference = event.newValue === 'light' || event.newValue === 'dark' ? event.newValue : null;
    apply(preference || systemTheme());
  });
})();
