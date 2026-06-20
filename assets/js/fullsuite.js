/* SellerChamp Full Suite landing — testimonial carousel */
(function () {
  "use strict";

  var carousel = document.getElementById("testiCarousel");
  if (!carousel) return;

  var slides = carousel.querySelectorAll(".testi-slide");
  var dots = document.querySelectorAll("#testiDots .testi-dot");
  var total = slides.length;
  var current = 0;
  var timer = null;
  var ROTATE_MS = 7000;

  function show(idx) {
    slides[current].classList.remove("active");
    if (dots[current]) dots[current].classList.remove("active");
    current = (idx + total) % total;
    slides[current].classList.add("active");
    if (dots[current]) dots[current].classList.add("active");
  }

  function start() {
    stop();
    timer = setInterval(function () {
      show(current + 1);
    }, ROTATE_MS);
  }

  function stop() {
    if (timer) {
      clearInterval(timer);
      timer = null;
    }
  }

  dots.forEach(function (dot) {
    dot.addEventListener("click", function () {
      show(parseInt(dot.getAttribute("data-slide"), 10));
      start();
    });
  });

  var prevBtn = document.getElementById("testiPrev");
  var nextBtn = document.getElementById("testiNext");
  if (prevBtn) {
    prevBtn.addEventListener("click", function () {
      show(current - 1);
      start();
    });
  }
  if (nextBtn) {
    nextBtn.addEventListener("click", function () {
      show(current + 1);
      start();
    });
  }

  carousel.addEventListener("mouseenter", stop);
  carousel.addEventListener("mouseleave", start);

  start();
})();
