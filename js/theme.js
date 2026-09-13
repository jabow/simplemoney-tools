/* ============================================================================
   Simple Money Tools — theme switching
   ----------------------------------------------------------------------------
   Load in <head>, WITHOUT defer or async:
       <script src="js/theme.js?v=1"></script>
   It has to run before the browser paints, otherwise a visitor who has chosen
   the opposite of their system theme sees a flash of the wrong one.

   Three states, cycled by the button:  system -> light -> dark -> system
   "system" stores nothing and tracks the OS live, so it is the default for
   everyone who has never pressed the button.
   ========================================================================== */
(function () {
  "use strict";

  var KEY = "smt-theme";
  var root = document.documentElement;
  var media = window.matchMedia ? window.matchMedia("(prefers-color-scheme: dark)") : null;

  function stored() {
    try {
      var v = localStorage.getItem(KEY);
      return v === "light" || v === "dark" ? v : null;
    } catch (e) {
      return null; // private mode, blocked storage — fall back to system
    }
  }

  function save(v) {
    try {
      if (v) localStorage.setItem(KEY, v);
      else localStorage.removeItem(KEY);
    } catch (e) {
      /* nothing to do — the choice just won't survive a reload */
    }
  }

  function mode() { return stored() || "system"; }

  function effective() {
    var m = mode();
    if (m !== "system") return m;
    return media && media.matches ? "dark" : "light";
  }

  function paint() {
    var m = mode();
    if (m === "system") root.removeAttribute("data-theme");
    else root.setAttribute("data-theme", m);
  }

  // Runs immediately, before first paint.
  paint();

  /* -- the button ---------------------------------------------------------- */

  var LABELS = {
    system: "Theme: following your system. Switch to light.",
    light: "Theme: light. Switch to dark.",
    dark: "Theme: dark. Switch back to your system setting."
  };
  var NEXT = { system: "light", light: "dark", dark: "system" };

  var ICONS =
    '<svg class="icon-system" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">' +
      '<circle cx="12" cy="12" r="8"/><path d="M12 4v16a8 8 0 0 0 0-16z" fill="currentColor" stroke="none"/>' +
    "</svg>" +
    '<svg class="icon-light" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">' +
      '<circle cx="12" cy="12" r="4.2"/><path d="M12 2.6v2.2M12 19.2v2.2M4.2 12H2M22 12h-2.2M6.3 6.3 4.8 4.8M19.2 19.2l-1.5-1.5M17.7 6.3l1.5-1.5M4.8 19.2l1.5-1.5"/>' +
    "</svg>" +
    '<svg class="icon-dark" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M20 14.2A8.4 8.4 0 0 1 9.8 4 8.4 8.4 0 1 0 20 14.2z"/>' +
    "</svg>";

  var btn = null;

  function sync() {
    if (!btn) return;
    var m = mode();
    btn.setAttribute("data-mode", m);
    btn.setAttribute("aria-label", LABELS[m]);
    btn.setAttribute("title", LABELS[m]);
  }

  function build() {
    var nav = document.querySelector(".site-header .nav-inner");
    if (!nav || document.querySelector(".theme-toggle")) return;

    btn = document.createElement("button");
    btn.type = "button";
    btn.className = "theme-toggle";
    btn.innerHTML = ICONS;
    sync();

    btn.addEventListener("click", function () {
      save(NEXT[mode()] === "system" ? null : NEXT[mode()]);
      paint();
      sync();
    });

    // Before the hamburger, so it stays reachable on mobile instead of being
    // buried inside the menu panel. CSS handles the ordering at both sizes.
    var hamburger = nav.querySelector(".nav-toggle");
    if (hamburger) nav.insertBefore(btn, hamburger);
    else nav.appendChild(btn);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", build);
  } else {
    build();
  }

  /* -- follow the OS live while no explicit choice is stored --------------- */

  if (media) {
    var onChange = function () {
      if (mode() === "system") { paint(); sync(); }
    };
    if (media.addEventListener) media.addEventListener("change", onChange);
    else if (media.addListener) media.addListener(onChange); // older Safari
  }

  /* -- keep tabs in step --------------------------------------------------- */

  window.addEventListener("storage", function (e) {
    if (e.key === KEY) { paint(); sync(); }
  });
})();
