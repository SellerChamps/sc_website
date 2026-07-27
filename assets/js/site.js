/* Site chrome + motion */
(function () {
  "use strict";

  var nav = document.querySelector(".site-nav");
  var toggle = document.querySelector(".nav-toggle");
  if (nav && toggle) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });

    nav.querySelectorAll(".nav-links a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
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
})();
