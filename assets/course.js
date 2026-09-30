/* Agent Harness course — shared behaviour: theme toggle, quizzes, checklists, progress.
   Storage is a per-viewer convenience only; every page works without it. */
(function () {
  var KEY = "harness-course:";
  function get(k) { try { return localStorage.getItem(KEY + k); } catch (e) { return null; } }
  function set(k, v) { try { localStorage.setItem(KEY + k, v); } catch (e) {} }

  // ---- Theme: OS preference by default, explicit choice wins ----
  var root = document.documentElement;
  var saved = get("theme");
  if (saved) root.setAttribute("data-theme", saved);

  function currentTheme() {
    var t = root.getAttribute("data-theme");
    if (t) return t;
    return window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }

  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.createElement("button");
    btn.className = "theme-toggle";
    btn.type = "button";
    function label() { btn.textContent = currentTheme() === "dark" ? "Light" : "Dark"; }
    label();
    btn.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      set("theme", next);
      label();
    });
    document.body.appendChild(btn);

    initQuizzes();
    initChecklists();
    initToc();
  });

  // ---- Quizzes ----
  // Markup: <div class="quiz"><p class="q">…</p><div class="opts">
  //   <button class="opt" data-correct>…</button><button class="opt">…</button>…</div>
  //   <p class="why">…</p></div>
  // Options are shuffled on load so position is never a clue.
  function shuffle(list) {
    for (var i = list.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      list[i].parentNode.insertBefore(list[j], list[i]);
      var t = list[i]; list[i] = list[j]; list[j] = t;
    }
  }

  function initQuizzes() {
    var quizzes = Array.prototype.slice.call(document.querySelectorAll(".quiz"));
    if (!quizzes.length) return;
    var firstTry = {};
    var lesson = document.body.getAttribute("data-lesson");

    quizzes.forEach(function (quiz, qi) {
      var opts = Array.prototype.slice.call(quiz.querySelectorAll("button.opt"));
      opts.forEach(function (b) { b.type = "button"; });
      shuffle(opts.slice());

      var retry = document.createElement("button");
      retry.className = "btn retry";
      retry.type = "button";
      retry.textContent = "Try again";
      quiz.appendChild(retry);

      opts.forEach(function (b) {
        b.addEventListener("click", function () {
          var ok = b.hasAttribute("data-correct");
          if (!(qi in firstTry)) firstTry[qi] = ok;
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
        var current = Array.prototype.slice.call(quiz.querySelectorAll("button.opt"));
        current.forEach(function (o) { o.disabled = false; o.classList.remove("right", "wrong"); });
        shuffle(current);
      });
    });

    function report() {
      var answered = Object.keys(firstTry).length;
      var right = Object.keys(firstTry).filter(function (k) { return firstTry[k]; }).length;
      document.querySelectorAll(".score").forEach(function (s) {
        s.textContent = right + " of " + quizzes.length + " right first time" +
          (answered < quizzes.length ? " (" + (quizzes.length - answered) + " to go)" : "");
      });
      if (lesson && answered === quizzes.length) set("done:" + lesson, right + "/" + quizzes.length);
    }
  }

  // ---- Checklists: <ul class="check" data-key="…"> with <input type=checkbox> per item ----
  function initChecklists() {
    document.querySelectorAll("ul.check[data-key]").forEach(function (ul) {
      var key = "check:" + ul.getAttribute("data-key");
      var state = {};
      try { state = JSON.parse(get(key) || "{}"); } catch (e) {}
      ul.querySelectorAll("input[type=checkbox]").forEach(function (cb, i) {
        cb.checked = !!state[i];
        cb.addEventListener("change", function () { state[i] = cb.checked; set(key, JSON.stringify(state)); });
      });
    });
  }

  // ---- Course index: show quiz results per lesson ----
  function initToc() {
    document.querySelectorAll(".toc li[data-lesson]").forEach(function (li) {
      var v = get("done:" + li.getAttribute("data-lesson"));
      var st = li.querySelector(".st");
      if (v && st) st.textContent = "quiz " + v;
    });
  }
})();
