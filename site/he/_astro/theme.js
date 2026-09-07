(function () {
  "use strict";

  var KEY = "pvc-theme";

  function stored() {
    try { return localStorage.getItem(KEY); } catch (e) { return null; }
  }

  function apply(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    try { localStorage.setItem(KEY, theme); } catch (e) {}
    var toggles = document.querySelectorAll(".theme-toggle");
    toggles.forEach(function (t) {
      t.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
      t.setAttribute("title", theme === "dark" ? "Light mode" : "Dark mode");
    });
  }

  // Initial theme: stored > system preference
  var initial = stored();
  if (!initial) {
    initial = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  apply(initial);

  // Follow system changes unless user chose explicitly
  if (window.matchMedia) {
    var mq = window.matchMedia("(prefers-color-scheme: dark)");
    var handler = function (e) {
      if (!stored()) apply(e.matches ? "dark" : "light");
    };
    if (mq.addEventListener) mq.addEventListener("change", handler);
    else if (mq.addListener) mq.addListener(handler);
  }

  // Wire toggle buttons
  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".theme-toggle").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var cur = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
        apply(cur === "dark" ? "light" : "dark");
      });
    });
  });
})();
