/*
 * Simple Money Tools — shared site behaviour.
 * Vanilla JS, no dependencies. Every block below guards for the elements
 * it needs, so this single file can be safely included on every page.
 */

document.addEventListener("DOMContentLoaded", function () {
  setFooterYear();
  initMobileNav();
  initBackToTop();
  initRevealAnimations();
  initToolFilters();
  initTutorialFilters();
  initContactForm();
  initNewsletterForm();
});

/* ---- Footer year --------------------------------------------------------- */

function setFooterYear() {
  var yearEl = document.getElementById("year");
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }
}

/* ---- Mobile navigation ---------------------------------------------------- */

function initMobileNav() {
  var toggle = document.querySelector(".nav-toggle");
  var links = document.querySelector(".nav-links");
  if (!toggle || !links) return;

  toggle.addEventListener("click", function () {
    var isOpen = links.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    document.body.style.overflow = isOpen ? "hidden" : "";
  });

  links.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      links.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    });
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && links.classList.contains("is-open")) {
      links.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
      toggle.focus();
    }
  });
}

/* ---- Back to top button ---------------------------------------------------- */

function initBackToTop() {
  var btn = document.querySelector(".back-to-top");
  if (!btn) return;

  window.addEventListener(
    "scroll",
    function () {
      btn.classList.toggle("is-visible", window.scrollY > 600);
    },
    { passive: true }
  );

  btn.addEventListener("click", function () {
    window.scrollTo({
      top: 0,
      behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
        ? "auto"
        : "smooth",
    });
  });
}

/* ---- Reveal-on-scroll animation -------------------------------------------- */

function initRevealAnimations() {
  var targets = document.querySelectorAll(".reveal");
  if (!targets.length) return;

  if (
    window.matchMedia("(prefers-reduced-motion: reduce)").matches ||
    !("IntersectionObserver" in window)
  ) {
    targets.forEach(function (el) {
      el.classList.add("is-visible");
    });
    return;
  }

  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );

  targets.forEach(function (el) {
    observer.observe(el);
  });
}

/* ---- Tools page filtering --------------------------------------------------- */

function initToolFilters() {
  var filterBar = document.querySelector("[data-tool-filters]");
  var cards = document.querySelectorAll("[data-tool-card]");
  if (!filterBar || !cards.length) return;

  var buttons = filterBar.querySelectorAll(".filter-btn");
  var emptyState = document.querySelector("[data-tools-empty]");

  filterBar.addEventListener("click", function (e) {
    var btn = e.target.closest(".filter-btn");
    if (!btn) return;

    buttons.forEach(function (b) {
      b.setAttribute("aria-pressed", "false");
    });
    btn.setAttribute("aria-pressed", "true");

    var filter = btn.getAttribute("data-filter");
    var visibleCount = 0;

    cards.forEach(function (card) {
      var tags = (card.getAttribute("data-tags") || "").split(" ");
      var show = filter === "all" || tags.indexOf(filter) !== -1;
      card.style.display = show ? "" : "none";
      if (show) visibleCount++;
    });

    if (emptyState) {
      emptyState.classList.toggle("is-visible", visibleCount === 0);
    }
  });
}

/* ---- Tutorials page filtering + search --------------------------------------- */

function initTutorialFilters() {
  var filterBar = document.querySelector("[data-tutorial-filters]");
  var searchInput = document.querySelector("[data-tutorial-search]");
  var cards = document.querySelectorAll("[data-tutorial-card]");
  var emptyState = document.querySelector("[data-tutorials-empty]");

  if (!cards.length) return;

  var activeFilter = "all";

  function applyFilters() {
    var query = (searchInput ? searchInput.value : "").trim().toLowerCase();
    var visibleCount = 0;

    cards.forEach(function (card) {
      var tags = (card.getAttribute("data-tags") || "").split(" ");
      var searchText = (card.getAttribute("data-search") || "").toLowerCase();
      var matchesFilter = activeFilter === "all" || tags.indexOf(activeFilter) !== -1;
      var matchesQuery = query === "" || searchText.indexOf(query) !== -1;
      var show = matchesFilter && matchesQuery;
      card.style.display = show ? "" : "none";
      if (show) visibleCount++;
    });

    if (emptyState) {
      emptyState.classList.toggle("is-visible", visibleCount === 0);
    }
  }

  if (filterBar) {
    var buttons = filterBar.querySelectorAll(".filter-btn");
    filterBar.addEventListener("click", function (e) {
      var btn = e.target.closest(".filter-btn");
      if (!btn) return;
      buttons.forEach(function (b) {
        b.setAttribute("aria-pressed", "false");
      });
      btn.setAttribute("aria-pressed", "true");
      activeFilter = btn.getAttribute("data-filter");
      applyFilters();
    });
  }

  if (searchInput) {
    searchInput.addEventListener("input", applyFilters);
  }
}

/* ---- Contact form: client-side validation only --------------------------------
 * This is a static site with no backend configured. Submission is intentionally
 * disabled — see contact.html and README.md for the documented placeholder.
 */

function initContactForm() {
  var form = document.querySelector("[data-contact-form]");
  if (!form) return;

  var statusEl = form.querySelector("[data-form-status]");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var valid = validateForm(form);

    if (!valid) {
      if (statusEl) {
        statusEl.textContent = "Please fix the highlighted fields before sending.";
        statusEl.classList.remove("is-success");
        statusEl.classList.add("is-error");
      }
      return;
    }

    if (statusEl) {
      statusEl.textContent =
        "This form isn't connected to a backend yet, so nothing was actually sent. " +
        "Please email hello@simplemoney-tools.co.uk directly for now.";
      statusEl.classList.remove("is-error");
      statusEl.classList.add("is-success");
    }
  });
}

function initNewsletterForm() {
  var form = document.querySelector("[data-newsletter-form]");
  if (!form) return;

  var statusEl = form.querySelector("[data-form-status]");

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var valid = validateForm(form);

    if (!valid) {
      if (statusEl) {
        statusEl.textContent = "Please enter a valid email address.";
        statusEl.classList.remove("is-success");
        statusEl.classList.add("is-error");
      }
      return;
    }

    if (statusEl) {
      statusEl.textContent =
        "This is a placeholder — no email service is connected yet, so you have not been signed up.";
      statusEl.classList.remove("is-error");
      statusEl.classList.add("is-success");
    }
  });
}

function validateForm(form) {
  var valid = true;
  var fields = form.querySelectorAll("[required]");

  fields.forEach(function (field) {
    var errorEl = form.querySelector('[data-error-for="' + field.id + '"]');
    var fieldValid = field.checkValidity();

    if (!fieldValid) {
      valid = false;
    }

    if (errorEl) {
      errorEl.textContent = fieldValid ? "" : errorMessageFor(field);
    }

    field.setAttribute("aria-invalid", fieldValid ? "false" : "true");
  });

  return valid;
}

function errorMessageFor(field) {
  if (field.type === "email") {
    return "Enter a valid email address.";
  }
  if (field.validity.valueMissing) {
    return "This field is required.";
  }
  return "Please check this field.";
}
