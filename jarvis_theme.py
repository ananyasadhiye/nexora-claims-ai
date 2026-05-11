"""
JARVIS Claims AI — Ultra-Premium Animated Dark Cyberpunk CSS Theme v2
Enhanced with rich animations, micro-interactions, and full responsiveness.
"""

JARVIS_CSS = """
<style>

/* ===================================================
   ROOT & IMPORTS
=================================================== */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --cyan:         #00f5ff;
    --cyan-dim:     rgba(0,245,255,0.13);
    --cyan-glow:    rgba(0,245,255,0.35);
    --green:        #00ff9d;
    --green-dim:    rgba(0,255,157,0.13);
    --red:          #ff4d6d;
    --red-dim:      rgba(255,77,109,0.13);
    --yellow:       #ffd93d;
    --purple:       #a855f7;
    --bg-deep:      #020409;
    --bg-card:      rgba(255,255,255,0.03);
    --bg-card2:     rgba(0,245,255,0.04);
    --border:       rgba(0,245,255,0.18);
    --border2:      rgba(0,245,255,0.08);
    --border3:      rgba(0,245,255,0.04);
    --text:         #e2f4ff;
    --text-dim:     rgba(226,244,255,0.5);
    --text-dimmer:  rgba(226,244,255,0.22);
    --radius:       18px;
    --radius-sm:    12px;
    --radius-xs:    8px;
    --blur:         blur(24px);
    --blur-sm:      blur(12px);
    --transition:   all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    --font-display: 'Syne', sans-serif;
    --font-mono:    'JetBrains Mono', monospace;
    --font-body:    'Inter', sans-serif;
}

/* ===================================================
   GLOBAL RESET & BACKGROUND
=================================================== */
html, body, [data-testid="stAppViewContainer"] {
    background: #020409 !important;
    color: var(--text) !important;
    font-family: var(--font-body) !important;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% 0%, rgba(0,245,255,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 100%, rgba(0,255,157,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 50% 50%, rgba(168,85,247,0.04) 0%, transparent 70%),
        #020409;
    animation: bgBreath 12s ease infinite alternate;
    z-index: -10;
}
@keyframes bgBreath { 0% { opacity:0.7; } 100% { opacity:1; } }

[data-testid="stAppViewContainer"]::after {
    content: "";
    position: fixed; inset: 0;
    background-image:
        linear-gradient(rgba(0,245,255,0.032) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,245,255,0.032) 1px, transparent 1px);
    background-size: 48px 48px;
    z-index: -9;
    pointer-events: none;
    animation: gridDrift 40s linear infinite;
}
@keyframes gridDrift { 0% { transform: translateY(0); } 100% { transform: translateY(48px); } }

[data-testid="stMain"]::before {
    content: "";
    position: fixed;
    width: 700px; height: 700px; border-radius: 50%;
    background: radial-gradient(circle, rgba(0,245,255,0.08) 0%, transparent 65%);
    top: -300px; left: -200px;
    pointer-events: none; z-index: -8;
    animation: orbFloat1 20s ease infinite alternate;
}
[data-testid="stMain"]::after {
    content: "";
    position: fixed;
    width: 600px; height: 600px; border-radius: 50%;
    background: radial-gradient(circle, rgba(0,255,157,0.07) 0%, transparent 65%);
    bottom: -200px; right: -150px;
    pointer-events: none; z-index: -8;
    animation: orbFloat2 25s ease infinite alternate;
}
@keyframes orbFloat1 { 0% { transform: translate(0,0) scale(1); } 100% { transform: translate(120px,180px) scale(1.15); } }
@keyframes orbFloat2 { 0% { transform: translate(0,0) scale(1); } 100% { transform: translate(-100px,-80px) scale(1.1); } }

/* ===================================================
   SIDEBAR
=================================================== */
[data-testid="stSidebar"] {
    background: rgba(2,4,9,0.97) !important;
    border-right: 1px solid var(--border) !important;
    backdrop-filter: var(--blur) !important;
    min-width: 230px !important; max-width: 230px !important;
}
[data-testid="stSidebar"]::before {
    content: "";
    position: absolute; inset: 0;
    background: linear-gradient(180deg, rgba(0,245,255,0.07) 0%, transparent 25%, transparent 75%, rgba(0,255,157,0.05) 100%);
    pointer-events: none; z-index: 0;
}
[data-testid="stSidebar"]::after {
    content: "";
    position: absolute; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0.35; z-index: 1; pointer-events: none;
    animation: sidebarScan 5s linear infinite;
}
@keyframes sidebarScan {
    0% { top:0; opacity:0; } 8% { opacity:0.35; } 92% { opacity:0.25; } 100% { top:100%; opacity:0; }
}

.jarvis-brand {
    display: flex; align-items: center; gap: 14px;
    padding: 28px 20px 12px; margin-bottom: 10px; position: relative; z-index: 2;
}
.jarvis-brand-icon {
    width: 42px; height: 42px; border-radius: 12px;
    background: linear-gradient(135deg, var(--cyan) 0%, var(--green) 100%);
    display: flex; align-items: center; justify-content: center; font-size: 20px;
    box-shadow: 0 0 30px var(--cyan-glow), 0 0 60px rgba(0,245,255,0.12);
    animation: iconPulse 3s ease infinite; position: relative; overflow: hidden;
}
.jarvis-brand-icon::after {
    content: "";
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(255,255,255,0.2), transparent);
    border-radius: inherit;
}
@keyframes iconPulse {
    0%,100% { box-shadow: 0 0 25px var(--cyan-glow); transform: scale(1); }
    50% { box-shadow: 0 0 50px rgba(0,245,255,0.7), 0 0 80px rgba(0,245,255,0.2); transform: scale(1.04); }
}
.jarvis-brand-text { line-height: 1.2; }
.jarvis-brand-name {
    font-size: 17px; font-weight: 800; font-family: var(--font-display);
    background: linear-gradient(90deg, var(--cyan), var(--green));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: 2px;
}
.jarvis-brand-sub {
    font-size: 9px; color: var(--text-dim);
    letter-spacing: 3px; text-transform: uppercase; font-weight: 500; margin-top: 2px;
}

[data-testid="stSidebar"] button,
[data-testid="stSidebar"] .stButton button {
    width: 100% !important; background: transparent !important; border: none !important;
    color: var(--text-dim) !important; font-size: 13px !important; font-weight: 500 !important;
    font-family: var(--font-body) !important; padding: 11px 16px !important;
    border-radius: var(--radius-xs) !important; text-align: left !important;
    transition: var(--transition) !important; margin-bottom: 2px !important;
    letter-spacing: 0.3px; position: relative; overflow: hidden;
}
[data-testid="stSidebar"] button:hover,
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(0,245,255,0.06) !important;
    color: var(--cyan) !important;
    box-shadow: inset 3px 0 0 var(--cyan) !important;
    transform: translateX(5px) !important;
}
.nav-active button {
    background: rgba(0,245,255,0.08) !important;
    color: var(--cyan) !important;
    box-shadow: inset 3px 0 0 var(--cyan), 0 0 20px rgba(0,245,255,0.05) !important;
}

.live-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: rgba(0,255,157,0.08); border: 1px solid rgba(0,255,157,0.25);
    border-radius: 20px; padding: 5px 12px;
    font-size: 11px; font-weight: 600; color: var(--green);
    letter-spacing: 0.5px; margin: 12px 20px 10px;
    animation: liveGlow 2s ease infinite alternate;
}
@keyframes liveGlow { 0% { box-shadow: none; } 100% { box-shadow: 0 0 15px rgba(0,255,157,0.15); } }
.live-dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--green); animation: blink 1.4s ease infinite; box-shadow: 0 0 8px var(--green);
}
@keyframes blink { 50% { opacity:0.2; transform:scale(0.8); } }

/* ===================================================
   TOP HEADER
=================================================== */
[data-testid="stHeader"] {
    background: rgba(2,4,9,0.95) !important;
    border-bottom: 1px solid var(--border2) !important;
    backdrop-filter: var(--blur) !important;
}

[data-testid="block-container"] {
    padding: 1.5rem 2rem 2rem !important; max-width: 100% !important;
}

/* ===================================================
   AUTO BADGE
=================================================== */
.auto-badge {
    display: inline-flex; align-items: center; gap: 8px;
    background: linear-gradient(90deg, rgba(0,245,255,0.08), rgba(0,245,255,0.04));
    border: 1px solid var(--border); border-radius: 6px;
    padding: 5px 14px; font-size: 10px; font-weight: 700;
    font-family: var(--font-display); color: var(--cyan);
    letter-spacing: 2px; text-transform: uppercase; margin-bottom: 14px;
    animation: badgeAppear 0.6s ease both; position: relative; overflow: hidden;
}
.auto-badge::after {
    content: ""; position: absolute; top:0; left:-100%; bottom:0; width:100%;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,0.1), transparent);
    animation: badgeSweep 3s ease infinite;
}
@keyframes badgeSweep { 0% { left:-100%; } 100% { left:100%; } }
@keyframes badgeAppear { from { opacity:0; transform:translateY(-10px); } to { opacity:1; transform:translateY(0); } }
.auto-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--cyan); animation: blink 1.2s ease infinite; box-shadow: 0 0 8px var(--cyan);
}

/* ===================================================
   HERO SECTION
=================================================== */
.hero-section {
    background:
        linear-gradient(135deg, rgba(0,245,255,0.07) 0%, rgba(0,255,157,0.03) 40%,
            rgba(168,85,247,0.04) 70%, rgba(0,245,255,0.02) 100%);
    border: 1px solid var(--border); border-radius: 24px;
    padding: 44px 48px; margin-bottom: 28px;
    position: relative; overflow: hidden;
    backdrop-filter: var(--blur); animation: heroReveal 1s cubic-bezier(0.4,0,0.2,1) both;
}
@keyframes heroReveal {
    from { opacity:0; transform:translateY(30px) scale(0.98); }
    to   { opacity:1; transform:translateY(0) scale(1); }
}
.hero-section::before {
    content: ""; position: absolute; top:0; left:0; right:0; height:1px;
    background: linear-gradient(90deg, transparent 0%, var(--cyan) 30%, var(--green) 70%, transparent 100%);
    animation: heroBorderAnim 4s ease infinite;
}
.hero-section::after {
    content: ""; position: absolute;
    width: 300px; height: 300px; border-radius: 50%;
    background: radial-gradient(circle, rgba(0,245,255,0.12) 0%, transparent 70%);
    top: -100px; right: -50px; pointer-events: none;
    animation: heroOrb 8s ease infinite alternate;
}
@keyframes heroBorderAnim { 0%,100% { opacity:0.5; } 50% { opacity:1; } }
@keyframes heroOrb { 0% { transform:translate(0,0) scale(1); } 100% { transform:translate(-30px,30px) scale(1.2); } }

.hero-h1 {
    font-size: 48px; font-weight: 800; line-height: 1.05;
    font-family: var(--font-display);
    background: linear-gradient(90deg, var(--cyan) 0%, #7fffff 40%, var(--green) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 6px; letter-spacing: -0.5px;
    animation: textReveal 0.8s ease 0.2s both;
}
.hero-h2 {
    font-size: 38px; font-weight: 700; line-height: 1.15;
    font-family: var(--font-display); color: var(--text);
    margin: 0 0 18px; animation: textReveal 0.8s ease 0.3s both;
}
@keyframes textReveal {
    from { opacity:0; transform:translateY(20px); }
    to   { opacity:1; transform:translateY(0); }
}
.hero-sub {
    font-size: 14px; color: var(--text-dim);
    max-width: 540px; line-height: 1.7; margin-bottom: 30px;
    animation: fadeSlideUp 0.8s ease 0.4s both;
}
.hero-risk-badge {
    position: absolute; right: 48px; top: 44px;
    background: rgba(255,77,109,0.08); border: 1px solid rgba(255,77,109,0.3);
    border-radius: 16px; padding: 22px 30px; text-align: right;
    animation: riskBadgeIn 0.8s ease 0.5s both; backdrop-filter: var(--blur-sm);
}
@keyframes riskBadgeIn { from { opacity:0; transform:translateX(30px); } to { opacity:1; transform:translateX(0); } }
.hero-risk-label {
    font-size: 10px; color: rgba(255,77,109,0.8);
    letter-spacing: 2px; text-transform: uppercase; font-weight: 700; margin-bottom: 4px;
}
.hero-risk-num {
    font-size: 60px; font-weight: 900; font-family: var(--font-mono);
    color: var(--red); line-height: 1;
    text-shadow: 0 0 40px rgba(255,77,109,0.6);
    animation: riskPulse 3s ease 1.5s infinite;
}
@keyframes riskPulse {
    0%,100% { text-shadow: 0 0 30px rgba(255,77,109,0.5); }
    50% { text-shadow: 0 0 60px rgba(255,77,109,0.9), 0 0 100px rgba(255,77,109,0.3); }
}
.hero-risk-sub { font-size: 11px; color: var(--text-dim); margin-top: 4px; }

/* ===================================================
   BUTTONS
=================================================== */
.stButton > button {
    background: linear-gradient(135deg, rgba(0,245,255,0.92), rgba(0,200,210,0.92)) !important;
    color: #020409 !important; font-weight: 700 !important; font-size: 13px !important;
    font-family: var(--font-body) !important; border: none !important;
    border-radius: var(--radius-xs) !important; padding: 11px 22px !important;
    box-shadow: 0 0 20px rgba(0,245,255,0.25), inset 0 1px 0 rgba(255,255,255,0.3) !important;
    transition: var(--transition) !important; letter-spacing: 0.4px !important;
    width: 100%; position: relative; overflow: hidden;
}
.stButton > button:hover {
    box-shadow: 0 0 40px rgba(0,245,255,0.5), 0 8px 30px rgba(0,245,255,0.2) !important;
    transform: translateY(-3px) !important;
}
.stButton > button:active { transform: translateY(0) scale(0.98) !important; }

.btn-ghost > button {
    background: transparent !important; color: var(--text-dim) !important;
    border: 1px solid var(--border2) !important; box-shadow: none !important;
}
.btn-ghost > button:hover {
    border-color: var(--cyan) !important; color: var(--cyan) !important;
    background: var(--cyan-dim) !important; box-shadow: 0 0 20px rgba(0,245,255,0.1) !important;
}

/* ===================================================
   KPI CARDS
=================================================== */
.kpi-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.02) 100%);
    border: 1px solid var(--border2); border-radius: var(--radius);
    padding: 24px; position: relative; overflow: hidden;
    backdrop-filter: var(--blur); transition: var(--transition); cursor: pointer;
}
.kpi-card::before {
    content: ""; position: absolute; top:0; left:0; right:0; height:1px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    opacity: 0.4; transition: opacity 0.3s;
}
.kpi-card::after {
    content: ""; position: absolute; inset:0;
    background: radial-gradient(ellipse 60% 50% at 50% 0%, rgba(0,245,255,0.06), transparent);
    opacity: 0; transition: opacity 0.4s; border-radius: inherit;
}
.kpi-card:hover {
    border-color: rgba(0,245,255,0.3);
    box-shadow: 0 0 40px rgba(0,245,255,0.12), 0 20px 60px rgba(0,0,0,0.3), inset 0 0 40px rgba(0,245,255,0.03);
    transform: translateY(-6px) scale(1.01);
}
.kpi-card:hover::before { opacity: 1; }
.kpi-card:hover::after { opacity: 1; }

.kpi-label {
    font-size: 9px; font-weight: 700; color: var(--text-dim);
    letter-spacing: 2px; text-transform: uppercase; margin-bottom: 12px;
}
.kpi-value {
    font-size: 36px; font-weight: 900; font-family: var(--font-mono);
    color: var(--cyan); line-height: 1;
    text-shadow: 0 0 25px rgba(0,245,255,0.45); transition: var(--transition);
}
.val-ok   { color: var(--green)  !important; text-shadow: 0 0 25px rgba(0,255,157,0.45) !important; }
.val-warn { color: var(--yellow) !important; text-shadow: 0 0 25px rgba(255,211,61,0.45) !important; }
.val-err  { color: var(--red)    !important; text-shadow: 0 0 25px rgba(255,77,109,0.45) !important; }

.kpi-delta {
    display: inline-flex; align-items: center; gap: 5px;
    font-size: 11px; font-weight: 600; margin-top: 10px; color: var(--green);
}
.kpi-delta-red { color: var(--red) !important; }
.kpi-delta-val { font-size: 10px; color: var(--text-dim); margin-left: 2px; }
.kpi-icon {
    position: absolute; right: 20px; top: 20px;
    width: 38px; height: 38px; border-radius: 10px;
    background: var(--cyan-dim); border: 1px solid var(--border);
    display: flex; align-items: center; justify-content: center; font-size: 16px;
    transition: var(--transition);
}
.kpi-card:hover .kpi-icon {
    transform: rotate(15deg) scale(1.1);
    background: rgba(0,245,255,0.2); box-shadow: 0 0 20px rgba(0,245,255,0.2);
}

/* ===================================================
   GLASS CARDS
=================================================== */
.glass-card {
    background: rgba(255,255,255,0.03); border: 1px solid var(--border2);
    border-radius: var(--radius); padding: 24px; position: relative; overflow: hidden;
    backdrop-filter: var(--blur); transition: var(--transition);
}
.glass-card::before {
    content: ""; position: absolute; top:0; left:0; right:0; height:1px;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,0.3), transparent);
    opacity: 0; transition: opacity 0.4s;
}
.glass-card::after {
    content: ""; position: absolute; bottom:0; left:0; right:0; height:1px;
    background: linear-gradient(90deg, transparent, rgba(0,255,157,0.12), transparent);
}
.glass-card:hover {
    border-color: rgba(0,245,255,0.2);
    box-shadow: 0 10px 60px rgba(0,245,255,0.08), 0 0 0 1px rgba(0,245,255,0.04);
    transform: translateY(-2px);
}
.glass-card:hover::before { opacity: 1; }

/* Scan line variant */
.scan-card::before {
    content: ""; position: absolute;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, var(--cyan), transparent);
    top: 0; left: 0; animation: scanLine 4s linear infinite; opacity: 0.4;
}
@keyframes scanLine {
    0% { top:0; opacity:0; } 5% { opacity:0.5; } 95% { opacity:0.3; } 100% { top:100%; opacity:0; }
}

.card-header { display: flex; align-items: center; gap: 12px; margin-bottom: 20px; }
.card-icon {
    width: 34px; height: 34px; border-radius: 9px;
    background: var(--cyan-dim); border: 1px solid var(--border);
    display: flex; align-items: center; justify-content: center; font-size: 15px;
    transition: var(--transition); flex-shrink: 0;
}
.glass-card:hover .card-icon { background: rgba(0,245,255,0.2); box-shadow: 0 0 15px rgba(0,245,255,0.2); }
.card-title { font-size: 14px; font-weight: 700; color: var(--text); font-family: var(--font-display); }
.card-sub { font-size: 11px; color: var(--text-dim); letter-spacing: 0.3px; margin-top: 2px; }

/* ===================================================
   ROUTE BADGES
=================================================== */
.route-badge {
    display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 20px;
    font-size: 11px; font-weight: 700; letter-spacing: 0.8px; text-transform: uppercase;
    font-family: var(--font-body); transition: var(--transition);
}
.route-fast   { background: rgba(0,255,157,0.1); border: 1px solid rgba(0,255,157,0.3); color: var(--green); animation: routeGlowGreen 3s ease infinite; }
.route-manual { background: rgba(255,211,61,0.1); border: 1px solid rgba(255,211,61,0.3); color: var(--yellow); }
.route-fraud  { background: rgba(255,77,109,0.1); border: 1px solid rgba(255,77,109,0.3); color: var(--red); animation: routeGlowRed 2s ease infinite; }
.route-spec   { background: rgba(0,245,255,0.1); border: 1px solid rgba(0,245,255,0.3); color: var(--cyan); }
@keyframes routeGlowGreen { 0%,100% { box-shadow:0 0 8px rgba(0,255,157,0.1); } 50% { box-shadow:0 0 20px rgba(0,255,157,0.3); } }
@keyframes routeGlowRed   { 0%,100% { box-shadow:0 0 8px rgba(255,77,109,0.1); } 50% { box-shadow:0 0 25px rgba(255,77,109,0.4); } }

/* ===================================================
   FIELD GRID
=================================================== */
.field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 14px; }
.field-item {
    background: rgba(0,245,255,0.025); border: 1px solid var(--border2);
    border-radius: var(--radius-xs); padding: 10px 14px; transition: var(--transition); cursor: default;
}
.field-item:hover { background: rgba(0,245,255,0.06); border-color: rgba(0,245,255,0.2); transform: scale(1.02); }
.field-key { font-size: 9px; font-weight: 700; color: var(--text-dim); letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 4px; }
.field-val { font-size: 12px; font-weight: 600; color: var(--text); font-family: var(--font-mono); }

/* ===================================================
   STATUS PILLS
=================================================== */
.status-pill {
    display: inline-flex; align-items: center; gap: 4px; padding: 3px 10px; border-radius: 12px;
    font-size: 10px; font-weight: 700; margin: 3px; letter-spacing: 0.5px;
}
.pill-ok   { background: rgba(0,255,157,0.1); color: var(--green);  border: 1px solid rgba(0,255,157,0.25); }
.pill-warn { background: rgba(255,211,61,0.1); color: var(--yellow); border: 1px solid rgba(255,211,61,0.25); }
.pill-err  { background: rgba(255,77,109,0.1); color: var(--red);   border: 1px solid rgba(255,77,109,0.25); }

/* ===================================================
   AI CONSOLE
=================================================== */
.ai-console {
    background: rgba(2,4,9,0.98); border: 1px solid var(--border);
    border-radius: var(--radius); overflow: hidden; position: relative;
}
.ai-console::before {
    content: ""; position: absolute; top:0; left:0; right:0; height:1px;
    background: linear-gradient(90deg, var(--cyan), var(--green)); opacity: 0.8;
}
.ai-console-header {
    padding: 14px 18px; border-bottom: 1px solid var(--border2);
    display: flex; align-items: center; gap: 10px;
    background: rgba(0,245,255,0.04);
}
.ai-console-dot {
    width: 9px; height: 9px; border-radius: 50%;
    background: var(--green); box-shadow: 0 0 12px var(--green);
    animation: consolePulse 1.8s ease infinite;
}
@keyframes consolePulse {
    0%,100% { transform:scale(1); box-shadow:0 0 8px var(--green); }
    50% { transform:scale(1.3); box-shadow:0 0 18px var(--green), 0 0 30px rgba(0,255,157,0.3); }
}
.ai-console-title { font-size: 13px; font-weight: 700; color: var(--text); font-family: var(--font-display); }
.ai-console-sub { font-size: 10px; color: var(--text-dim); margin-left: auto; }
.ai-console-body { padding: 18px; }
.ai-msg {
    background: rgba(0,245,255,0.05); border-left: 2px solid var(--cyan);
    padding: 10px 14px; border-radius: 0 10px 10px 0; margin-bottom: 10px;
    font-size: 12px; color: var(--text); animation: msgSlideIn 0.4s ease; line-height: 1.5;
}
.ai-msg-user {
    background: rgba(0,255,157,0.05); border-right: 2px solid var(--green); text-align: right;
    padding: 10px 14px; border-radius: 10px 0 0 10px; margin-bottom: 10px;
    font-size: 12px; color: var(--text); animation: msgSlideRight 0.4s ease; line-height: 1.5;
}
@keyframes msgSlideIn    { from { opacity:0; transform:translateX(-12px); } to { opacity:1; transform:translateX(0); } }
@keyframes msgSlideRight { from { opacity:0; transform:translateX(12px);  } to { opacity:1; transform:translateX(0); } }

/* ===================================================
   SECTION HEADERS
=================================================== */
.section-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
.section-title {
    font-size: 15px; font-weight: 700; font-family: var(--font-display);
    color: var(--text); display: flex; align-items: center; gap: 10px;
}
.section-title::before {
    content: ""; width: 3px; height: 20px;
    background: linear-gradient(180deg, var(--cyan), var(--green));
    border-radius: 2px; box-shadow: 0 0 10px var(--cyan-glow);
}
.section-action {
    font-size: 11px; font-weight: 600; color: var(--cyan);
    cursor: pointer; opacity: 0.75; transition: opacity 0.2s; letter-spacing: 0.5px;
}
.section-action:hover { opacity: 1; text-shadow: 0 0 10px var(--cyan-glow); }

/* ===================================================
   FRAUD ALERT
=================================================== */
.fraud-alert {
    background: rgba(255,77,109,0.07); border: 1px solid rgba(255,77,109,0.3);
    border-left: 4px solid var(--red); border-radius: 12px; padding: 14px 18px;
    display: flex; align-items: center; gap: 12px;
    font-size: 13px; color: var(--red); font-weight: 600;
    animation: fraudPulse 2s ease infinite;
}
@keyframes fraudPulse {
    0%,100% { box-shadow:0 0 0 rgba(255,77,109,0); border-left-color:var(--red); }
    50% { box-shadow:0 0 25px rgba(255,77,109,0.2); border-left-color:rgba(255,77,109,0.6); }
}

/* ===================================================
   INPUTS
=================================================== */
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.04) !important; border: 1px solid var(--border2) !important;
    border-radius: var(--radius-xs) !important; color: var(--text) !important;
    font-size: 13px !important; transition: var(--transition) !important; padding: 10px 16px !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 3px rgba(0,245,255,0.1), 0 0 20px rgba(0,245,255,0.08) !important;
    background: rgba(0,245,255,0.03) !important;
}
[data-testid="stTextInput"] input::placeholder { color: var(--text-dimmer) !important; }

[data-testid="stTextArea"] textarea {
    background: rgba(0,0,0,0.3) !important; border: 1px solid var(--border2) !important;
    border-radius: var(--radius-xs) !important; color: var(--text) !important;
    font-size: 12px !important; font-family: var(--font-mono) !important;
    transition: var(--transition) !important; resize: vertical !important; line-height: 1.6 !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: var(--cyan) !important;
    box-shadow: 0 0 0 3px rgba(0,245,255,0.1) !important; background: rgba(0,20,30,0.5) !important;
}

[data-testid="stFileUploader"] {
    background: rgba(0,245,255,0.025) !important; border: 1px dashed rgba(0,245,255,0.22) !important;
    border-radius: var(--radius-xs) !important; padding: 16px !important; transition: var(--transition) !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--cyan) !important; background: var(--cyan-dim) !important;
    box-shadow: 0 0 20px rgba(0,245,255,0.08) !important;
}
[data-testid="stFileUploader"] button {
    background: var(--cyan-dim) !important; border: 1px solid var(--border) !important;
    color: var(--cyan) !important; border-radius: var(--radius-xs) !important;
    font-size: 12px !important; font-weight: 600 !important; padding: 6px 14px !important;
    box-shadow: none !important; width: auto !important;
}

[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.04) !important; border: 1px solid var(--border2) !important;
    border-radius: var(--radius-xs) !important; color: var(--text) !important; transition: var(--transition) !important;
}

/* ===================================================
   PROGRESS BARS
=================================================== */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--cyan), var(--green)) !important;
    border-radius: 4px !important;
    box-shadow: 0 0 10px rgba(0,245,255,0.4) !important;
}
.stProgress > div > div > div {
    background: rgba(255,255,255,0.05) !important; border-radius: 4px !important;
}

/* ===================================================
   METRICS / ALERTS / TABS
=================================================== */
[data-testid="stMetric"] {
    background: var(--bg-card); border: 1px solid var(--border2);
    border-radius: var(--radius); padding: 16px 20px; transition: var(--transition);
}
[data-testid="stMetric"]:hover { border-color: var(--border); box-shadow: 0 0 40px rgba(0,245,255,0.15); transform: translateY(-3px); }
[data-testid="stMetricValue"] { color: var(--cyan) !important; font-family: var(--font-mono) !important; }
[data-testid="stMetricLabel"] { color: var(--text-dim) !important; font-size: 11px !important; }

.stSuccess { background: rgba(0,255,157,0.07)  !important; border: 1px solid rgba(0,255,157,0.25)  !important; color: var(--green) !important; border-radius: var(--radius-xs) !important; }
.stError   { background: rgba(255,77,109,0.07)  !important; border: 1px solid rgba(255,77,109,0.25) !important; color: var(--red) !important; border-radius: var(--radius-xs) !important; }
.stWarning { background: rgba(255,211,61,0.07)  !important; border: 1px solid rgba(255,211,61,0.25) !important; color: var(--yellow) !important; border-radius: var(--radius-xs) !important; }
.stInfo    { background: rgba(0,245,255,0.05)   !important; border: 1px solid var(--border) !important; color: var(--cyan) !important; border-radius: var(--radius-xs) !important; }

[data-testid="stTabs"] [role="tablist"] { gap: 4px; border-bottom: 1px solid var(--border2) !important; }
[data-testid="stTabs"] [role="tab"] {
    background: transparent !important; color: var(--text-dim) !important;
    font-size: 12px !important; font-weight: 600 !important;
    border-radius: 8px 8px 0 0 !important; padding: 9px 18px !important;
    border: none !important; transition: var(--transition) !important; font-family: var(--font-body) !important;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: var(--cyan-dim) !important; color: var(--cyan) !important;
    border-bottom: 2px solid var(--cyan) !important; box-shadow: 0 0 15px rgba(0,245,255,0.1) !important;
}

/* ===================================================
   SCROLLBAR
=================================================== */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: var(--cyan); }

/* ===================================================
   RESPONSIVE
=================================================== */
@media (max-width: 900px) {
    [data-testid="block-container"] { padding: 1rem 1.25rem !important; }
    .hero-section { padding: 28px 24px !important; }
    .hero-h1 { font-size: 34px !important; }
    .hero-h2 { font-size: 26px !important; }
    .hero-risk-badge { position: relative !important; right: auto !important; top: auto !important; display: inline-flex !important; margin-top: 16px !important; text-align: left !important; }
    .hero-risk-num { font-size: 40px !important; }
    .field-grid { grid-template-columns: 1fr !important; }
    [data-testid="stSidebar"] { min-width: 200px !important; max-width: 200px !important; }
}
@media (max-width: 600px) {
    .hero-h1 { font-size: 26px !important; }
    .hero-h2 { font-size: 20px !important; }
    .kpi-value { font-size: 26px !important; }
    [data-testid="stSidebar"] { min-width: 180px !important; max-width: 180px !important; }
    .jarvis-brand-name { font-size: 14px !important; }
}

/* ===================================================
   DECISION EMPTY STATE
=================================================== */
.decision-empty {
    min-height: 280px; display: flex; flex-direction: column;
    align-items: center; justify-content: center; color: var(--text-dim); gap: 14px;
}

/* ===================================================
   KEYFRAME LIBRARY
=================================================== */
@keyframes fadeSlideUp { from { opacity:0; transform:translateY(24px); } to { opacity:1; transform:translateY(0); } }
@keyframes fadeSlideLeft { from { opacity:0; transform:translateX(-16px); } to { opacity:1; transform:translateX(0); } }
@keyframes fadeSlideRight { from { opacity:0; transform:translateX(16px); } to { opacity:1; transform:translateX(0); } }
@keyframes fadeIn { from { opacity:0; } to { opacity:1; } }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes glowPulse {
    0%,100% { text-shadow: 0 0 20px rgba(0,245,255,0.4); }
    50% { text-shadow: 0 0 50px rgba(0,245,255,0.9), 0 0 80px rgba(0,245,255,0.3); }
}
@keyframes barFill { from { width: 0; } }
@keyframes alertPulse { 0%,100% { box-shadow:0 0 0 rgba(255,77,109,0); } 50% { box-shadow:0 0 20px rgba(255,77,109,0.2); } }

.delay-1 { animation-delay: 0.05s; }
.delay-2 { animation-delay: 0.12s; }
.delay-3 { animation-delay: 0.20s; }
.delay-4 { animation-delay: 0.30s; }

/* ===================================================
   HIDE STREAMLIT CHROME
=================================================== */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }
[data-testid="stToolbar"] { display: none; }

/* ===================================================
   UTILITY
=================================================== */
.mono { font-family: var(--font-mono) !important; }
.display { font-family: var(--font-display) !important; }
.cyan { color: var(--cyan) !important; }
.green { color: var(--green) !important; }
.red { color: var(--red) !important; }
.dim { color: var(--text-dim) !important; }
.fw-bold { font-weight: 700 !important; }

</style>

<!-- ========== ANIMATED PARTICLES ========== -->
<div style="position:fixed;inset:0;pointer-events:none;z-index:-7;overflow:hidden;">
  <div style="position:absolute;width:2px;height:2px;border-radius:50%;background:#00f5ff;box-shadow:0 0 6px #00f5ff;left:5%;animation:particleFloat 14s linear infinite 0s;opacity:0.5;"></div>
  <div style="position:absolute;width:3px;height:3px;border-radius:50%;background:#00f5ff;box-shadow:0 0 6px #00f5ff;left:15%;animation:particleFloat 11s linear infinite 2s;opacity:0.4;"></div>
  <div style="position:absolute;width:2px;height:2px;border-radius:50%;background:#00ff9d;box-shadow:0 0 6px #00ff9d;left:28%;animation:particleFloat 18s linear infinite 4s;opacity:0.5;"></div>
  <div style="position:absolute;width:3px;height:3px;border-radius:50%;background:#00f5ff;box-shadow:0 0 8px #00f5ff;left:42%;animation:particleFloat 13s linear infinite 1s;opacity:0.3;"></div>
  <div style="position:absolute;width:2px;height:2px;border-radius:50%;background:#00ff9d;box-shadow:0 0 6px #00ff9d;left:58%;animation:particleFloat 16s linear infinite 6s;opacity:0.5;"></div>
  <div style="position:absolute;width:3px;height:3px;border-radius:50%;background:#00f5ff;box-shadow:0 0 6px #00f5ff;left:72%;animation:particleFloat 12s linear infinite 3s;opacity:0.4;"></div>
  <div style="position:absolute;width:2px;height:2px;border-radius:50%;background:#a855f7;box-shadow:0 0 6px #a855f7;left:84%;animation:particleFloat 15s linear infinite 7s;opacity:0.35;"></div>
  <div style="position:absolute;width:2px;height:2px;border-radius:50%;background:#00f5ff;box-shadow:0 0 6px #00f5ff;left:93%;animation:particleFloat 10s linear infinite 5s;opacity:0.4;"></div>
  <div style="position:absolute;width:4px;height:4px;border-radius:50%;background:#00ff9d;box-shadow:0 0 10px #00ff9d;left:35%;animation:particleFloat 20s linear infinite 9s;opacity:0.25;"></div>
  <div style="position:absolute;width:2px;height:2px;border-radius:50%;background:#00f5ff;box-shadow:0 0 6px #00f5ff;left:62%;animation:particleFloat 17s linear infinite 8s;opacity:0.45;"></div>
</div>

<style>
@keyframes particleFloat {
    0%   { transform: translateY(110vh) translateX(0px); opacity: 0; }
    5%   { opacity: 0.5; }
    85%  { opacity: 0.4; }
    100% { transform: translateY(-10vh) translateX(30px); opacity: 0; }
}
</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(JARVIS_CSS, unsafe_allow_html=True)
