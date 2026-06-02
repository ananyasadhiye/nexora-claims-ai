import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import random
import time
import json
import sqlite3
from datetime import datetime, timedelta
from PyPDF2 import PdfReader
import docx as docxlib

st.set_page_config(
    layout="wide",
    page_title="NEXORA · Claims Intelligence",
    page_icon="⬡",
    initial_sidebar_state="expanded",
)

from jarvis_theme import inject_css
inject_css()

from extractor  import extract_fields
from validator  import validate_fields
from router     import route_claim
from explainer  import generate_reason
from db         import init_db, save_claim, get_claims
from ai_chat    import ask_ai

init_db()

if "page"          not in st.session_state: st.session_state.page = "Dashboard"
if "chat_history"  not in st.session_state: st.session_state.chat_history = []
if "last_result"   not in st.session_state: st.session_state.last_result = None
if "agents_online" not in st.session_state: st.session_state.agents_online = random.randint(20, 32)

SAMPLE_FNOL = """\
FNOL Report
Policy Number: PNL-554120
Policyholder: Anya Patel
Effective: 2024-01-12 to 2025-01-12

Incident Date: 2025-04-22
Time: 14:38
Location: Highway 51, Mumbai
Description: Rear-end collision while stopped at signal. No injuries.

Claimant: Anya Patel
Third Parties: Truck driver (license TN-09-XX)
Contact: anya.p@email.com / +91 98xxxxxx

Asset Type: Auto
Asset ID: MH-02-AK-4492
Estimated Damage: 42500
Claim Type: vehicle
Initial Estimate: 44000
"""

def read_file(f):
    if f.name.endswith(".txt"):
        return f.read().decode()
    if f.name.endswith(".json"):
        return json.dumps(json.load(f), indent=2)
    if f.name.endswith(".pdf"):
        r = PdfReader(f)
        return "\n".join(p.extract_text() or "" for p in r.pages)
    if f.name.endswith(".docx"):
        d = docxlib.Document(f)
        return "\n".join(p.text for p in d.paragraphs)
    return ""

def plotly_dark_layout(fig, height=260, margin=None):
    m = margin or dict(l=0, r=0, t=0, b=0)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2f4ff", family="Inter, sans-serif", size=11),
        height=height, margin=m, showlegend=False,
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,245,255,0.06)", zeroline=False, color="#e2f4ff", tickfont=dict(size=10))
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,245,255,0.06)", zeroline=False, color="#e2f4ff", tickfont=dict(size=10))
    return fig

def route_class(route):
    return {"Fast-track":"route-fast","Manual Review":"route-manual","Investigation Flag":"route-fraud","Specialist Queue":"route-spec"}.get(route,"route-manual")

def quality_color(q):
    return {"high":"val-ok","medium":"val-warn","low":"val-err"}.get(q,"")

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("""
    <div class="jarvis-brand">
      <div class="jarvis-brand-icon">⬡</div>
      <div class="jarvis-brand-text">
        <div class="jarvis-brand-name">NEXORA</div>
        <div class="jarvis-brand-sub">Claims AI</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="live-badge">
      <div class="live-dot"></div>
      Live · {st.session_state.agents_online} agents online
    </div>
    """, unsafe_allow_html=True)

    pages = [("⊞","Dashboard"),("◈","Claims"),("◎","Fraud Radar"),("⟁","Pipeline"),("⌘","AI Console"),("✦","Settings")]
    for icon, label in pages:
        active = "nav-active" if st.session_state.page == label else ""
        col = st.container()
        col.markdown(f'<div class="{active}">', unsafe_allow_html=True)
        if col.button(f"{icon}  {label}", key=f"nav_{label}", width='stretch'):
            st.session_state.page = label
            st.rerun()
        col.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="padding:12px 20px;">
      <div style="font-size:10px;color:rgba(226,244,255,0.35);letter-spacing:1px;text-transform:uppercase;margin-bottom:6px;">System Status</div>
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
        <div style="width:6px;height:6px;border-radius:50%;background:#00ff9d;box-shadow:0 0 8px #00ff9d;"></div>
        <span style="font-size:11px;color:rgba(226,244,255,0.65);">Extraction Engine</span>
      </div>
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
        <div style="width:6px;height:6px;border-radius:50%;background:#00ff9d;box-shadow:0 0 8px #00ff9d;"></div>
        <span style="font-size:11px;color:rgba(226,244,255,0.65);">Fraud Model</span>
      </div>
      <div style="display:flex;align-items:center;gap:8px;">
        <div style="width:6px;height:6px;border-radius:50%;background:#00f5ff;box-shadow:0 0 8px #00f5ff;animation:blink 1.5s ease infinite;"></div>
        <span style="font-size:11px;color:rgba(226,244,255,0.65);">AI Router</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════
