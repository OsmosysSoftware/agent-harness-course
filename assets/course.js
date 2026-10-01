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
    initStart();
    initCopy();
    initSpots();
    initWho();
    initCompletion();
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
    html += '</nav><a class="meter" href="' + b + 'completion.html" title="Your completion page">' + meter(count()) + "</a>";
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
          (next ? '<a class="btn" href="' + next[0] + '">Next: ' + next[1] + " →</a>" : '<a class="btn" href="../completion.html">Open your completion page →</a>') +
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
      // Each step stays up long enough to read its caption (about 4 to 9 seconds).
      function wait() { var n = at >= 0 ? cap.textContent.length : 0; return Math.min(9000, Math.max(4000, 2000 + n * 40)); }
      function tick() { at = at >= steps.length - 1 ? 0 : at + 1; show(); timer = setTimeout(tick, wait()); }
      function start() {
        play.textContent = "Pause";
        if (timer || !auto || !visible) return;
        if (at < 0) tick(); else timer = setTimeout(tick, wait());
      }
      function halt() { clearTimeout(timer); timer = null; }
      function stop() { halt(); play.textContent = "Play"; }
      function manual() { auto = false; stop(); }
      play.addEventListener("click", function () { if (auto) manual(); else { auto = true; start(); } });
      next.addEventListener("click", function () { manual(); at = at === steps.length - 1 ? -1 : at + 1; show(); });
      prev.addEventListener("click", function () { manual(); if (at > 0) { at--; show(); } });
      show();
      if (!auto) play.textContent = "Play";
      if ("IntersectionObserver" in window) {
        new IntersectionObserver(function (es) {
          visible = es[0].isIntersecting;
          if (visible) start(); else halt();
        }, { threshold: 0.3 }).observe(fig);
      } else { visible = true; start(); }
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
      var bHand = tray.querySelector('[data-act="handoff"]'), bFork = tray.querySelector('[data-act="fork"]');
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
        if (bHand) bHand.disabled = bFork.disabled = cards.length <= START.length;
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
        reset("<b>New chat.</b> A fresh window: only the startup cards. Your rules file loads again; nothing from the old chat comes along, and STOCK-OK is gone. The old chat isn't deleted: <code>/resume</code> opens it again. Use this between unrelated tasks.");
      });
      if (bHand) bHand.addEventListener("click", function () {
        var h = ["hand", "handoff.md", "in flight, why, next step; plans linked by path"];
        cards = START.concat([h]); w = 0; bWork.disabled = false;
        say.innerHTML = "<b>Handed off.</b> The agent wrote a short file (to your temp folder), you started a new chat and said <i>read it and continue</i>. Fresh window, plus one small card that carries the work. STOCK-OK survives only if the file wrote it down; a rule still belongs in AGENTS.md.";
        render([h]);
      });
      if (bFork) bFork.addEventListener("click", function () {
        say.innerHTML = "<b>Forked.</b> Nothing changed here: this window is exactly as it was. A full copy of it now runs as a separate background session on the side task, in its own worktree. (<code>/branch</code> makes the same copy but switches you into it.)";
        stack.classList.remove("forked"); void stack.offsetWidth; stack.classList.add("forked");
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

  // ---- Home page: the start button becomes "continue" once you've made progress ----
  function initStart() {
    var btn = document.getElementById("start-btn"), flag = flagId();
    if (!btn || !count()) return;
    if (!flag) { btn.textContent = "All 11 plaques earned · revisit the capstone →"; btn.href = "lessons/" + LESSONS[10][0]; return; }
    var i = LESSONS.findIndex(function (l, k) { return lessonId(k) === flag; });
    btn.textContent = "Continue: lesson " + (i + 1) + ", " + LESSONS[i][1] + " →";
    btn.href = "lessons/" + LESSONS[i][0];
  }

  // ---- Spot the problem: click the faulty lines, then Check ----
  function initSpots() {
    document.querySelectorAll(".spot").forEach(function (box) {
      var lines = box.querySelectorAll(".lines li"), res = box.querySelector(".result");
      var btn = document.createElement("button");
      btn.className = "btn primary"; btn.type = "button"; btn.textContent = "Check";
      box.querySelector(".lines").after(btn);
      lines.forEach(function (li) {
        li.tabIndex = 0;
        li.setAttribute("role", "checkbox"); li.setAttribute("aria-checked", "false");
        function toggle() {
          if (box.classList.contains("checked")) return;
          var on = li.classList.toggle("picked"); li.setAttribute("aria-checked", on ? "true" : "false");
        }
        li.addEventListener("click", toggle);
        li.addEventListener("keydown", function (e) { if (e.key === " " || e.key === "Enter") { e.preventDefault(); toggle(); } });
      });
      btn.addEventListener("click", function () {
        if (box.classList.contains("checked")) {
          box.classList.remove("checked"); btn.textContent = "Check"; res.innerHTML = "";
          lines.forEach(function (li) { li.classList.remove("picked", "hit", "miss", "wrong"); li.setAttribute("aria-checked", "false"); var n = li.querySelector(".why-line"); if (n) n.remove(); });
          return;
        }
        var hit = 0, bad = 0, wrong = 0;
        lines.forEach(function (li) {
          var isBad = li.hasAttribute("data-bad"), picked = li.classList.contains("picked"), why = li.getAttribute("data-why");
          if (isBad) bad++;
          var state = isBad && picked ? "hit" : isBad ? "miss" : picked ? "wrong" : "";
          if (state === "hit") hit++;
          if (state === "wrong") wrong++;
          if (state) {
            li.classList.add(state);
            if (why) { var n = document.createElement("span"); n.className = "why-line"; n.textContent = why.replace(/^(Fine|True)[:.]\s*/, ""); li.appendChild(n); }
          }
        });
        box.classList.add("checked"); btn.textContent = "Try again";
        res.innerHTML = "<b>" + hit + " of " + bad + " found" + (wrong ? ", " + wrong + " false alarm" + (wrong > 1 ? "s" : "") : "") + ".</b> " + (hit === bad && !wrong ? "Clean." : "Read the notes under the marked lines.");
      });
    });
  }

  // ---- Who you are: asked on the home page before you start, shown on the completion card ----
  function profile() { try { return JSON.parse(get("profile") || "{}"); } catch (e) { return {}; } }
  function saveProfile(p) { set("profile", JSON.stringify(p)); }
  function esc(t) { return String(t || "").replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function initWho() {
    var box = document.querySelector("[data-who]");
    if (!box) return;
    function render() {
      var p = profile();
      if (p.name) {
        box.innerHTML = '<p class="hello">Welcome, <b>' + esc(p.name) + '</b>. <button class="linkish" type="button">Change name</button></p>';
        box.querySelector("button").addEventListener("click", function () { p.name = ""; saveProfile(p); render(); box.querySelector("input").focus(); });
        return;
      }
      box.innerHTML = '<form class="ask-name"><label for="who-name">First, what’s your name? You need it to start; it goes on your completion page at the end.</label>' +
        '<div><input id="who-name" type="text" autocomplete="name" maxlength="60" placeholder="Your name" required aria-required="true">' +
        '<button class="btn" type="submit">Save</button></div></form>';
      box.querySelector("form").addEventListener("submit", function (e) {
        e.preventDefault();
        var v = box.querySelector("input").value.trim();
        if (!v) return;
        var q = profile(); q.name = v; saveProfile(q); render();
      });
    }
    render();
    // The journey starts only once there is a name: Start saves a typed name, or asks for one.
    var start = document.getElementById("start-btn");
    if (start) start.addEventListener("click", function (e) {
      if (profile().name) return;
      var inp = box.querySelector("input"), v = inp ? inp.value.trim() : "";
      if (v) { var q = profile(); q.name = v; saveProfile(q); return; }
      e.preventDefault();
      var form = box.querySelector(".ask-name");
      form.classList.add("need");
      var hint = form.querySelector(".hint") || form.appendChild(Object.assign(document.createElement("p"), { className: "hint" }));
      hint.textContent = "Add your name to start. It's saved only in this browser.";
      inp.focus();
    });
  }

  // ---- Completion page: unlocked by all 11 plaques; save as PNG, print, or share a link ----
  function initCompletion() {
    var box = document.querySelector("[data-completion]");
    if (!box) return;
    function url(u) { return /^https?:\/\/\S+$/i.test(u || "") ? u : ""; }
    function finished() {
      var d = ""; LESSONS.forEach(function (l, i) { var w = get("when:" + lessonId(i)) || ""; if (w > d) d = w; });
      return d || new Date().toISOString().slice(0, 10);
    }
    var CAN = ["Keep rules in files the agent reads every session", "Make the agent stop and hand over a decision (1-3-1)",
      "Gate work behind a reviewed plan, one slice per commit", "Turn repeated procedures into skills",
      "Get independent review from subagents", "Block risky actions with permission rules, hooks and tests",
      "Prove a harness on a fresh clone with the swap test"];
    function card(d, shared) {
      var links = [["Practice repo", url(d.repo)], ["Capstone repo", url(d.cap)]].filter(function (x) { return x[1]; });
      return '<article class="cert">' +
        '<span class="kick">Agent Harness · course completed</span>' +
        "<h3>" + esc(d.name || "Your name") + "</h3>" +
        '<p class="cdate">completed all 11 lessons on ' + esc(d.date) + "</p>" +
        '<div class="cplaques">' + LESSONS.map(function (l) { return '<span title="' + esc(l[2]) + '">' + icon(l[3]) + "<i>" + esc(l[2]) + "</i></span>"; }).join("") + "</div>" +
        '<p class="ccan"><b>Can now:</b> ' + CAN.map(esc).join(" · ") + "</p>" +
        (links.length ? '<p class="clinks">' + links.map(function (x) { return x[0] + ': <a href="' + esc(x[1]) + '">' + esc(x[1]) + "</a>"; }).join("<br>") + "</p>" : "") +
        '<p class="chonest">' + (shared ? "Shared completion card. " : "") + "Self-reported: each lesson was marked done by the learner. The repositories are the evidence: their git history shows the harness commits, the plans and the reviews.</p>" +
        "</article>";
    }
    // A shared link (#c=…) shows the card read-only, in anyone's browser.
    var m = location.hash.match(/^#c=(.+)$/);
    if (m) {
      var d = {};
      try { d = JSON.parse(decodeURIComponent(escape(atob(decodeURIComponent(m[1]))))); } catch (e) { d = null; }
      if (d && d.name) {
        var h1 = document.querySelector("h1"), lede = document.querySelector(".lede");
        if (h1) h1.textContent = d.name + " completed the Agent Harness course";
        if (lede) lede.textContent = "A free, hands-on tutorial on configuring AI coding agents: rules files, plans, skills, reviewers, guards and the swap test. Progress is self-reported; the linked repositories are the evidence.";
        document.title = d.name + " · Agent Harness completion";
      }
      box.innerHTML = d && d.name ? card(d, true) + '<p class="small">Want your own? <a href="index.html">Start the course</a>.</p>'
                                  : '<div class="clocked">This share link is incomplete or damaged. Ask for it again.</div>';
      return;
    }
    var prof = profile();
    box.innerHTML =
      '<div class="cfields">' +
      '<label>Your name<input type="text" data-f="name" autocomplete="name" maxlength="60"></label>' +
      '<label>Practice repo URL <small>(optional, the proof)</small><input type="url" data-f="repo" placeholder="https://github.com/you/stockapi" maxlength="200"></label>' +
      '<label>Capstone repo URL <small>(optional)</small><input type="url" data-f="cap" placeholder="https://github.com/you/roombooking" maxlength="200"></label>' +
      '</div><div class="cout"></div>';
    var out = box.querySelector(".cout");
    box.querySelectorAll("input[data-f]").forEach(function (inp) {
      var f = inp.getAttribute("data-f");
      inp.value = prof[f] || "";
      inp.addEventListener("input", function () { prof[f] = inp.value.trim(); saveProfile(prof); render(); });
    });
    function render() {
      var n = count();
      if (n < 11) {
        var miss = [];
        LESSONS.forEach(function (l, i) { if (!passed(lessonId(i))) miss.push('<a href="lessons/' + l[0] + '">' + (i + 1) + ". " + esc(l[1]) + "</a>"); });
        out.innerHTML = '<div class="clocked"><b>' + n + " of 11 plaques.</b> The card unlocks when every lesson's “Done when” list is ticked. Still to do: " + miss.join(" · ") + "</div>";
        return;
      }
      var d = { name: prof.name, date: finished(), repo: url(prof.repo), cap: url(prof.cap) };
      var share = location.href.split("#")[0] + "#c=" + encodeURIComponent(btoa(unescape(encodeURIComponent(JSON.stringify(d)))));
      out.innerHTML = card(d, false) +
        '<div class="cbtns"><button class="btn primary" type="button" data-act="png">Save as image</button>' +
        '<button class="btn" type="button" data-act="print">Print or save as PDF</button>' +
        '<button class="btn" type="button" data-act="share">Copy share link</button></div>' +
        '<p class="small share-out" hidden>Send this link: <input type="text" readonly></p>';
      out.querySelector('[data-act="print"]').addEventListener("click", function () {
        document.body.classList.add("print-cert"); window.print();
        setTimeout(function () { document.body.classList.remove("print-cert"); }, 500);
      });
      out.querySelector('[data-act="png"]').addEventListener("click", function () { savePng(d); });
      out.querySelector('[data-act="share"]').addEventListener("click", function () {
        var btn = this, box2 = out.querySelector(".share-out"), inp = box2.querySelector("input");
        inp.value = share; box2.hidden = false; inp.select();
        function done(ok) { btn.textContent = ok ? "Link copied" : "Copy it below"; setTimeout(function () { btn.textContent = "Copy share link"; }, 1800); }
        if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(share).then(function () { done(true); }, function () { done(false); });
        else { var ok = false; try { ok = document.execCommand("copy"); } catch (e) {} done(ok); }
      });
    }
    function savePng(d) {
      var W = 1200, H = 800, x = esc;
      var links = [["Practice repo", d.repo], ["Capstone repo", d.cap]].filter(function (l) { return l[1]; });
      var plaques = LESSONS.map(function (l, i) {
        var cx = i < 6 ? 150 + i * 180 : 240 + (i - 6) * 180, cy = i < 6 ? 320 : 430;
        return '<g transform="translate(' + (cx - 24) + "," + (cy - 40) + ') scale(2)" fill="none" stroke="#f3d27a" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">' + ICON[l[3]] + "</g>" +
          '<text x="' + cx + '" y="' + (cy + 30) + '" font-size="17" fill="#e9d8b4" text-anchor="middle">' + x(l[2]) + "</text>";
      }).join("");
      var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="' + W + '" height="' + H + '" font-family="Georgia, serif">' +
        '<rect width="100%" height="100%" fill="#2b1f14"/><rect x="24" y="24" width="' + (W - 48) + '" height="' + (H - 48) + '" rx="18" fill="none" stroke="#c99a3c" stroke-width="3"/>' +
        '<text x="600" y="100" font-size="20" letter-spacing="4" fill="#c99a3c" text-anchor="middle" font-family="Helvetica, Arial, sans-serif">AGENT HARNESS · COURSE COMPLETED</text>' +
        '<text x="600" y="175" font-size="58" fill="#fff3d6" text-anchor="middle">' + x(d.name || "Your name") + "</text>" +
        '<text x="600" y="220" font-size="22" fill="#e9d8b4" text-anchor="middle">completed all 11 lessons on ' + x(d.date) + "</text>" + plaques +
        '<text x="600" y="540" font-size="18" fill="#e9d8b4" text-anchor="middle" font-family="Helvetica, Arial, sans-serif">Rules files · 1-3-1 hand-overs · gated plans · skills · reviewers · guards · MCP · ADRs · evidence · the swap test</text>' +
        links.map(function (l, i) { return '<text x="600" y="' + (595 + i * 34) + '" font-size="20" fill="#f3d27a" text-anchor="middle" font-family="Helvetica, Arial, sans-serif">' + x(l[0] + ": " + l[1]) + "</text>"; }).join("") +
        '<text x="600" y="' + (H - 70) + '" font-size="16" fill="#bfae8c" text-anchor="middle" font-family="Helvetica, Arial, sans-serif">Self-reported. The repositories are the evidence: their git history shows the work.</text></svg>';
      var img = new Image();
      img.onload = function () {
        var cv = document.createElement("canvas"); cv.width = W; cv.height = H;
        cv.getContext("2d").drawImage(img, 0, 0);
        var a = document.createElement("a");
        a.download = "agent-harness-completion.png"; a.href = cv.toDataURL("image/png");
        document.body.appendChild(a); a.click(); a.remove();
      };
      img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg);
    }
    render();
  }
})();
