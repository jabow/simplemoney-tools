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

/* ---- Contact form ------------------------------------------------------------
 * Posts to contact.php, which emails SimpleMoneyTools1@gmail.com and answers
 * with JSON. The form keeps a real action/method, so it still submits (as a
 * normal page POST) if this script fails to load — the fetch path below is
 * the progressive enhancement, not the only route.
 *
 * The one rule here: never tell someone their message was sent unless the
 * server actually said so. Every failure path names the email address
 * instead, because a message silently lost is worse than an ugly error.
 */

var CONTACT_EMAIL = "SimpleMoneyTools1@gmail.com";

function initContactForm() {
  var form = document.querySelector("[data-contact-form]");
  if (!form) return;

  var statusEl = form.querySelector("[data-form-status]");
  var submitBtn = form.querySelector('button[type="submit"]');
  var submitLabel = submitBtn ? submitBtn.textContent : "";

  showRedirectOutcome();

  /*
   * The no-JavaScript path posts the form normally, and contact.php answers
   * that with a redirect carrying the outcome in the query string. If this
   * script did load afterwards (JS was merely slow, not off), surface that
   * outcome here rather than leaving the visitor on a page that looks like
   * nothing happened.
   */
  function showRedirectOutcome() {
    if (!window.URLSearchParams) return;
    var params = new URLSearchParams(window.location.search);
    if (!params.has("sent")) return;

    if (params.get("sent") === "1") {
      setStatus(
        "Thanks — your message has been sent. You'll get a reply to the address you gave.",
        "success"
      );
    } else {
      var reason = params.get("reason") || "Something went wrong sending that.";
      setStatus(reason + " You can email " + CONTACT_EMAIL + " directly instead.", "error");
    }

    // Drop the parameters so a refresh doesn't replay a stale message.
    if (window.history && window.history.replaceState) {
      window.history.replaceState({}, "", window.location.pathname + window.location.hash);
    }
  }

  function setStatus(message, kind) {
    if (!statusEl) return;
    statusEl.textContent = message;
    statusEl.classList.toggle("is-success", kind === "success");
    statusEl.classList.toggle("is-error", kind === "error");
  }

  function setBusy(busy) {
    if (!submitBtn) return;
    submitBtn.disabled = busy;
    submitBtn.textContent = busy ? "Sending…" : submitLabel;
  }

  form.addEventListener("submit", function (e) {
    // Only intercept where fetch can actually take over. On anything older,
    // fall through to the plain form POST rather than blocking submission.
    if (!window.fetch || !window.FormData) return;

    e.preventDefault();

    if (!validateForm(form)) {
      setStatus("Please fix the highlighted fields before sending.", "error");
      return;
    }

    setBusy(true);
    setStatus("Sending your message…", "");

    fetch(form.getAttribute("action"), {
      method: "POST",
      body: new FormData(form),
      headers: { Accept: "application/json" },
    })
      .then(function (res) {
        // A non-JSON body here means PHP itself errored (or isn't running
        // at all, e.g. previewed over file://) — treat it as a failure
        // rather than reading a 200 as proof of delivery.
        return res.json().then(
          function (data) {
            return { ok: res.ok, data: data };
          },
          function () {
            return { ok: false, data: null };
          }
        );
      })
      .then(function (result) {
        if (result.ok && result.data && result.data.ok) {
          form.reset();
          setStatus(
            "Thanks — your message has been sent. You'll get a reply to the address you gave.",
            "success"
          );
          return;
        }

        var reason =
          result.data && result.data.error
            ? result.data.error
            : "Something went wrong sending that.";
        setStatus(reason + " You can email " + CONTACT_EMAIL + " directly instead.", "error");
      })
      .catch(function () {
        setStatus(
          "Couldn't reach the server — check your connection, or email " +
            CONTACT_EMAIL +
            " directly instead.",
          "error"
        );
      })
      .then(function () {
        setBusy(false);
      });
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