if st.session_state.page == "Dashboard":
    risk_score = 38
    st.markdown(f"""
    <div class="hero-section">
      <div class="auto-badge"><div class="auto-dot"></div> Autonomous Mode · Active</div>
      <div class="hero-h1">Claims Intelligence</div>
      <div class="hero-h2">at machine speed.</div>
      <div class="hero-sub">NEXORA ingests FNOL documents, extracts fields, validates, scores fraud risk and routes — fully explainable, in seconds.</div>
      <div style="display:flex;gap:24px;flex-wrap:wrap;margin-bottom:24px;">
        <div style="display:flex;align-items:center;gap:8px;">
          <div style="width:6px;height:6px;border-radius:50%;background:#00ff9d;box-shadow:0 0 8px #00ff9d;"></div>
          <span style="font-size:11px;color:rgba(226,244,255,0.6);">Extraction Engine <span style="color:#00ff9d;font-weight:700;">Online</span></span>
        </div>
        <div style="display:flex;align-items:center;gap:8px;">
          <div style="width:6px;height:6px;border-radius:50%;background:#00ff9d;box-shadow:0 0 8px #00ff9d;"></div>
          <span style="font-size:11px;color:rgba(226,244,255,0.6);">Fraud Model <span style="color:#00ff9d;font-weight:700;">Active</span></span>
        </div>
        <div style="display:flex;align-items:center;gap:8px;">
          <div style="width:6px;height:6px;border-radius:50%;background:#00f5ff;box-shadow:0 0 8px #00f5ff;"></div>
          <span style="font-size:11px;color:rgba(226,244,255,0.6);">AI Router <span style="color:#00f5ff;font-weight:700;">Processing</span></span>
        </div>
        <span style="font-size:11px;color:rgba(226,244,255,0.4);">{st.session_state.agents_online} agents online</span>
      </div>
      <div class="hero-risk-badge">
        <div class="hero-risk-label">▲ System Risk</div>
        <div class="hero-risk-num">{risk_score}</div>
        <div class="hero-risk-sub">/ 100 threshold</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    b1, b2, b_rest = st.columns([1.3, 1.3, 6])
    with b1:
        if st.button("⬆  Ingest new claim", key="hero_ingest"):
            st.session_state.page = "Claims"; st.rerun()
    with b2:
        st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
        if st.button("View pipeline", key="hero_pipeline"):
            st.session_state.page = "Pipeline"; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)
    kpi_data = [
        ("CLAIMS TODAY","1,284","val-ok","⬈ +12.4%",True,"◈",78),
        ("AUTO-RESOLVED","86%","val-ok","⬈ +3.1%",True,"⚡",86),
        ("FRAUD FLAGS","34","val-err","⬊ -8.2%",False,"◉",34),
        ("RESERVES SAVED","$2.4M","val-ok","⬈ +18%",True,"✦",72),
    ]
    for i, (col, (label, val, vc, delta, up, icon, bar_pct)) in enumerate(zip([k1,k2,k3,k4], kpi_data)):
        with col:
            delta_cls = "" if up else "kpi-delta-red"
            bar_color = "#00ff9d" if up else "#ff4d6d"
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-icon">{icon}</div>
              <div class="kpi-label">{label}</div>
              <div class="kpi-value {vc}">{val}</div>
              <div class="kpi-delta {delta_cls}">{delta} <span class="kpi-delta-val">vs last week</span></div>
              <div style="height:3px;background:rgba(255,255,255,0.06);border-radius:2px;margin-top:14px;overflow:hidden;">
                <div style="height:100%;width:{bar_pct}%;background:{bar_color};border-radius:2px;box-shadow:0 0 8px {bar_color}88;"></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left_col, right_col = st.columns([1.05, 1])
    with left_col:
        st.markdown("""<div class="card-header"><div class="card-icon">◈</div><div><div class="card-title">FNOL Intake</div><div class="card-sub">Paste text or upload .txt</div></div></div>""", unsafe_allow_html=True)
        fnol_text = st.text_area("FNOL Text", value=SAMPLE_FNOL, height=220, key="dashboard_fnol", label_visibility="collapsed")
        uploaded = st.file_uploader("Upload FNOL document", type=["txt","json","pdf","docx"], key="dashboard_upload", label_visibility="collapsed")
        if uploaded:
            fnol_text = read_file(uploaded)
        pc, rc = st.columns([1.3, 1])
        with pc:
            process_btn = st.button("⚙  Process FNOL", key="dash_process")
        with rc:
            st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
            if st.button("Reset to sample", key="dash_reset"):
                st.session_state.last_result = None; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown("""<div class="card-header"><div class="card-icon">✦</div><div><div class="card-title">Decision Output</div><div class="card-sub">extractedFields · missingFields · route · reasoning</div></div></div>""", unsafe_allow_html=True)
        result_placeholder = st.empty()

        if st.session_state.last_result:
            r = st.session_state.last_result
            data = r["data"]; validation = r["validation"]; route = r["route"]; reason = r["reason"]
            rc_cls = route_class(route)
            q_pill = {"high":"pill-ok","medium":"pill-warn","low":"pill-err"}.get(validation.get("quality",""),"pill-warn")

            fields_html = "".join(
                f'<div class="field-item"><div class="field-key">{k.replace("_"," ")}</div><div class="field-val">{str(v)[:28] if v else "—"}</div></div>'
                for k, v in list(data.items())[:8] if not k.startswith("_")
            )
            fraud_alerts = "".join(
                f'<div class="fraud-alert" style="margin-top:10px;">🚨 {x.replace("_"," ").title()}</div>'
                for x in validation.get("inconsistent", [])[:2]
            )

            result_placeholder.markdown(f"""
            <div style="animation:fadeSlideUp 0.5s ease;">
              <div style="display:flex;align-items:center;gap:10px;margin-bottom:14px;flex-wrap:wrap;">
                <span class="route-badge {rc_cls}">{route}</span>
                <span class="status-pill {q_pill}">Quality: {validation.get("quality","—").upper()}</span>
                <span style="font-size:11px;color:var(--text-dim);margin-left:auto;">Score: <span class="mono cyan">{validation.get("confidence_score",0)}</span></span>
              </div>
              <div class="field-grid">{fields_html}</div>
              <div style="margin-top:12px;padding:10px 14px;background:rgba(0,245,255,0.04);border:1px solid var(--border2);border-radius:8px;">
                <div style="font-size:10px;color:var(--text-dim);letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;">Reasoning</div>
                <div style="font-size:12px;color:var(--text);">{reason}</div>
              </div>
              {fraud_alerts}
            </div>
            """, unsafe_allow_html=True)
        else:
            result_placeholder.markdown("""
            <div class="decision-empty" style="min-height:240px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;">
              <div style="font-size:36px;opacity:0.3;">✦</div>
              <div style="font-size:13px;color:var(--text-dim);text-align:center;">Submit an FNOL to see the agent's structured<br>extraction, validation and routing decision.</div>
            </div>
            """, unsafe_allow_html=True)

    if process_btn and fnol_text.strip():
        with st.spinner(""):
            prog = st.progress(0)
            status_box = st.empty()
            for i, msg in enumerate(["Preprocessing FNOL document…","Extracting structured fields via AI…","Validating policy dates & damage…","Scoring fraud indicators…","Routing claim decision…"]):
                status_box.markdown(f'<div class="glass-card" style="padding:12px 16px;margin-top:8px;"><span class="cyan mono" style="font-size:12px;">▶ {msg}</span></div>', unsafe_allow_html=True)
                prog.progress((i+1)*20)
                time.sleep(0.3)
            data = extract_fields(fnol_text)
            validation = validate_fields(data)
            route = route_claim(data, validation)
            reason = generate_reason(route, data, validation)
            risk = max(0, 100 - validation.get("confidence_score", 50))
            save_claim(data, validation, route, reason, risk)
            st.session_state.last_result = dict(data=data, validation=validation, route=route, reason=reason, risk=risk)
            prog.empty(); status_box.empty()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    tc, ac = st.columns([1.4, 1])
    with tc:
        st.markdown("""<div class="section-header"><div class="section-title">Throughput · 12h</div><div style="font-size:12px;color:var(--text-dim);">Claims processed per hour</div></div>""", unsafe_allow_html=True)
        now = datetime.now()
        hrs = [(now - timedelta(hours=12-i)).strftime("%H:%M") for i in range(13)]
        noise = [b + random.randint(-4,4) for b in [38,42,55,48,72,81,69,95,110,102,118,130,128]]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hrs, y=noise, mode="lines", fill="tozeroy", fillcolor="rgba(0,245,255,0.07)", line=dict(color="#00f5ff", width=2.5, shape="spline"), hovertemplate="%{x}<br><b>%{y}</b> claims<extra></extra>"))
        fig = plotly_dark_layout(fig, height=240)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with ac:
        st.markdown("""
        <div class="ai-console" style="min-height:280px;">
          <div class="ai-console-header"><div class="ai-console-dot"></div><div class="ai-console-title">AI Console</div><div class="ai-console-sub">GPT-4o · Claims v2</div></div>
          <div class="ai-console-body" style="max-height:200px;">
            <div class="ai-msg">Pipeline scan complete. 3 new FNOLs ingested in last 60s.</div>
            <div class="ai-msg-user">Summarize FNOL-8801 risk factors.</div>
            <div class="ai-msg">Theft claim · $22,150 · 2 inconsistencies in timeline · prior claim 11mo ago. Recommend Investigation Flag.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Open full AI Console →", key="dash_open_console"):
            st.session_state.page = "AI Console"; st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="section-header"><div class="section-title">Live Claims Pipeline</div><div class="section-action">View all →</div></div>""", unsafe_allow_html=True)

    rows = get_claims()
    if rows:
        cols_h = st.columns([1.2, 1.5, 1, 1, 1.8, 1.2])
        for col, h in zip(cols_h, ["ID","Policy","Damage","Risk","Route","Date"]):
            col.markdown(f"<div style='font-size:10px;font-weight:700;color:var(--text-dim);letter-spacing:1px;text-transform:uppercase;padding:6px 0;'>{h}</div>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:4px 0 8px;'>", unsafe_allow_html=True)
        for row in rows[-8:][::-1]:
            cid, raw_data, raw_val, route_, reason_, risk_ = row
            try: d = json.loads(raw_data)
            except: d = {}
            rc_cls = route_class(route_)
            damage = d.get("estimated_damage","—")
            policy = d.get("policy_number", f"PN-{cid:04d}")
            rcolor = "#ff4d4d" if int(risk_ or 0) > 60 else "#ffd93d" if int(risk_ or 0) > 35 else "#00ff9d"
            cols_r = st.columns([1.2, 1.5, 1, 1, 1.8, 1.2])
            cols_r[0].markdown(f"<span class='mono cyan' style='font-size:11px;'>#{cid:04d}</span>", unsafe_allow_html=True)
            cols_r[1].markdown(f"<span style='font-size:12px;'>{str(policy)[:14]}</span>", unsafe_allow_html=True)
            cols_r[2].markdown(f"<span style='font-size:12px;font-weight:600;'>₹{damage}</span>", unsafe_allow_html=True)
            cols_r[3].markdown(f"<span style='font-size:12px;color:{rcolor};font-weight:700;'>{risk_}</span>", unsafe_allow_html=True)
            cols_r[4].markdown(f"<span class='route-badge {rc_cls}' style='font-size:10px;padding:3px 8px;'>{route_}</span>", unsafe_allow_html=True)
            cols_r[5].markdown(f"<span style='font-size:10px;color:var(--text-dim);'>{datetime.now().strftime('%d %b %H:%M')}</span>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-card" style="text-align:center;padding:32px;color:var(--text-dim);font-size:13px;">No claims processed yet. Use the FNOL Intake above to get started.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# CLAIMS
# ══════════════════════════════════════════════════════
elif st.session_state.page == "Claims":
    st.markdown("""
    <div class="auto-badge"><div class="auto-dot"></div> Claims Processing</div>
    <div class="hero-h1" style="font-size:32px;margin-bottom:4px;">Ingest New Claim</div>
    <div class="hero-sub" style="margin-bottom:24px;">Upload or paste any FNOL document. NEXORA extracts, validates and routes it instantly.</div>
    """, unsafe_allow_html=True)

    lc, rc = st.columns([1.1, 1])
    with lc:
        st.markdown("""<div class="card-header"><div class="card-icon">◈</div><div><div class="card-title">FNOL Document</div><div class="card-sub">Paste raw text or upload a file</div></div></div>""", unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload FNOL", type=["txt","json","pdf","docx"], key="claims_upload", label_visibility="collapsed")
        default_text = SAMPLE_FNOL
        if uploaded_file:
            default_text = read_file(uploaded_file)
        claim_text = st.text_area("FNOL Document", value=default_text, height=340, key="claims_textarea", label_visibility="collapsed")
        c1, c2 = st.columns(2)
        with c1:
            run_btn = st.button("⚙  Run AI Agent", key="claims_run")
        with c2:
            st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
            if st.button("Use Sample", key="claims_sample"): st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    with rc:
        st.markdown("""<div class="card-header"><div class="card-icon">✦</div><div><div class="card-title">AI Extraction Result</div><div class="card-sub">Structured fields · Validation · Routing</div></div></div>""", unsafe_allow_html=True)
        

        if run_btn and claim_text.strip():
            bar = st.progress(0)
            for step, pct in [("Classifying document…",20),("Extracting fields…",45),("Validating data…",65),("Scoring risk…",82),("Routing…",100)]:
                bar.progress(pct)
                st.markdown(f'<div class="glass-card" style="padding:14px 18px;"><span class="cyan mono" style="font-size:12px;">▶ {step}</span></div>', unsafe_allow_html=True)
                time.sleep(0.35)

            data = extract_fields(claim_text)
            validation = validate_fields(data)
            route = route_claim(data, validation)
            reason = generate_reason(route, data, validation)
            risk = max(0, 100 - validation.get("confidence_score", 50))
            save_claim(data, validation, route, reason, risk)
            st.session_state.last_result = dict(data=data, validation=validation, route=route, reason=reason, risk=risk)
            bar.empty()

            if data.get("_meta"):
                st.markdown(f'<div class="fraud-alert">⚠ Document classified as: <b>{data["_meta"].replace("_"," ").upper()}</b></div>', unsafe_allow_html=True)
            else:
                rc_cls = route_class(route)
                q = validation.get("quality","")
                q_cls = {"high":"pill-ok","medium":"pill-warn","low":"pill-err"}.get(q,"pill-warn")

                fields_html = "".join(
                    f'<div class="field-item"><div class="field-key">{k.replace("_"," ")}</div><div class="field-val">{str(v)[:32] if v else "—"}</div></div>'
                    for k, v in data.items() if not k.startswith("_")
                )

                # Build sections as variables BEFORE f-string
                missing_items = validation.get("missing", [])
                inconsist_items = validation.get("inconsistent", [])

                missing_pills = "".join(f'<span class="status-pill pill-err">{f}</span>' for f in missing_items)
                inconsist_pills = "".join(f'<span class="status-pill pill-warn">{w.replace("_"," ")}</span>' for w in inconsist_items)

                missing_section = '<div style="font-size:11px;color:var(--text-dim);margin-bottom:6px;">Missing Fields</div>' + missing_pills if missing_pills else ""
                inconsist_section = '<div style="font-size:11px;color:var(--text-dim);margin:8px 0 6px;">Inconsistencies</div>' + inconsist_pills if inconsist_pills else ""

                st.markdown(f"""
                <div style="animation:fadeSlideUp 0.5s ease;">
                  <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;flex-wrap:wrap;">
                    <span class="route-badge {rc_cls}">{route}</span>
                    <span class="status-pill {q_cls}">Quality: {q.upper()}</span>
                    <span style="margin-left:auto;font-size:12px;color:var(--text-dim);">Confidence: <span class="mono cyan">{validation.get("confidence_score",0)}/100</span></span>
                  </div>
                  <div class="field-grid">{fields_html}</div>
                  <div style="margin-top:14px;">
                    {missing_section}
                    {inconsist_section}
                  </div>
                  <div style="margin-top:14px;padding:12px 16px;background:rgba(0,245,255,0.04);border:1px solid var(--border2);border-radius:8px;">
                    <div style="font-size:10px;color:var(--text-dim);letter-spacing:1px;text-transform:uppercase;margin-bottom:4px;">AI Reasoning</div>
                    <div style="font-size:12px;color:var(--text);">{reason}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.last_result:
            r = st.session_state.last_result
            rc_cls = route_class(r["route"])
            st.markdown(f"""
            <div class="glass-card">
              <div class="route-badge {rc_cls}" style="margin-bottom:12px;">{r["route"]}</div>
              <div style="font-size:12px;color:var(--text-dim);margin-bottom:8px;">Last processed result. Run a new FNOL to refresh.</div>
              <div style="font-size:12px;color:var(--text);">{r.get("reason","")}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="decision-empty" style="min-height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;">
              <div style="font-size:48px;opacity:0.2;">✦</div>
              <div style="font-size:13px;color:var(--text-dim);text-align:center;">Run the AI agent to see extraction results here.</div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# FRAUD RADAR
# ══════════════════════════════════════════════════════
elif st.session_state.page == "Fraud Radar":
    st.markdown("""
    <div class="auto-badge"><div class="auto-dot"></div> Fraud Detection</div>
    <div class="hero-h1" style="font-size:32px;margin-bottom:4px;">Fraud Radar</div>
    <div class="hero-sub" style="margin-bottom:24px;">Real-time fraud signal monitoring, geographic hotspot analysis, and risk scoring.</div>
    """, unsafe_allow_html=True)

    fk1, fk2, fk3, fk4 = st.columns(4)
    for col, (label, val, vc, delta, up) in zip([fk1,fk2,fk3,fk4],[
        ("ACTIVE FLAGS","34","val-err","⬈ +12%",True),
        ("INVESTIGATION","9","val-warn","→ 0%",True),
        ("AVG RISK SCORE","61","val-warn","⬊ -4.1%",False),
        ("SAVED (FRAUD)","$1.2M","val-ok","⬈ +22%",True),
    ]):
        with col:
            dc = "" if up else "kpi-delta-red"
            st.markdown(f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value {vc}">{val}</div><div class="kpi-delta {dc}">{delta} <span class="kpi-delta-val">vs last week</span></div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    mc, rc = st.columns([1.3, 1])
    with mc:
        st.markdown("""<div class="section-header"><div class="section-title">Fraud Hotspot Map</div></div>""", unsafe_allow_html=True)
        lats = [19.076,28.704,12.971,22.572,17.385,23.022,26.912,13.082,21.177,30.733]
        lons = [72.877,77.102,77.594,88.363,78.486,72.571,75.857,80.270,72.831,76.779]
        sizes = [random.randint(8,25) for _ in range(10)]
        cities = ["Mumbai","Delhi","Bangalore","Kolkata","Hyderabad","Ahmedabad","Jaipur","Chennai","Surat","Ludhiana"]
        fig = go.Figure()
        fig.add_trace(go.Scattergeo(lat=lats, lon=lons, text=cities, mode="markers",
            marker=dict(size=sizes, color=sizes, colorscale=[[0,"rgba(0,255,157,0.7)"],[0.5,"rgba(255,211,61,0.8)"],[1,"rgba(255,77,77,0.9)"]],
            showscale=False, line=dict(width=1, color="rgba(0,245,255,0.4)")), hovertemplate="<b>%{text}</b><extra></extra>"))
        fig.update_geos(scope="asia", bgcolor="rgba(0,0,0,0)", showland=True, landcolor="rgba(0,20,30,0.8)",
            showocean=True, oceancolor="rgba(0,5,15,0.9)", showcoastlines=True, coastlinecolor="rgba(0,245,255,0.2)", showframe=False)
        fig = plotly_dark_layout(fig, height=320)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with rc:
        st.markdown("""<div class="section-header"><div class="section-title">Risk Distribution</div></div>""", unsafe_allow_html=True)
        fig = go.Figure(data=[go.Pie(
            labels=["Low (0-35)","Medium (35-65)","High (65-100)"], values=[42,35,23], hole=0.65,
            marker=dict(colors=["rgba(0,255,157,0.8)","rgba(255,211,61,0.8)","rgba(255,77,77,0.8)"], line=dict(color="rgba(0,0,0,0.3)",width=2)),
            textfont=dict(size=11, color="#e2f4ff"), hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>")])
        fig.add_annotation(text="34<br>flags", x=0.5, y=0.5, showarrow=False, font=dict(size=22, color="#00f5ff"), align="center")
        fig = plotly_dark_layout(fig, height=280)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown('<div class="fraud-alert">🚨 High Risk Claim Detected — FNOL-8801 · $22,150 · Theft</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div class="section-header"><div class="section-title">Multi-Signal Fraud Radar</div><div class="section-action">Run deep scan →</div></div>""", unsafe_allow_html=True)
    rows = get_claims()
    if rows:
        ri, ri2 = st.columns(2)
        risky = [r for r in rows if (r[5] or 0) > 40][-6:]
        with ri:
            categories = ["Timeline Gap","Damage Mismatch","Contact Invalid","Policy Lapse","Prior Claims","Third Party"]
            for rw in risky[:3]:
                cid, raw_data, raw_val, route_, _, risk_ = rw
                vals = [random.randint(20,100) for _ in categories]
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(r=vals+[vals[0]], theta=categories+[categories[0]], fill="toself",
                    fillcolor="rgba(255,77,77,0.1)", line=dict(color="#ff4d4d",width=1.5), name=f"Claim #{cid}"))
                fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,100],tickfont=dict(size=8,color="#aaa")),
                    angularaxis=dict(tickfont=dict(size=10,color="#e2f4ff")), bgcolor="rgba(0,0,0,0)"),
                    paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e2f4ff"), height=200, margin=dict(l=30,r=30,t=20,b=20),
                    title=dict(text=f"Claim #{cid} · Risk {risk_}", font=dict(size=12,color="#00f5ff")))
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.markdown('<div class="glass-card" style="text-align:center;padding:32px;color:var(--text-dim);font-size:13px;">Process claims to see fraud radar analysis.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# PIPELINE
# ══════════════════════════════════════════════════════
elif st.session_state.page == "Pipeline":
    st.markdown("""
    <div class="auto-badge"><div class="auto-dot"></div> Live Pipeline</div>
    <div class="hero-h1" style="font-size:32px;margin-bottom:4px;">Claims Pipeline</div>
    <div class="hero-sub" style="margin-bottom:24px;">All processed claims with routing decisions, risk scores, and status tracking.</div>
    """, unsafe_allow_html=True)

    rows = get_claims()
    total = len(rows)
    fast   = sum(1 for r in rows if r[3] == "Fast-track")
    manual = sum(1 for r in rows if r[3] == "Manual Review")
    fraud  = sum(1 for r in rows if r[3] == "Investigation Flag")
    spec   = sum(1 for r in rows if r[3] == "Specialist Queue")

    pa, pb, pc_, pd = st.columns(4)
    for col, label, val, cls in [(pa,"TOTAL CLAIMS",total,"val-ok"),(pb,"FAST-TRACK",fast,"val-ok"),(pc_,"MANUAL REVIEW",manual,"val-warn"),(pd,"FLAGGED",fraud+spec,"val-err")]:
        with col:
            st.markdown(f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value {cls}">{val}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    fc, sc_ = st.columns([2, 1])
    with fc:
        search = st.text_input("Search", placeholder="🔍  Search claims, cases, agents…", key="pipeline_search", label_visibility="collapsed")
    with sc_:
        route_filter = st.selectbox("Filter", ["All Routes","Fast-track","Manual Review","Investigation Flag","Specialist Queue"], key="pipeline_filter", label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    if rows:
        hcols = st.columns([0.7, 1.5, 1.8, 1.3, 0.8, 1.5, 1])
        for col, h in zip(hcols, ["#","Policy","Claimant","Damage","Risk","Route","Quality"]):
            col.markdown(f"<div style='font-size:10px;font-weight:700;color:var(--text-dim);letter-spacing:1px;text-transform:uppercase;padding:4px 0;'>{h}</div>", unsafe_allow_html=True)
        st.markdown("<hr style='margin:4px 0 4px;'>", unsafe_allow_html=True)
        for row in rows[::-1]:
            cid, raw_data, raw_val, route_, reason_, risk_ = row
            try: d = json.loads(raw_data)
            except: d = {}
            try: v = json.loads(raw_val)
            except: v = {}
            if route_filter != "All Routes" and route_ != route_filter: continue
            policy_ = str(d.get("policy_number", f"PN-{cid:04d}"))
            claimant_ = str(d.get("claimant","—"))
            if search and search.lower() not in (policy_+claimant_).lower(): continue
            damage_ = d.get("estimated_damage","—")
            quality_ = v.get("quality","—")
            rc_cls = route_class(route_)
            qc = {"high":"pill-ok","medium":"pill-warn","low":"pill-err"}.get(quality_,"pill-warn")
            rcolor = "#ff4d4d" if int(risk_ or 0) > 60 else "#ffd93d" if int(risk_ or 0) > 35 else "#00ff9d"
            dcols = st.columns([0.7, 1.5, 1.8, 1.3, 0.8, 1.5, 1])
            dcols[0].markdown(f"<span class='mono cyan' style='font-size:11px;'>#{cid:04d}</span>", unsafe_allow_html=True)
            dcols[1].markdown(f"<span style='font-size:12px;'>{policy_[:16]}</span>", unsafe_allow_html=True)
            dcols[2].markdown(f"<span style='font-size:12px;'>{claimant_[:20]}</span>", unsafe_allow_html=True)
            dcols[3].markdown(f"<span style='font-size:12px;font-weight:600;'>₹{damage_}</span>", unsafe_allow_html=True)
            dcols[4].markdown(f"<span style='font-size:12px;color:{rcolor};font-weight:700;'>{risk_}</span>", unsafe_allow_html=True)
            dcols[5].markdown(f"<span class='route-badge {rc_cls}' style='font-size:10px;padding:3px 8px;'>{route_}</span>", unsafe_allow_html=True)
            dcols[6].markdown(f"<span class='status-pill {qc}' style='font-size:10px;padding:3px 8px;'>{quality_}</span>", unsafe_allow_html=True)
            st.markdown("<div style='border-bottom:1px solid rgba(0,245,255,0.06);margin:2px 0;'></div>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="glass-card" style="text-align:center;padding:48px;color:var(--text-dim);font-size:13px;">No claims in the pipeline yet. Process an FNOL on the Claims page.</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# AI CONSOLE
# ══════════════════════════════════════════════════════
elif st.session_state.page == "AI Console":
    st.markdown("""
    <div class="auto-badge"><div class="auto-dot"></div> AI Agent Interface</div>
    <div class="hero-h1" style="font-size:32px;margin-bottom:4px;">AI Console</div>
    <div class="hero-sub" style="margin-bottom:24px;">Chat directly with the claims AI. Ask about fraud signals, validate policies, or query claim data.</div>
    """, unsafe_allow_html=True)

    chat_col, info_col = st.columns([1.6, 1])
    with chat_col:
        st.markdown("""
        <div class="ai-console" style="min-height:400px;">
          <div class="ai-console-header"><div class="ai-console-dot"></div><div class="ai-console-title">NEXORA · Claims Intelligence v2</div><div class="ai-console-sub">GPT-4o-mini</div></div>
          <div class="ai-console-body">
        """, unsafe_allow_html=True)

        if not st.session_state.chat_history:
            st.markdown('<div class="ai-msg">👋 NEXORA online. I can help you analyze claims, detect fraud signals, validate policy data, or summarize case files. What would you like to investigate?</div>', unsafe_allow_html=True)

        for msg in st.session_state.chat_history[-10:]:
            css_class = "ai-msg-user" if msg["role"] == "user" else "ai-msg"
            st.markdown(f'<div class="{css_class}">{msg["content"]}</div>', unsafe_allow_html=True)

        st.markdown("</div></div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        user_input = st.text_input("Ask NEXORA", placeholder="Ask NEXORA anything about your claims…", key="ai_input", label_visibility="collapsed")
        ic1, ic2 = st.columns([1.5, 1])
        with ic1:
            send_btn = st.button("⬆  Send", key="ai_send")
        with ic2:
            st.markdown('<div class="btn-ghost">', unsafe_allow_html=True)
            if st.button("Clear history", key="ai_clear"):
                st.session_state.chat_history = []; st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        if send_btn and user_input.strip():
            st.session_state.chat_history.append({"role":"user","content":user_input})
            with st.spinner(""):
                time.sleep(0.2)
                try: reply = ask_ai(user_input)
                except Exception as e: reply = f"[Agent offline: {e}]"
            st.session_state.chat_history.append({"role":"assistant","content":reply})
            st.rerun()

        st.markdown("""<div style="margin-top:12px;"><div style="font-size:10px;color:var(--text-dim);letter-spacing:1px;text-transform:uppercase;margin-bottom:8px;">Quick Prompts</div></div>""", unsafe_allow_html=True)
        for p in ["Summarize the top fraud risk factors in recent claims","What's the most common reason for Manual Review routing?","How is fraud score calculated in NEXORA?"]:
            if st.button(p, key=f"quick_{p[:20]}"):
                st.session_state.chat_history.append({"role":"user","content":p})
                try: reply = ask_ai(p)
                except Exception as e: reply = f"[Agent offline: {e}]"
                st.session_state.chat_history.append({"role":"assistant","content":reply})
                st.rerun()

    with info_col:
        st.markdown("""<div class="glass-card"><div class="card-header"><div class="card-icon">◉</div><div><div class="card-title">Agent Capabilities</div></div></div>""", unsafe_allow_html=True)
        for icon, title, desc in [("🔍","FNOL Analysis","Extract & validate claim fields from raw documents"),("⚡","Fraud Detection","Score risk signals and flag suspicious patterns"),("◈","Policy Lookup","Cross-reference policy dates, limits and coverage"),("✦","Routing Logic","Explain why a claim was routed to a specific queue"),("◎","Case Summary","Summarize entire claim history and decisions")]:
            st.markdown(f"""<div style="display:flex;gap:12px;padding:10px 0;border-bottom:1px solid var(--border2);align-items:flex-start;"><div style="font-size:18px;min-width:24px;">{icon}</div><div><div style="font-size:12px;font-weight:700;color:var(--text);margin-bottom:2px;">{title}</div><div style="font-size:11px;color:var(--text-dim);">{desc}</div></div></div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        rows = get_claims()
        st.markdown(f"""
        <div class="glass-card">
          <div class="card-header"><div class="card-icon">⊞</div><div><div class="card-title">System Stats</div></div></div>
          <div style="display:flex;flex-direction:column;gap:10px;">
            <div class="field-item"><div class="field-key">Claims Processed</div><div class="field-val">{len(rows)}</div></div>
            <div class="field-item"><div class="field-key">Chat Turns</div><div class="field-val">{len(st.session_state.chat_history)}</div></div>
            <div class="field-item"><div class="field-key">AI Model</div><div class="field-val">GPT-4o-mini</div></div>
            <div class="field-item"><div class="field-key">Agents Online</div><div class="field-val">{st.session_state.agents_online}</div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# SETTINGS
# ══════════════════════════════════════════════════════
elif st.session_state.page == "Settings":
    st.markdown("""
    <div class="auto-badge"><div class="auto-dot"></div> Configuration</div>
    <div class="hero-h1" style="font-size:32px;margin-bottom:4px;">Settings</div>
    <div class="hero-sub" style="margin-bottom:24px;">Configure NEXORA AI models, thresholds, routing rules, and system preferences.</div>
    """, unsafe_allow_html=True)

    s1, s2 = st.columns(2)
    with s1:
        st.markdown("""<div class="card-header"><div class="card-icon">⚡</div><div><div class="card-title">AI Model Config</div></div></div>""", unsafe_allow_html=True)
        st.selectbox("Extraction Model", ["openai/gpt-4o-mini","openai/gpt-4o","openai/gpt-3.5-turbo"], key="s_model")
        st.selectbox("Fraud Model", ["gemini-2.0-flash","gemini-1.5-pro","claude-3-haiku"], key="s_fraud_model")
        st.slider("Extraction Temperature", 0.0, 1.0, 0.0, 0.1, key="s_temp")
        st.slider("Fraud Sensitivity", 0, 100, 65, 5, key="s_fraud_sens")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div class="card-header"><div class="card-icon">◈</div><div><div class="card-title">Routing Thresholds</div></div></div>""", unsafe_allow_html=True)
        st.slider("Fast-track max damage (₹)", 5000, 100000, 25000, 5000, key="s_fasttrack")
        st.slider("High-risk score cutoff", 50, 100, 75, 5, key="s_highrisk")

    with s2:
        st.markdown("""<div class="card-header"><div class="card-icon">◉</div><div><div class="card-title">System Preferences</div></div></div>""", unsafe_allow_html=True)
        st.toggle("Autonomous Mode", value=True, key="s_auto")
        st.toggle("Real-time Alerts", value=True, key="s_alerts")
        st.toggle("Save all claims to DB", value=True, key="s_save_db")
        st.toggle("Enable voice agent", value=False, key="s_voice")
        st.toggle("Debug extraction logs", value=False, key="s_debug")
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""<div class="card-header"><div class="card-icon">⊞</div><div><div class="card-title">Database</div></div></div>""", unsafe_allow_html=True)
        rows = get_claims()
        st.markdown(f"""
        <div class="glass-card" style="padding:16px;">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
            <span style="font-size:13px;color:var(--text);">claims.db</span>
            <span class="mono cyan" style="font-size:13px;">{len(rows)} records</span>
          </div>
          <div style="height:4px;background:rgba(255,255,255,0.06);border-radius:4px;">
            <div style="height:100%;width:{min(100,len(rows)*10)}%;background:linear-gradient(90deg,var(--cyan),var(--green));border-radius:4px;"></div>
          </div>
          <div style="font-size:10px;color:var(--text-dim);margin-top:6px;">{min(100,len(rows)*10)}% of 10-record preview capacity</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save Settings", key="save_settings"):
            st.success("Settings saved successfully.")