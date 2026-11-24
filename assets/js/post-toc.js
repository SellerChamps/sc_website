/* Blog post sidebar: Jump to section */
(function () {
  "use strict";

  var postContent = document.getElementById("post-content");
  var postToc = document.getElementById("post-toc");
  var postTocList = document.getElementById("post-toc-list");
  if (!postContent || !postToc || !postTocList) return;

  var h2s = postContent.querySelectorAll("h2");
  var headings = h2s.length > 0 ? h2s : postContent.querySelectorAll("h3");
  var tocMaxItems = 12;
  var usedIds = Object.create(null);
  var skipWithin = ".pseo-faq, .pseo-tldr, .post-demo-banner, .post-demo-banner-wrap";

  function slugify(text) {
    return text
      .trim()
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, "")
      .replace(/\s+/g, "-")
      .replace(/-+/g, "-")
      .replace(/^-|-$/g, "");
  }

  function uniqueId(base) {
    var id = base || "section";
    var n = 2;
    while (usedIds[id]) {
      id = base + "-" + n;
      n += 1;
    }
    usedIds[id] = true;
    return id;
  }

  function shouldSkipHeading(el) {
    return el.closest(skipWithin) != null;
  }

  function isCtaHeading(label) {
    return /try sellerchamp|request a sellerchamp demo|request sellerchamp demo/i.test(label);
  }

  for (var h = 0; h < headings.length && postTocList.children.length < tocMaxItems; h++) {
    var heading = headings[h];
    if (shouldSkipHeading(heading)) continue;
    var label = (heading.textContent || "").replace(/\s+/g, " ").trim();
    if (!label || isCtaHeading(label)) continue;
    var baseId = slugify(label);
    var id = heading.id;
    if (!id) {
      id = uniqueId(baseId);
      heading.id = id;
    } else {
      usedIds[id] = true;
    }

    var li = document.createElement("li");
    var a = document.createElement("a");
    a.href = "#" + id;
    a.textContent = label;
    li.appendChild(a);
    postTocList.appendChild(li);
  }

  if (postTocList.children.length > 0) {
    postToc.hidden = false;
  }
})();