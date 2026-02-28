/* N.E.K.O Plugin SDK Docs - SPA-like Page Transitions */

(function () {
  "use strict";

  var CONTENT_SEL = ".main";
  var TOC_SEL = ".toc-tree";
  var SIDEBAR_SEL = ".sidebar-tree";
  var TRANSITION_MS = 180;
  var cache = {};

  function isInternalLink(link) {
    if (!link || !link.href) return false;
    var href = link.getAttribute("href");
    if (!href || href.startsWith("#") || href.startsWith("javascript")) return false;
    if (link.target === "_blank") return false;
    if (link.origin !== location.origin) return false;
    return true;
  }

  function fetchPage(url) {
    if (cache[url]) return Promise.resolve(cache[url]);
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.text();
    }).then(function (html) {
      var doc = new DOMParser().parseFromString(html, "text/html");
      cache[url] = doc;
      return doc;
    });
  }

  function swapContent(doc, url) {
    // Swap main content
    var newMain = doc.querySelector(CONTENT_SEL);
    var oldMain = document.querySelector(CONTENT_SEL);
    if (newMain && oldMain) {
      oldMain.innerHTML = newMain.innerHTML;
    }

    // Swap right-side TOC
    var newToc = doc.querySelector(TOC_SEL);
    var oldToc = document.querySelector(TOC_SEL);
    if (newToc && oldToc) {
      oldToc.innerHTML = newToc.innerHTML;
    }

    // Update sidebar active state
    var newSidebar = doc.querySelector(SIDEBAR_SEL);
    var oldSidebar = document.querySelector(SIDEBAR_SEL);
    if (newSidebar && oldSidebar) {
      oldSidebar.innerHTML = newSidebar.innerHTML;
    }

    // Update title
    document.title = doc.title;

    // Update URL
    history.pushState(null, doc.title, url);

    // Scroll to top
    window.scrollTo(0, 0);

    // Re-run any scripts that need it (mermaid, etc.)
    reinitPage();
  }

  function reinitPage() {
    // Re-trigger mermaid if present
    if (window.mermaid && window.mermaid.init) {
      try { window.mermaid.init(undefined, ".mermaid"); } catch(e) {}
    }
    // Re-init copy buttons
    var btns = document.querySelectorAll(".copybtn");
    btns.forEach(function(b) { b.dataset.clipboardCopied = ""; });
  }

  function navigateTo(url) {
    var main = document.querySelector(CONTENT_SEL);
    if (!main) { window.location.href = url; return; }

    // Fade out
    main.classList.add("page-transitioning-out");

    fetchPage(url).then(function (doc) {
      setTimeout(function () {
        swapContent(doc, url);
        // Fade in
        main.classList.remove("page-transitioning-out");
        main.classList.add("page-transitioning-in");
        setTimeout(function () {
          main.classList.remove("page-transitioning-in");
        }, TRANSITION_MS);
      }, TRANSITION_MS);
    }).catch(function () {
      // Fallback to normal navigation on error
      window.location.href = url;
    });
  }

  /* ── Click handler ── */
  document.addEventListener("click", function (e) {
    if (e.ctrlKey || e.metaKey || e.shiftKey || e.altKey) return;
    var link = e.target.closest("a[href]");
    if (!isInternalLink(link)) return;

    // Skip if same page anchor
    if (link.pathname === location.pathname) return;

    e.preventDefault();
    navigateTo(link.href);
  });

  /* ── Popstate (back/forward) ── */
  window.addEventListener("popstate", function () {
    navigateTo(location.href);
  });

  /* ── Prefetch on hover ── */
  document.addEventListener("mouseover", function (e) {
    var link = e.target.closest("a[href]");
    if (isInternalLink(link) && !cache[link.href]) {
      fetchPage(link.href);
    }
  });

  /* ── Initial fade-in ── */
  document.body.classList.add("page-loaded");
})();
