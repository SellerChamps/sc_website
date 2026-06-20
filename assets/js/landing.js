/* SellerChamp Lister landing — interactions */
(function () {
  "use strict";

  // ── Pricing: monthly / annual toggle ──────────────────────
  var toggle = document.querySelector("[data-price-toggle]");
  if (toggle) {
    var labelM = document.querySelector("[data-label-monthly]");
    var labelA = document.querySelector("[data-label-annual]");
    var prices = document.querySelectorAll("[data-monthly]");

    function render(annual) {
      toggle.setAttribute("aria-checked", annual ? "true" : "false");
      if (labelM) labelM.classList.toggle("on", !annual);
      if (labelA) labelA.classList.toggle("on", annual);
      prices.forEach(function (el) {
        var m = parseInt(el.getAttribute("data-monthly"), 10);
        if (isNaN(m)) return;
        var annualMo = parseInt(el.getAttribute("data-annual-mo"), 10);
        var shown = annual && !isNaN(annualMo) ? annualMo : m;
        var num = el.querySelector(".price-num");
        if (num) num.textContent = "$" + shown;
        var bill = el.querySelector("[data-bill]");
        if (bill) {
          bill.textContent = annual
            ? "Billed annually · $" + (shown * 12) + "/yr"
            : "Billed monthly";
        }
      });
    }

    toggle.addEventListener("click", function () {
      render(toggle.getAttribute("aria-checked") !== "true");
    });
    render(false);
  }

  // ── Mobile nav ────────────────────────────────────────────
  var nav = document.querySelector(".nav");
  var navToggle = document.querySelector("[data-nav-toggle]");
  var navLinks = document.getElementById("nav-links");

  function setNavOpen(open) {
    if (!nav || !navToggle) return;
    nav.classList.toggle("nav--open", open);
    navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    navToggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }

  if (navToggle && navLinks && nav) {
    navToggle.addEventListener("click", function () {
      setNavOpen(!nav.classList.contains("nav--open"));
    });

    navLinks.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setNavOpen(false);
      });
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setNavOpen(false);
    });

    document.addEventListener("click", function (e) {
      if (!nav.classList.contains("nav--open")) return;
      if (!nav.contains(e.target)) setNavOpen(false);
    });
  }

  // ── Click-to-play video frames ────────────────────────────
  function playVideoFrame(frame) {
    if (frame.classList.contains("is-playing")) return;

    var embed = frame.querySelector(".embed");
    var poster = frame.querySelector(".video-frame__poster");
    if (!embed || !poster) return;

    var mp4 = frame.getAttribute("data-video-src");
    var ytId = frame.getAttribute("data-youtube-id");

    if (mp4) {
      var video = document.createElement("video");
      video.controls = true;
      video.playsInline = true;
      video.preload = "auto";
      video.setAttribute("aria-label", "Demo video");
      video.src = mp4;

      embed.appendChild(video);
      video.play().catch(function () {});
    } else if (ytId) {
      var iframe = document.createElement("iframe");
      iframe.src = "https://www.youtube.com/embed/" + ytId + "?autoplay=1&rel=0";
      iframe.title = "SellerChamp overview";
      iframe.allow =
        "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      iframe.allowFullscreen = true;
      embed.appendChild(iframe);
    }

    poster.classList.add("is-hidden");
    frame.classList.add("is-playing");
  }

  document.querySelectorAll(".video-frame--click").forEach(function (frame) {
    frame.addEventListener("click", function (e) {
      if (e.target.closest("video, iframe")) return;
      playVideoFrame(frame);
    });
  });

  // ── Hero scan visual — click play to load demo video ─────
  var heroWrap = document.getElementById("heroScanVideo");
  var heroPoster = document.getElementById("heroScanPoster");
  if (heroWrap && heroPoster) {
    var heroScanVideoSrc =
      "https://p62.p2.n0.cdn.zight.com/items/eDuOJXrO/cf0ca4bb-1d97-4f08-bc6b-39e14de11ef8.mp4?v=cc2b70c0bf8b6218590ee06abd40dea6";

    function playHeroScanVideo() {
      if (heroPoster.classList.contains("hidden")) return;

      var video = document.createElement("video");
      video.controls = true;
      video.playsInline = true;
      video.preload = "metadata";
      video.setAttribute("aria-label", "Quick item scan demo");

      var source = document.createElement("source");
      source.src = heroScanVideoSrc;
      source.type = "video/mp4";
      video.appendChild(source);

      heroWrap.appendChild(video);
      heroPoster.classList.add("hidden");
      heroWrap.classList.remove("hero-scan-video");
      heroWrap.style.cursor = "default";
      video.play().catch(function () {});
    }

    heroWrap.addEventListener("click", function (e) {
      if (e.target.closest("video")) return;
      playHeroScanVideo();
    });
  }
})();
