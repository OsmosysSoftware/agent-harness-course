/* Agent Harness course: shared behaviour.
   Cabinet of plaques (course map), theme toggle (light by default), quizzes with a streak, "Done when" lists that
   pass a stage and award its plaque, step-through diagrams, and the context-tray demo.
   Storage is per browser and optional: every page works without it. */
(function () {
  var KEY = "harness-course:";
  function get(k) { try { return localStorage.getItem(KEY + k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(KEY + k, v); } catch (e) {} }

  // Course map: file, title, plaque name, icon.
  var ICON = {
    loop: '<path d="M4 12a8 8 0 0 1 13.7-5.6M20 12a8 8 0 0 1-13.7 5.6"/><path d="M17 3v4h-4M7 21v-4h4"/>',
    doc: '<path d="M7 3h8l4 4v14H7z"/><path d="M15 3v4h4M10 12h6M10 16h6"/>',
    sign: '<path d="M12 3v18"/><path d="M5 6h11l3 2.5L16 11H5z"/><path d="M19 13H8l-3 2.5L8 18h11z"/>',
    map: '<path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z"/><path d="M9 4v14M15 6v14"/>',
    wrench: '<path d="M14.5 6.5a4 4 0 0 0-5.3 5.2L4 17l3 3 5.3-5.2a4 4 0 0 0 5.2-5.3l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    lens: '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/>',
    shield: '<path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    plug: '<path d="M9 3v5M15 3v5M7 8h10v3a5 5 0 0 1-10 0z"/><path d="M12 16v5"/>',
    quill: '<path d="M20 4c-6 1-11 6-13 13l-2 3"/><path d="M20 4c-1 6-5 10-11 11"/>',
    ledger: '<path d="M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z"/><path d="M5 17a3 3 0 0 1 3-3h11M9 8h6"/>',
    trophy: '<path d="M8 4h8v5a4 4 0 0 1-8 0z"/><path d="M8 6H5a3 3 0 0 0 3 4M16 6h3a3 3 0 0 1-3 4M12 13v4M9 21h6M10 17h4v4h-4z"/>'
  };
  var LESSONS = [
    ["0001-how-an-agent-works.html", "How an agent works", "Loop Reader", "loop"],
    ["0002-rules-files.html", "Rules files", "Rule Writer", "doc"],
    ["0003-one-three-one.html", "1-3-1 when stuck", "Clean Hand-over", "sign"],
    ["0004-plan-gated-workflow.html", "Plan-gated workflow", "Plan Gatekeeper", "map"],
    ["0005-skills.html", "Skills", "Skill Smith", "wrench"],
    ["0006-reviewer-subagents.html", "Reviewer subagents", "Second Opinion", "lens"],
    ["0007-guards.html", "Guards", "Guard Builder", "shield"],
    ["0008-mcp.html", "MCP", "Live Docs", "plug"],
    ["0009-writing-for-the-agent.html", "Writing for the agent", "Agent's Author", "quill"],
    ["0010-evidence-and-honesty.html", "Evidence and honesty", "Honest Log", "ledger"],
    ["0011-capstone.html", "Capstone", "Harness Ready", "trophy"]
  ];
  function icon(name) { return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICON[name] + "</svg>"; }
  function lessonId(i) { return ("000" + (i + 1)).slice(-4); }
  function passed(id) { return get("passed:" + id) === "1"; }
  function count() { var n = 0; LESSONS.forEach(function (l, i) { if (passed(lessonId(i))) n++; }); return n; }
  function meter(n) { return "<b>" + n + "</b> of 11 plaques"; }

  var root = document.documentElement;
  if (get("theme") === "dark") root.setAttribute("data-theme", "dark");

  document.addEventListener("DOMContentLoaded", function () {
    var lesson = document.body.getAttribute("data-lesson");
    if (lesson) set("last", lesson);
    buildCabinet();
    initQuizzes();
    initChecklists();
    initDiagrams();
    initTrays();
    initToc();
    initCopy();
  });

  // ---- Cabinet: brand, a plaque per lesson, a tape flag where you stopped, progress, theme ----
  function base() { return /\/(lessons|reference)\//.test(location.pathname) ? "../" : ""; }
  function flagId() {
    // The flag marks the first lesson you haven't passed yet (where to pick up).
    for (var i = 0; i < LESSONS.length; i++) if (!passed(lessonId(i))) return lessonId(i);
    return null;
  }
  function paintShelf(shelf) {
    var current = document.body.getAttribute("data-lesson"), flag = flagId();
    shelf.querySelectorAll("a").forEach(function (a, i) {
      var id = lessonId(i), p = passed(id);
      a.className = (p ? "passed" : "") + (id === current ? " current" : "") + (id === flag ? " flag" : "");
      a.innerHTML = p ? icon(LESSONS[i][3]) : String(i + 1);
      a.title = (i + 1) + ". " + LESSONS[i][1] + (p ? " · plaque: " + LESSONS[i][2] : "") + (id === flag ? " · pick up here" : "");
    });
  }
  function buildCabinet() {
    var b = base(), current = document.body.getAttribute("data-lesson");
    var bar = document.createElement("header");
    bar.className = "cabinet";
    var html = '<a class="brand" href="' + b + 'index.html">Agent Harness</a><nav class="shelf" aria-label="Course lessons">';
    LESSONS.forEach(function (l, i) {
      html += '<a href="' + b + "lessons/" + l[0] + '"' + (lessonId(i) === current ? ' aria-current="page"' : "") + "></a>";
    });
    html += '</nav><span class="meter">' + meter(count()) + "</span>";
    bar.innerHTML = html;
    var btn = document.createElement("button");
    btn.className = "theme-toggle";
    btn.type = "button";
    function label() { btn.textContent = root.getAttribute("data-theme") === "dark" ? "Light" : "Dark"; }
    label();
    btn.addEventListener("click", function () {
      var dark = root.getAttribute("data-theme") === "dark";
      if (dark) root.removeAttribute("data-theme"); else root.setAttribute("data-theme", "dark");
      set("theme", dark ? "light" : "dark");
      label();
    });
    bar.appendChild(btn);
    document.body.insertBefore(bar, document.body.firstChild);
    paintShelf(bar.querySelector(".shelf"));
    var cur = bar.querySelector(".shelf a.current");
    if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: "nearest", inline: "center" });
  }
  function refreshCabinet() {
    var shelf = document.querySelector(".cabinet .shelf");
    if (shelf) paintShelf(shelf);
    var m = document.querySelector(".cabinet .meter");
    if (m) m.innerHTML = meter(count());
  }

  // ---- Quizzes: shuffled options with letter keys, first-try streak across the course ----
  function shuffle(list) {
    for (var i = list.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      list[i].parentNode.insertBefore(list[j], list[i]);
      var t = list[i]; list[i] = list[j]; list[j] = t;
    }
  }
  function relabel(quiz) {
    quiz.querySelectorAll("button.opt").forEach(function (o, i) {
      var k = o.querySelector(".key");
      if (!k) { k = document.createElement("span"); k.className = "key"; o.insertBefore(k, o.firstChild); }
      k.textContent = "ABCDEF"[i];
    });
  }
  function initQuizzes() {
    var quizzes = Array.prototype.slice.call(document.querySelectorAll(".quiz"));
    if (!quizzes.length) return;
    var firstTry = {};
    quizzes.forEach(function (quiz, qi) {
      var opts = Array.prototype.slice.call(quiz.querySelectorAll("button.opt"));
      opts.forEach(function (b) { b.type = "button"; });
      shuffle(opts.slice());
      relabel(quiz);
      var retry = document.createElement("button");
      retry.className = "btn retry";
      retry.type = "button";
      retry.textContent = "Try again";
      quiz.appendChild(retry);
      opts.forEach(function (b) {
        b.addEventListener("click", function () {
          var ok = b.hasAttribute("data-correct");
          if (!(qi in firstTry)) {
            firstTry[qi] = ok;
            var s = ok ? parseInt(get("streak") || "0", 10) + 1 : 0;
            set("streak", String(s));
          }
          quiz.querySelectorAll("button.opt").forEach(function (o) {
            o.disabled = true;
            if (o.hasAttribute("data-correct")) o.classList.add("right");
          });
          if (!ok) { b.classList.add("wrong"); quiz.classList.add("missed"); }
          quiz.classList.add("answered");
          report();
        });
      });
      retry.addEventListener("click", function () {
        quiz.classList.remove("answered", "missed");
        var cur = Array.prototype.slice.call(quiz.querySelectorAll("button.opt"));
        cur.forEach(function (o) { o.disabled = false; o.classList.remove("right", "wrong"); });
        shuffle(cur);
        relabel(quiz);
      });
    });
    function report() {
      var answered = Object.keys(firstTry).length;
      var right = Object.keys(firstTry).filter(function (k) { return firstTry[k]; }).length;
      document.querySelectorAll(".score").forEach(function (s) {
        s.innerHTML = right + " of " + quizzes.length + " right first time" +
          (answered < quizzes.length ? " · " + (quizzes.length - answered) + " to go" : "") +
          ' · <span class="streak">streak ' + (get("streak") || "0") + "</span>";
      });
    }
  }

  // ---- "Done when": all ticked passes the stage and shows its plaque card ----
  function initChecklists() {
    var lesson = document.body.getAttribute("data-lesson");
    document.querySelectorAll("ul.check[data-key]").forEach(function (ul) {
      var key = "check:" + ul.getAttribute("data-key");
      var state = {};
      try { state = JSON.parse(get(key) || "{}"); } catch (e) {}
      var boxes = ul.querySelectorAll("input[type=checkbox]");
      var panel = ul.closest(".done");
      var award = null, idx = lesson ? parseInt(lesson, 10) - 1 : -1;
      if (panel && LESSONS[idx]) {
        var next = LESSONS[idx + 1];
        award = document.createElement("div");
        award.className = "award";
        award.setAttribute("role", "status");
        award.innerHTML = '<div class="plaque">' + icon(LESSONS[idx][3]) + "</div><div>" +
          '<span class="kick">Stage ' + (idx + 1) + " of 11 passed</span>" +
          "<h3>" + LESSONS[idx][2] + "</h3>" +
          (panel.getAttribute("data-built") ? '<p class="built">You built: ' + panel.getAttribute("data-built") + "</p>" : "") +
          '<p class="when"></p>' +
          (next ? '<a class="btn" href="' + next[0] + '">Next: ' + next[1] + " →</a>" : '<a class="btn" href="../index.html">See your cabinet →</a>') +
          "</div>";
        panel.appendChild(award);
      }
      function sync(animate) {
        var all = boxes.length > 0 && Array.prototype.every.call(boxes, function (b) { return b.checked; });
        if (!panel || !lesson) return;
        var was = passed(lesson);
        panel.classList.toggle("complete", all);
        set("passed:" + lesson, all ? "1" : "0");
        if (all && !was) set("when:" + lesson, new Date().toISOString().slice(0, 10));
        if (award) {
          award.querySelector(".plaque").style.animation = animate ? "" : "none";
          var when = get("when:" + lesson);
          award.querySelector(".when").textContent = when ? "Earned " + when + ". Saved in this browser." : "";
        }
        document.querySelectorAll(".badge-chip").forEach(function (c) { c.classList.toggle("earned", all); });
        refreshCabinet();
      }
      boxes.forEach(function (cb, i) {
        cb.checked = !!state[i];
        cb.addEventListener("change", function () {
          state[i] = cb.checked;
          set(key, JSON.stringify(state));
          sync(true);
        });
      });
      sync(false);
    });
  }

  // ---- Step-through diagrams: <figure class="diagram" data-steps='[{"cls":"s1","text":"..."}]'> ----
  function initDiagrams() {
    document.querySelectorAll("figure.diagram[data-steps]").forEach(function (fig) {
      var steps;
      try { steps = JSON.parse(fig.getAttribute("data-steps")); } catch (e) { return; }
      var svg = fig.querySelector("svg");
      var bar = document.createElement("div");
      bar.className = "bar";
      bar.innerHTML = '<button class="btn" type="button" data-act="play">Pause</button>' +
        '<button class="btn" type="button" data-act="prev">Back</button>' +
        '<button class="btn primary" type="button" data-act="next">Next</button>' +
        '<div class="caption" aria-live="polite"></div><div class="dots"></div>';
      fig.appendChild(bar);
      var cap = bar.querySelector(".caption"), dots = bar.querySelector(".dots");
      var prev = bar.querySelector('[data-act="prev"]'), next = bar.querySelector('[data-act="next"]');
      steps.forEach(function () { dots.appendChild(document.createElement("span")); });
      var at = -1, intro = fig.getAttribute("data-intro") || "Press Step through.";
      function show() {
        svg.querySelectorAll(".on").forEach(function (g) { g.classList.remove("on"); });
        fig.classList.toggle("stepping", at >= 0);
        if (at >= 0) svg.querySelectorAll("." + steps[at].cls).forEach(function (g) { g.classList.add("on"); });
        cap.innerHTML = at >= 0 ? "<b>Step " + (at + 1) + " of " + steps.length + ".</b> " + steps[at].text : intro;
        dots.querySelectorAll("span").forEach(function (d, i) { d.classList.toggle("on", i === at); });
        prev.disabled = at <= 0;
        next.textContent = at === steps.length - 1 ? "Start again" : "Next";
      }
      // Autoplay: advance every few seconds while visible; any manual control stops it.
      var play = bar.querySelector('[data-act="play"]'), timer = null, visible = false;
      var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
      var auto = !reduce && fig.getAttribute("data-autoplay") !== "off";
      function tick() { at = at >= steps.length - 1 ? 0 : at + 1; show(); }
      function start() { if (!timer && auto && visible) { if (at < 0) tick(); timer = setInterval(tick, 3800); } play.textContent = "Pause"; }
      function stop() { clearInterval(timer); timer = null; play.textContent = "Play"; }
      function manual() { auto = false; stop(); }
      play.addEventListener("click", function () { if (timer) manual(); else { auto = true; start(); } });
      next.addEventListener("click", function () { manual(); at = at === steps.length - 1 ? -1 : at + 1; show(); });
      prev.addEventListener("click", function () { manual(); if (at > 0) { at--; show(); } });
      fig.addEventListener("mouseenter", function () { if (timer) { clearInterval(timer); timer = null; } });
      fig.addEventListener("mouseleave", function () { if (auto) start(); });
      show();
      if (!auto) play.textContent = "Play";
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (es) {
          visible = es[0].isIntersecting;
          if (visible) start(); else if (timer) { clearInterval(timer); timer = null; }
        }, { threshold: 0.5 }).observe(fig);
      }
    });
  }

  // ---- Context tray: watch the window fill, auto-compact, and clear ----
  // Card kinds: pin (rules file, survives), sys (startup), chat (your messages), file (tool results), rule (a chat-only rule), sum (summary)
  function initTrays() {
    document.querySelectorAll(".tray[data-tray]").forEach(function (tray) {
      var CAP = 12;
      var START = [["pin", "AGENTS.md", "your rules file"], ["sys", "System + tools", "loaded first"]];
      var WORK = [
        ["rule", "You: “end answers with STOCK-OK”", "a rule typed in chat"],
        ["file", "Read OrderService.cs", "tool result"], ["chat", "You: add low-stock endpoint", "message"],
        ["file", "dotnet test output", "tool result"], ["file", "Read ProductsController.cs", "tool result"],
        ["chat", "You: also filter by SKU", "message"], ["file", "git diff", "tool result"],
        ["file", "Read StockDbContext.cs", "tool result"], ["chat", "You: run the tests again", "message"],
        ["file", "dotnet build output", "tool result"]
      ];
      var stack = tray.querySelector(".stack"), fill = tray.querySelector(".fill i"), pct = tray.querySelector(".fill b");
      var say = tray.querySelector(".say"), bWork = tray.querySelector('[data-act="work"]');
      var bCompact = tray.querySelector('[data-act="compact"]'), bClear = tray.querySelector('[data-act="clear"]');
      var cards = [], w = 0;
      function render(flash) {
        stack.innerHTML = "";
        cards.forEach(function (c) {
          var el = document.createElement("div");
          el.className = "card " + c[0] + (flash && flash.indexOf(c) > -1 ? " pop" : "");
          el.innerHTML = "<b>" + c[1] + "</b><span>" + c[2] + "</span>";
          stack.appendChild(el);
        });
        var used = Math.min(100, Math.round(cards.length / CAP * 100));
        fill.style.width = used + "%";
        fill.className = used >= 90 ? "hot" : "";
        pct.textContent = used + "% full";
        bCompact.disabled = cards.length <= START.length + 1;
      }
      function reset(msg) {
        cards = START.map(function (c) { return c; }); w = 0;
        say.innerHTML = msg;
        render(cards);
      }
      bWork.addEventListener("click", function () {
        var added = [];
        for (var k = 0; k < 3 && w < WORK.length; k++, w++) { cards.push(WORK[w]); added.push(WORK[w]); }
        if (cards.length >= CAP - 1) {
          say.innerHTML = "<b>Almost full.</b> Claude Code will compact on its own soon. Press <b>Compact</b> to see what that does.";
        } else {
          say.innerHTML = w <= 3 ? "Every message and every tool result lands in the window. Note your chat rule, <b>STOCK-OK</b>, sitting with everything else."
                                 : "File reads fill it fastest. The window keeps growing with each turn.";
        }
        if (w >= WORK.length) bWork.disabled = true;
        render(added);
      });
      bCompact.addEventListener("click", function () {
        var summary = ["sum", "Summary of earlier work", "short; STOCK-OK may or may not be in it"];
        cards = START.concat([summary]);
        say.innerHTML = "<b>Compacted.</b> The conversation became one short summary. Your chat rule <b>might</b> survive in it, or might not: you can't rely on it. <b>AGENTS.md was re-read from disk</b>, so every rule in it is back, word for word.";
        bWork.disabled = false; w = Math.min(w, WORK.length);
        render(cards.slice(0, 1).concat([summary]));
      });
      bClear.addEventListener("click", function () {
        bWork.disabled = false;
        reset("<b>Cleared.</b> A fresh window: only the startup cards. Your rules file loads again; nothing from the chat survives. Use <code>/clear</code> between unrelated tasks.");
      });
      reset(tray.getAttribute("data-intro") || "This is a fresh session. Press <b>Keep working</b>.");
    });
  }

  // ---- Course index: plaques earned ----
  function initToc() {
    document.querySelectorAll(".toc li[data-lesson]").forEach(function (li) {
      var id = li.getAttribute("data-lesson"), idx = parseInt(id, 10) - 1;
      var st = li.querySelector(".st");
      if (passed(id) && LESSONS[idx]) {
        li.classList.add("passed");
        var n = li.querySelector(".n");
        if (n) n.innerHTML = icon(LESSONS[idx][3]);
        if (st) st.textContent = "Plaque: " + LESSONS[idx][2];
      }
    });
  }

  // ---- Copy buttons on every code block ----
  function initCopy() {
    document.querySelectorAll("pre").forEach(function (pre) {
      if (pre.closest(".diagram") || pre.querySelector(".copy")) return;
      var btn = document.createElement("button");
      btn.className = "copy";
      btn.type = "button";
      btn.textContent = "Copy";
      btn.setAttribute("aria-label", "Copy this code");
      btn.addEventListener("click", function () {
        var clone = pre.cloneNode(true), b2 = clone.querySelector(".copy");
        if (b2) b2.remove();
        var text = clone.textContent.replace(/\s+$/, "");
        function done(ok) {
          btn.textContent = ok ? "Copied" : "Press Ctrl+C";
          setTimeout(function () { btn.textContent = "Copy"; }, 1600);
        }
        if (navigator.clipboard && window.isSecureContext) {
          navigator.clipboard.writeText(text).then(function () { done(true); }, function () { done(false); });
        } else {
          var t = document.createElement("textarea");
          t.value = text; t.style.position = "fixed"; t.style.opacity = "0";
          document.body.appendChild(t); t.select();
          var ok = false; try { ok = document.execCommand("copy"); } catch (e) {}
          document.body.removeChild(t); done(ok);
        }
      });
      pre.appendChild(btn);
    });
  }
})();
