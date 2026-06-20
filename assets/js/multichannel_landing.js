/* Multi-channel listing landing v2 */
(function () {
  "use strict";

  /* Sticky nav after util bar scrolls away */
  (function () {
    var utilBar = document.querySelector(".util-bar");
    var nav = document.querySelector("nav");
    if (!utilBar || !nav) return;
    var spacer = document.querySelector(".sc-nav-spacer");
    if (!spacer) {
      spacer = document.createElement("div");
      spacer.className = "sc-nav-spacer";
      nav.parentNode.insertBefore(spacer, nav.nextSibling);
    }
    function tick() {
      var threshold = utilBar.offsetHeight;
      if (window.scrollY >= threshold) {
        nav.classList.add("sc-nav-fixed");
        spacer.classList.add("active");
      } else {
        nav.classList.remove("sc-nav-fixed");
        spacer.classList.remove("active");
      }
    }
    window.addEventListener("scroll", tick, { passive: true });
    tick();
  })();

  /* Testimonial carousel */
  (function () {
    var track = document.getElementById("ttrack");
    var dotsEl = document.getElementById("tdots");
    if (!track || !dotsEl) return;

    var cards = track.querySelectorAll(".tcard");
    var perPage = 3;
    var pages = Math.ceil(cards.length / perPage);
    var current = 0;

    dotsEl.innerHTML = "";
    for (var i = 0; i < pages; i++) {
      var dot = document.createElement("button");
      dot.className = "tdot" + (i === 0 ? " active" : "");
      dot.type = "button";
      (function (page) {
        dot.onclick = function () {
          goTo(page);
        };
      })(i);
      dotsEl.appendChild(dot);
    }

    function goTo(p) {
      current = ((p % pages) + pages) % pages;
      var cardW = cards[0].offsetWidth + 20;
      track.style.transform = "translateX(-" + current * perPage * cardW + "px)";
      var dots = dotsEl.querySelectorAll(".tdot");
      for (var j = 0; j < dots.length; j++) {
        dots[j].classList.toggle("active", j === current);
      }
    }

    var prev = document.getElementById("tprev");
    var next = document.getElementById("tnext");
    if (prev) prev.onclick = function () { goTo(current - 1); };
    if (next) next.onclick = function () { goTo(current + 1); };
  })();

  /* Demo modal */
  window.scModal = function () {
    var overlay = document.getElementById("scModalOverlay");
    var iframe = document.getElementById("scModalIframe");
    if (!overlay || !iframe) return;

    var leadsUrl = iframe.getAttribute("data-leads-url");
    if (!leadsUrl) return;
    if (!iframe.src || iframe.src === window.location.href) {
      iframe.src = leadsUrl;
      iframe.onload = function () {
        try {
          var doc = iframe.contentDocument || iframe.contentWindow.document;
          var s = doc.createElement("style");
          s.textContent =
            "body { font-family: 'Montserrat', system-ui, sans-serif !important; background: #fff !important; }" +
            "h1, h2, h3 { font-family: 'Montserrat', system-ui, sans-serif !important; font-size: 26px !important; font-weight: 800 !important; color: #001a4a !important; text-align: center !important; letter-spacing: -0.01em !important; margin-bottom: 6px !important; }" +
            "h1::after { content: ''; display: block; width: 40px; height: 3px; background: #00cfa7; border-radius: 2px; margin: 8px auto 0 !important; }" +
            ".container, .container-fluid { max-width: 560px !important; padding: 2rem 2.5rem !important; }" +
            "label { font-size: 12px !important; font-weight: 600 !important; color: #4a5a7a !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; margin-bottom: 5px !important; }" +
            "input[type='text'], input[type='email'], input[type='tel'], input[type='number'], textarea, select { border: 1.5px solid #dde6f5 !important; border-radius: 8px !important; padding: 10px 14px !important; font-size: 14px !important; font-family: 'Montserrat', system-ui, sans-serif !important; color: #001a4a !important; background: #f8faff !important; width: 100% !important; box-sizing: border-box !important; }" +
            "input:focus, textarea:focus, select:focus { border-color: #00cfa7 !important; box-shadow: 0 0 0 3px rgba(0,207,167,0.12) !important; outline: none !important; background: #fff !important; }" +
            "input[type='submit'], button[type='submit'] { background: #00cfa7 !important; color: #001a4a !important; font-family: 'Montserrat', system-ui, sans-serif !important; font-size: 15px !important; font-weight: 800 !important; border: none !important; border-bottom: 3px solid #009e7e !important; border-radius: 10px !important; padding: 14px 32px !important; width: 100% !important; cursor: pointer !important; }";
          doc.head.appendChild(s);
        } catch (e) { /* cross-origin */ }
      };
    }
    overlay.classList.add("open");
    document.body.style.overflow = "hidden";
  };

  window.scModalClose = function () {
    var overlay = document.getElementById("scModalOverlay");
    if (overlay) overlay.classList.remove("open");
    document.body.style.overflow = "";
  };

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") window.scModalClose();
  });
})();
