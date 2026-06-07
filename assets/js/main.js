/* Herzensfaden – interactions */
(function () {
  "use strict";
  var body = document.body;

  /* ---- Mobile nav ---- */
  var toggle = document.querySelector(".nav-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.querySelectorAll(".nav-menu a").forEach(function (a) {
      a.addEventListener("click", function () {
        body.classList.remove("nav-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  /* ---- Sticky header shadow ---- */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () {
      header.classList.toggle("scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---- Scroll reveal ---- */
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window &&
      !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- Region toggle (Bücher CH / DE) ---- */
  document.querySelectorAll("[data-region-switch]").forEach(function (group) {
    var btns = group.querySelectorAll("[data-region]");
    btns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var region = btn.getAttribute("data-region");
        btns.forEach(function (b) { b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
        document.querySelectorAll("[data-region-panel]").forEach(function (p) {
          p.hidden = p.getAttribute("data-region-panel") !== region;
        });
      });
    });
  });

  /* ---- Forms (mailto by default, optional fetch backend) ---- */
  var DEFAULT_RECIPIENT = "brigitte.meissner@bluewin.ch";

  // Optional: echten Versand aktivieren (Anfragen kommen direkt ins Postfach,
  // ohne das E-Mail-Programm der Besucher zu öffnen).
  // 1. Kostenloses Formular auf https://formspree.io erstellen.
  // 2. Die Endpunkt-URL hier eintragen, z. B. "https://formspree.io/f/abcdwxyz".
  // Leer ("") lässt alles beim bisherigen mailto-Verhalten.
  var FORM_ENDPOINT = "https://formspree.io/f/xqeopnva";

  function cleanLabel(text) {
    return (text || "").replace(/\*/g, "").replace(/\s+/g, " ").trim();
  }

  // Human-readable label for a form control, used to build the e-mail text.
  function fieldLabel(el) {
    if (el.dataset && el.dataset.label) { return el.dataset.label; }
    var field = el.closest(".field");
    if (field) {
      var span = field.querySelector(":scope > span");
      if (span) { return cleanLabel(span.textContent); }
    }
    var label = el.closest("label");
    if (label) { return cleanLabel(label.textContent); }
    return el.name;
  }

  // Collect all filled-in controls in DOM order; checkbox groups are merged.
  function collectFields(form) {
    var lines = [];
    var index = {};
    Array.prototype.forEach.call(form.elements, function (el) {
      if (!el.name || el.disabled || el.name === "_gotcha") { return; }
      var type = (el.type || "").toLowerCase();
      if (type === "submit" || type === "button" || type === "reset" || type === "file") { return; }
      if ((type === "checkbox" || type === "radio") && !el.checked) { return; }
      var value = (el.value || "").trim();
      if (!value) { return; }
      if (type === "checkbox" && index[el.name] != null) {
        lines[index[el.name]].value += ", " + value;
        return;
      }
      if (type === "checkbox") { index[el.name] = lines.length; }
      lines.push({ label: fieldLabel(el), value: value });
    });
    return lines;
  }

  // HTML5 constraint validation with visible field highlighting.
  function validate(form, result) {
    var firstInvalid = null;
    Array.prototype.forEach.call(form.elements, function (el) {
      if (!el.name || el.disabled || !el.willValidate) { return; }
      var field = el.closest(".field") || el.closest(".check-group");
      if (field) { field.classList.remove("field--error"); }
      if (el.checkValidity()) {
        el.removeAttribute("aria-invalid");
      } else {
        if (field) { field.classList.add("field--error"); }
        el.setAttribute("aria-invalid", "true");
        if (!firstInvalid) { firstInvalid = el; }
      }
    });
    if (firstInvalid) {
      if (result) {
        result.textContent = "Bitte ergänzen Sie die rot markierten Felder.";
        result.classList.add("is-error");
        result.classList.remove("is-ok");
      }
      firstInvalid.focus();
      return false;
    }
    return true;
  }

  function mailSubject(form) {
    var topicEl = form.querySelector('[name="topic"], [name="region"]');
    var topic = topicEl ? topicEl.value : "";
    var subjectBase = form.dataset.mailtoSubject || "Kontakt/Anmeldung Herzensfaden";
    return subjectBase + (topic ? " – " + topic : "");
  }

  function buildMailto(form) {
    var lines = collectFields(form);
    var recipient = form.dataset.mailtoRecipient || DEFAULT_RECIPIENT;
    var subject = mailSubject(form);
    var body = lines.map(function (l) { return l.label + ": " + l.value; }).join("\n") + "\n";
    return "mailto:" + encodeURIComponent(recipient) +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(body);
  }

  function setResult(result, text, ok) {
    if (!result) { return; }
    result.textContent = text;
    result.classList.toggle("is-ok", !!ok);
    result.classList.toggle("is-error", !ok);
  }

  document.querySelectorAll("form.contact-form, form.mailto-form").forEach(function (form) {
    var result = form.querySelector(".form-result");

    // Inject a spam honeypot: bots tend to fill every field; humans never see it.
    // "_gotcha" is also recognised and filtered by Formspree.
    if (!form.querySelector('[name="_gotcha"]')) {
      var hp = document.createElement("div");
      hp.className = "hp";
      hp.setAttribute("aria-hidden", "true");
      hp.innerHTML = '<label>Bitte freilassen<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label>';
      form.appendChild(hp);
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!validate(form, result)) { return; }

      // Honeypot triggered → silently pretend success, send nothing.
      var hpField = form.querySelector('[name="_gotcha"]');
      if (hpField && hpField.value) {
        setResult(result, "Vielen Dank für Ihre Nachricht.", true);
        return;
      }

      var actionUrl = form.dataset.actionUrl || FORM_ENDPOINT;
      if (actionUrl) {
        // Real submission to a form backend (e.g. Formspree) – no e-mail program needed.
        var submitBtn = form.querySelector('[type="submit"]');
        var label = submitBtn ? submitBtn.textContent : "";
        if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = "Wird gesendet …"; }
        setResult(result, "Wird gesendet …", true);
        var payload = new FormData(form);
        if (!payload.has("_subject")) { payload.append("_subject", mailSubject(form)); }
        fetch(actionUrl, {
          method: "POST",
          body: payload,
          headers: { Accept: "application/json" }
        }).then(function (res) {
          if (!res.ok) { throw new Error("Request failed"); }
          form.reset();
          setResult(result, "Vielen Dank! Ihre Nachricht wurde gesendet. Ich melde mich so schnell wie möglich zurück.", true);
        }).catch(function () {
          setResult(result, "Senden nicht möglich. Bitte nutzen Sie das E-Mail-Programm – es öffnet sich jetzt.", false);
          window.location.href = buildMailto(form);
        }).then(function () {
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = label; }
        });
        return;
      }

      // Default: hand off to the visitor's e-mail program with a prefilled message.
      setResult(result, "Ihr E-Mail-Programm wird geöffnet. Bitte prüfen Sie den Text und senden Sie die Nachricht ab.", true);
      window.location.href = buildMailto(form);
    });

    // Clear the error state on a field as soon as the visitor edits it.
    form.addEventListener("input", function (event) {
      var el = event.target;
      if (!el.name) { return; }
      var field = el.closest(".field") || el.closest(".check-group");
      if (field && el.willValidate && el.checkValidity()) {
        field.classList.remove("field--error");
        el.removeAttribute("aria-invalid");
      }
    });
  });

  /* ---- Footer year ---- */
  var y = document.querySelector("[data-year]");
  if (y) { y.textContent = new Date().getFullYear(); }
})();
