"""Case Coach: practise consulting case interviews — mental maths, step-by-step cases, frameworks.

Run locally:  streamlit run app.py
"""

import random
import time
from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from casecoach.cases import CASES, FRAMEWORKS
from casecoach.coach import interviewer_reply
from casecoach.drills import GENERATORS, check, fmt, make_drill

NAVY, INK, MUTED, LINE, GOOD, BAD = "#1F4E79", "#1B2430", "#6B7686", "#E3E7ED", "#2E7D5B", "#A3443B"

st.set_page_config(page_title="Case Coach", layout="wide")
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"], .stMarkdown, input, textarea, button {{ font-family: 'Inter', sans-serif; }}
  .block-container {{ padding-top: 2.6rem; max-width: 980px; }}
  #MainMenu, header [data-testid="stToolbar"] {{ visibility: hidden; }}
  .cc-head {{ border-bottom: 1px solid {LINE}; padding-bottom: 14px; margin-bottom: 18px; }}
  .cc-title {{ font-size: 28px; font-weight: 700; color: {INK}; letter-spacing: -0.3px; }}
  .cc-head p {{ color: {MUTED}; font-size: 14.5px; margin: 4px 0 0; }}
  .cc-q {{ font-size: 24px; font-weight: 600; color: {INK}; margin: 14px 0 18px; line-height: 1.35; }}
  .cc-step {{ font-size: 17px; font-weight: 600; color: {INK}; margin: 2px 0 10px; }}
  .cc-muted {{ color: {MUTED}; font-size: 13.5px; }}
  .cc-result {{ border-radius: 8px; padding: 12px 16px; margin: 4px 0 12px; font-size: 15px; color: {INK}; }}
  .cc-ok {{ background: #EAF4EE; border-left: 3px solid {GOOD}; }}
  .cc-no {{ background: #F8ECEB; border-left: 3px solid {BAD}; }}
  .cc-stats {{ display: flex; gap: 10px; margin: 2px 0 10px; }}
  .cc-stats div {{ flex: 1; border: 1px solid {LINE}; border-radius: 8px; padding: 8px 12px; }}
  .cc-stats span {{ display: block; color: {MUTED}; font-size: 12px; }}
  .cc-stats b {{ color: {INK}; font-size: 16px; font-weight: 600; }}
  .cc-card {{ border: 1px solid {LINE}; border-radius: 8px; padding: 14px 18px; margin: 8px 0 14px; background: #FFFFFF; }}
  .cc-prompt {{ background: #F3F5F8; border-left: 3px solid {NAVY}; padding: 12px 16px; border-radius: 4px;
               color: {INK}; font-size: 15px; margin: 6px 0 14px; }}
  .cc-tag {{ display: inline-block; font-size: 12px; color: {NAVY}; background: #E8EEF5; border-radius: 4px;
            padding: 2px 8px; margin-right: 6px; }}
  div[data-testid="stMetric"] {{ border: 1px solid {LINE}; border-radius: 8px; padding: 10px 14px; }}
  .cc-foot {{ color: {MUTED}; font-size: 12.5px; border-top: 1px solid {LINE}; margin-top: 28px; padding-top: 12px; }}
  .cc-foot a {{ color: {NAVY}; text-decoration: none; }}
</style>
<div class="cc-head">
  <div class="cc-title">Case Coach</div>
  <p>Practise for consulting case interviews: timed mental maths, step-by-step cases with model answers, and frameworks.</p>
</div>
""", unsafe_allow_html=True)

ss = st.session_state
ss.setdefault("rng", random.Random())
ss.setdefault("drill_log", [])   # one row per answered drill
ss.setdefault("case_log", [])    # one row per completed case
ss.setdefault("steps", {})       # case id -> number of steps revealed
ss.setdefault("revealed", set()) # (case id, step) pairs whose model answer is shown
ss.setdefault("chats", {})       # case id -> AI interviewer history

try:
    API_KEY = st.secrets.get("ANTHROPIC_API_KEY")
except Exception:
    API_KEY = None

tab_maths, tab_case, tab_frame, tab_prog = st.tabs(["Mental maths", "Practise a case", "Frameworks", "Progress"])

# ---------------- mental maths ----------------
with tab_maths:
    _, mid, _ = st.columns([0.12, 0.76, 0.12])
    with mid:
        stats = st.empty()  # filled at the end so the counts include the latest answer
        top_l, top_r = st.columns([3, 1])
        with top_r:
            with st.popover("Drill types", width="stretch"):
                kinds = st.multiselect("Include", list(GENERATORS), default=list(GENERATORS),
                                       label_visibility="collapsed") or list(GENERATORS)
        if "drill" not in ss or ss.get("drill_kinds") != kinds:
            ss.drill, ss.drill_kinds, ss.drill_start, ss.drill_result = make_drill(ss.rng, kinds), kinds, time.time(), None
        d = ss.drill
        top_l.markdown(f'<span class="cc-tag">{d.kind}</span>', unsafe_allow_html=True)
        st.markdown(f'<div class="cc-q">{d.question}</div>', unsafe_allow_html=True)
        with st.form("drill_form", clear_on_submit=True, border=False):
            a, b = st.columns([4, 1], vertical_alignment="bottom")
            answer = a.text_input("Your answer", placeholder="e.g. 36, 15%, 1,400 or 1.4k",
                                  label_visibility="collapsed")
            submitted = b.form_submit_button("Check", type="primary", width="stretch")
        if submitted and ss.drill_result is None:
            ok = check(d, answer)
            if ok is None:
                st.warning("Couldn't read that number. Try digits only, e.g. 36 or 15%.")
            else:
                secs = round(time.time() - ss.drill_start, 1)
                ss.drill_result = (ok, secs)
                ss.drill_log.append({"date": str(date.today()), "type": d.kind, "question": d.question,
                                     "your_answer": answer, "answer": fmt(d.answer, d.unit),
                                     "correct": ok, "seconds": secs})
        if ss.drill_result is not None:
            ok, secs = ss.drill_result
            cls, head = ("cc-ok", "Correct") if ok else ("cc-no", "Not quite")
            st.markdown(f'<div class="cc-result {cls}"><b>{head}.</b> The answer is {fmt(d.answer, d.unit)} '
                        f'<span class="cc-muted">· {secs:.0f} s</span><br><span class="cc-muted">{d.tip}</span></div>',
                        unsafe_allow_html=True)
            if st.button("Next question", type="primary"):
                ss.drill, ss.drill_start, ss.drill_result = make_drill(ss.rng, kinds), time.time(), None
                st.rerun()
        done = [r for r in ss.drill_log if r["date"] == str(date.today())]
        right_n = sum(r["correct"] for r in done)
        avg = f"{sum(r['seconds'] for r in done) / len(done):.0f} s" if done else "–"
        acc = f"{right_n / len(done):.0%}" if done else "–"
        stats.markdown(f'<div class="cc-stats"><div><span>Today</span><b>{right_n} / {len(done)}</b></div>'
                       f'<div><span>Accuracy</span><b>{acc}</b></div><div><span>Avg time</span><b>{avg}</b></div>'
                       f'<div><span>Goal</span><b>10 a day, &lt;20 s</b></div></div>', unsafe_allow_html=True)

# ---------------- case practice ----------------
with tab_case:
    by_id = {c["id"]: c for c in CASES}
    c1, c2 = st.columns([3, 1.4], vertical_alignment="bottom")
    pick = c1.selectbox("Case", list(by_id), format_func=lambda i: f"{by_id[i]['title']}  ·  {by_id[i]['type']}")
    mode = c2.segmented_control("Mode", ["Step by step", "AI interviewer"], default="Step by step",
                                label_visibility="hidden") or "Step by step"
    case = by_id[pick]
    tags = "".join(f'<span class="cc-tag">{t}</span>' for t in
                   (case["type"], case["difficulty"], f"~{case['minutes']} min"))
    st.markdown(f'<div class="cc-prompt">{tags}<div style="margin-top:8px">{case["prompt"]}</div></div>',
                unsafe_allow_html=True)

    if mode == "Step by step":
        with st.expander("Clarifying information"):
            st.write(case["clarifying"])
        total, shown = len(case["steps"]), ss.steps.get(pick, 1)
        st.progress(shown / total, text=f"Step {shown} of {total}")
        if shown > 1:
            with st.expander(f"Previous steps ({shown - 1})"):
                for i, step in enumerate(case["steps"][:shown - 1]):
                    st.markdown(f"**{i + 1}. {step['question']}**")
                    st.markdown(step["model_answer"])
        i, step = shown - 1, case["steps"][shown - 1]
        with st.container(border=True):
            st.markdown(f'<div class="cc-step">{step["question"]}</div>', unsafe_allow_html=True)
            if step.get("exhibit"):
                ex = step["exhibit"]
                rows = [[f"{v:,.1f}" if isinstance(v, float) else v for v in r] for r in ex["rows"]]
                st.table(pd.DataFrame(rows, columns=ex["columns"]).set_index(ex["columns"][0]))
            st.text_area("Your answer", key=f"ans_{pick}_{i}", height=130, label_visibility="collapsed",
                         placeholder="Write your answer first: structure, maths, so-what")
            if (pick, i) in ss.revealed:
                st.markdown("**Model answer**")
                st.markdown(step["model_answer"])
            b1, b2, _ = st.columns([1.2, 1, 2])
            if (pick, i) not in ss.revealed and b1.button("Show model answer", width="stretch"):
                ss.revealed.add((pick, i))
                st.rerun()
            if shown < total and b2.button("Next step", type="primary", width="stretch"):
                ss.steps[pick] = shown + 1
                st.rerun()
        if shown == total and (pick, i) in ss.revealed:
            st.markdown("**Case complete.** Score yourself honestly against the model answers.")
            s1, s2 = st.columns([2, 1], vertical_alignment="bottom")
            score = s1.slider("Overall score", 1, 10, 6)
            lesson = s1.text_input("One thing to improve next time")
            if s2.button("Log this case", type="primary", width="stretch"):
                ss.case_log.append({"date": str(date.today()), "case": case["title"], "type": case["type"],
                                    "score": score, "improve": lesson})
                st.success("Logged. See the Progress tab.")
            if s2.button("Restart case", width="stretch"):
                ss.steps[pick] = 1
                ss.revealed = {r for r in ss.revealed if r[0] != pick}
                st.rerun()
    else:
        if not API_KEY:
            st.info("The AI interviewer needs an Anthropic API key. Add ANTHROPIC_API_KEY to the app's secrets "
                    "(see .streamlit/secrets.toml.example). Step-by-step mode works without it.")
        else:
            chat = ss.chats.setdefault(pick, [{"role": "assistant", "content": case["prompt"] +
                                               "\n\nTake a moment, ask any clarifying questions, then walk me "
                                               "through your structure."}])
            for m in chat:
                st.chat_message(m["role"]).write(m["content"])
            if text := st.chat_input("Your answer"):
                chat.append({"role": "user", "content": text})
                reply = interviewer_reply(case, chat[1:], API_KEY)  # API history must start with the user
                chat.append({"role": "assistant", "content": reply or "Sorry, the interviewer is unavailable right now."})
                st.rerun()
            if len(chat) > 1 and st.button("Start over"):
                ss.chats.pop(pick)
                st.rerun()

# ---------------- frameworks ----------------
with tab_frame:
    st.markdown("Frameworks are a starting point. In an interview, tailor the structure to the specific problem.")
    cols = st.columns(2)
    for i, (name, body) in enumerate(FRAMEWORKS.items()):
        cols[i % 2].markdown(f'<div class="cc-card"><b>{name}</b><br>{body.replace(chr(10), "<br>")}</div>',
                             unsafe_allow_html=True)

# ---------------- progress ----------------
with tab_prog:
    st.caption("Progress is kept for this browser session. Download it to keep a record, and upload it next time.")
    up = st.file_uploader("Restore a saved case log (CSV)", type="csv")
    if up is not None and not ss.get("restored"):
        ss.case_log = pd.read_csv(up).to_dict("records") + ss.case_log
        ss.restored = True
    m1, m2, m3 = st.columns(3)
    m1.metric("Cases logged", len(ss.case_log))
    m2.metric("Average case score", f"{pd.DataFrame(ss.case_log)['score'].mean():.1f}" if ss.case_log else "–")
    acc = (sum(r["correct"] for r in ss.drill_log) / len(ss.drill_log)) if ss.drill_log else None
    m3.metric("Maths accuracy", f"{acc:.0%}" if acc is not None else "–")
    if len(ss.case_log) >= 2:
        df = pd.DataFrame(ss.case_log).reset_index()
        fig = go.Figure(go.Scatter(x=df["index"] + 1, y=df["score"], mode="lines+markers", line=dict(color=NAVY),
                                   hovertext=df["case"]))
        fig.update_layout(height=260, margin=dict(l=0, r=10, t=10, b=0), paper_bgcolor="#FFFFFF",
                          plot_bgcolor="#FFFFFF", font=dict(family="Inter, sans-serif", color=MUTED))
        fig.update_xaxes(title="Case number", gridcolor=LINE, dtick=1)
        fig.update_yaxes(title="Score", range=[0, 10.5], gridcolor=LINE)
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    if ss.case_log:
        st.dataframe(pd.DataFrame(ss.case_log), hide_index=True, width="stretch")
        st.download_button("Download case log (CSV)", pd.DataFrame(ss.case_log).to_csv(index=False), "case_log.csv")
    if ss.drill_log:
        st.download_button("Download maths log (CSV)", pd.DataFrame(ss.drill_log).to_csv(index=False), "maths_log.csv")

st.markdown('<div class="cc-foot">Aafan Khan · <a href="https://github.com/aafankhan4796-eng">GitHub</a> · '
            '<a href="https://www.linkedin.com/in/aafan-khan">LinkedIn</a> · All cases and companies are fictional '
            'and written for practice.</div>', unsafe_allow_html=True)
