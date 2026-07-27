/* Site chrome + motion */
(function () {
  "use strict";

  var nav = document.querySelector(".site-nav");
  var toggle = document.querySelector(".nav-toggle");

  function closeNavDropdowns(exceptItem) {
    if (!nav) return;
    nav.querySelectorAll(".nav-item.has-dropdown.is-open").forEach(function (item) {
      if (exceptItem && item === exceptItem) return;
      item.classList.remove("is-open");
      var btn = item.querySelector(".nav-dropdown-toggle");
      if (btn) btn.setAttribute("aria-expanded", "false");
    });
  }

  function closeMobileNav() {
    if (!nav || !toggle) return;
    nav.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open menu");
    closeNavDropdowns();
  }

  if (nav && toggle) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      if (!open) closeNavDropdowns();
    });

    nav.querySelectorAll(".nav-links a").forEach(function (link) {
      link.addEventListener("click", function () {
        closeMobileNav();
      });
    });
  }

  if (nav) {
    nav.querySelectorAll(".nav-dropdown-toggle").forEach(function (btn) {
      btn.addEventListener("click", function (event) {
        event.preventDefault();
        event.stopPropagation();
        var item = btn.closest(".nav-item.has-dropdown");
        if (!item) return;
        var willOpen = !item.classList.contains("is-open");
        closeNavDropdowns(willOpen ? item : null);
        item.classList.toggle("is-open", willOpen);
        btn.setAttribute("aria-expanded", willOpen ? "true" : "false");
      });
    });

    document.addEventListener("click", function (event) {
      if (!nav.contains(event.target)) closeNavDropdowns();
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        closeNavDropdowns();
        if (nav.classList.contains("is-open")) closeMobileNav();
      }
    });
  }

  /* Pause runway when off-screen (saves work; respects reduced-motion via CSS) */
  var runway = document.querySelector(".channel-runway-track");
  if (runway && "IntersectionObserver" in window) {
    var wrap = document.querySelector(".channel-runway");
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          runway.style.animationPlayState = entry.isIntersecting ? "running" : "paused";
        });
      },
      { threshold: 0.05 }
    );
    if (wrap) io.observe(wrap);
  }

  /* Home hero heading/subheading rotator — random pick, held ~30s */
  var rotator = document.querySelector("[data-hero-rotator]");
  if (rotator) {
    var copy = rotator.querySelector("[data-hero-copy]");
    var variants = Array.prototype.slice.call(
      rotator.querySelectorAll("template[data-hero-variant]")
    );
    var reduceMotion =
      window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (copy && variants.length) {
      var index = Math.floor(Math.random() * variants.length);
      var interval = parseInt(rotator.getAttribute("data-interval"), 10) || 30000;
      var transitioning = false;

      copy.innerHTML = variants[index].innerHTML;

      if (variants.length > 1 && !reduceMotion) {
        function syncHeight() {
          var width = copy.offsetWidth || rotator.clientWidth;
          var probe = document.createElement("div");
          probe.style.cssText =
            "position:absolute;visibility:hidden;pointer-events:none;width:" +
            width +
            "px;";
          rotator.appendChild(probe);
          var max = copy.scrollHeight;
          variants.forEach(function (tpl) {
            probe.innerHTML = tpl.innerHTML;
            var h = probe.scrollHeight;
            if (h > max) max = h;
          });
          rotator.removeChild(probe);
          if (max) rotator.style.minHeight = max + "px";
        }

        syncHeight();
        window.addEventListener("resize", syncHeight);

        function randomOtherIndex() {
          if (variants.length === 2) return index === 0 ? 1 : 0;
          var next = index;
          while (next === index) {
            next = Math.floor(Math.random() * variants.length);
          }
          return next;
        }

        function showVariant(nextIndex) {
          if (transitioning || nextIndex === index) return;
          transitioning = true;
          copy.classList.add("is-fading");

          window.setTimeout(function () {
            copy.innerHTML = variants[nextIndex].innerHTML;
            void copy.offsetWidth;
            copy.classList.remove("is-fading");
            index = nextIndex;
            transitioning = false;
          }, 450);
        }

        window.setInterval(function () {
          showVariant(randomOtherIndex());
        }, interval);
      }
    }
  }

  /* Replace legacy Elementor demo CTAs with the clickable banner */
  var bannerTpl = document.getElementById("post-demo-banner-template");
  var postBody = document.querySelector(".post-body");
  if (bannerTpl && postBody) {
    var ctaHeadingRe =
      /try sellerchamp for yourself|request a sellerchamp demo|request sellerchamp demo|ready to stop managing spreadsheets|tired of manual work|want to manage your listings|build profitable inventory|ready to make the most|try sellerchamp demo/i;
    var demoBtnRe = /schedule your demo today|request a demo|book your|book a demo/i;

    function cloneBanner() {
      return bannerTpl.content.firstElementChild.cloneNode(true);
    }

    function isElementor(el) {
      return el && el.classList && el.classList.contains("elementor-element");
    }

    function findCtaBlock(start) {
      var node = start;
      var best = null;
      for (var i = 0; i < 10 && node && node !== postBody; i++) {
        if (isElementor(node)) {
          var text = node.textContent || "";
          var hasDemoCta = demoBtnRe.test(text) || node.querySelector('a[href*="leads/new"], a[href*="sign_up"]');
          if (hasDemoCta) {
            best = node;
            var settings = node.getAttribute("data-settings") || "";
            if (settings.indexOf("gradient") !== -1 || settings.indexOf("background_background") !== -1) {
              return node;
            }
            if (node.querySelector("h5.elementor-heading-title, h2, h3") && node.querySelector(".elementor-button, a[href*='leads']")) {
              return node;
            }
          }
        }
        node = node.parentElement;
      }
      return best;
    }

    function removePrecedingCtaHeading(block) {
      var prev = block.previousElementSibling;
      while (prev && prev.nodeType === 1) {
        var text = (prev.textContent || "").replace(/\s+/g, " ").trim();
        if (!text) {
          var empty = prev;
          prev = prev.previousElementSibling;
          empty.parentNode.removeChild(empty);
          continue;
        }
        if (ctaHeadingRe.test(text) && text.length < 180 && !demoBtnRe.test(text)) {
          prev.parentNode.removeChild(prev);
        }
        break;
      }
    }

    var replaced = 0;
    var seen = [];

    function replaceBlock(block) {
      if (!block || !block.parentNode || seen.indexOf(block) !== -1) return;
      // Skip if this block is inside another already-queued block
      for (var i = 0; i < seen.length; i++) {
        if (seen[i].contains && seen[i].contains(block)) return;
      }
      seen.push(block);
      removePrecedingCtaHeading(block);
      var banner = cloneBanner();
      block.parentNode.insertBefore(banner, block);
      block.parentNode.removeChild(block);
      replaced += 1;
    }

    postBody.querySelectorAll("h5.elementor-heading-title, h2, h3").forEach(function (heading) {
      var text = heading.textContent || "";
      if (!ctaHeadingRe.test(text)) return;
      replaceBlock(findCtaBlock(heading));
    });

    // Catch gradient CTA boxes that use odd headings / white text
    postBody.querySelectorAll(".elementor-element").forEach(function (el) {
      var settings = el.getAttribute("data-settings") || "";
      if (settings.indexOf("gradient") === -1) return;
      var text = el.textContent || "";
      if (!demoBtnRe.test(text) && !/request a sellerchamp demo today/i.test(text)) return;
      replaceBlock(el);
    });

    // Remove leftover orphan demo heading blocks
    postBody.querySelectorAll(".elementor-element").forEach(function (el) {
      if (!el.parentNode) return;
      var text = (el.textContent || "").replace(/\s+/g, " ").trim();
      if (text.length > 160) return;
      if (!ctaHeadingRe.test(text)) return;
      if (el.querySelector(".post-demo-banner")) return;
      if (demoBtnRe.test(text)) return;
      el.parentNode.removeChild(el);
    });

    if (!replaced && !postBody.querySelector(".post-demo-banner")) {
      postBody.appendChild(cloneBanner());
    }

    // Never show stacked duplicate banners — keep the last one
    var banners = postBody.querySelectorAll(".post-demo-banner");
    if (banners.length > 1) {
      for (var b = 0; b < banners.length - 1; b++) {
        banners[b].parentNode.removeChild(banners[b]);
      }
    }
  }
})();
