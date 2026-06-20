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
})();
