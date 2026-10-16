# ============================================================
# ChargeWise India — EV Infrastructure Intelligence Platform
# Complete Streamlit app: real backend + animated frontend
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# ------------------------------------------------------------
# Page config (must be the first Streamlit call)
# ------------------------------------------------------------
st.set_page_config(
    page_title="ChargeWise India — EV Infrastructure Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------
# Custom CSS — premium light theme + animations
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root{
  --bg:#F6F8FB; --surface:#FFFFFF; --surface-2:#F8FAFC; --surface-3:#F1F5F9;
  --border:#E7ECF2; --border-2:#DCE3EC;
  --navy:#0B1B33; --navy-2:#1D2E48;
  --muted:#64748B; --muted-2:#94A3B8;
  --green:#0E9F6E; --green-d:#047857; --green-l:#E8F7F1;
  --amber:#F59E0B; --amber-l:#FEF4E3;
  --red:#EF4444; --red-l:#FEECEC;
  --blue:#3B82F6; --blue-l:#EAF2FE;
}

html, body, [class*="css"]{
  font-family:'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}
.stApp{
  background:
    radial-gradient(1100px 420px at 12% -8%, rgba(14,159,110,.055), transparent 62%),
    radial-gradient(900px 380px at 92% -12%, rgba(59,130,246,.045), transparent 60%),
    #F6F8FB;
  color:var(--navy);
}
#MainMenu, header[data-testid="stHeader"], footer{visibility:hidden; height:0;}
.block-container{padding: 1.4rem 2.2rem 3rem !important; max-width:100% !important;}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"]{
  background:#FFFFFF;
  border-right:1px solid var(--border);
}
section[data-testid="stSidebar"] > div:first-child{padding: 20px 14px;}

.brand{
  display:flex; align-items:center; gap:11px;
  padding: 4px 6px 18px; margin-bottom: 4px;
  border-bottom: 1px solid var(--border);
}
.brand-mark{
  width:38px; height:38px; border-radius:11px;
  background:linear-gradient(145deg,#0E9F6E,#0B8A5F);
  display:grid; place-items:center;
  box-shadow:0 8px 24px -8px rgba(14,159,110,.45);
  flex-shrink:0;
}
.brand-mark svg{width:20px; height:20px; color:#fff;}
.brand-name{font-size:15.5px; font-weight:800; letter-spacing:-.3px; line-height:1.15; color:#0B1B33;}
.brand-sub{font-size:10.5px; color:#94A3B8; font-weight:500; letter-spacing:.25px; text-transform:uppercase; margin-top:1px;}

.side-label{
  font-size:10px; font-weight:700; letter-spacing:.9px; text-transform:uppercase;
  color:#94A3B8; padding: 12px 4px 4px;
}

/* Streamlit widget overrides */
section[data-testid="stSidebar"] label{
  font-size:12.5px !important; font-weight:600 !important; color:#1D2E48 !important;
}
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"]{
  background:#0E9F6E !important; border-radius:8px !important;
}
section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] span{
  color:#fff !important; font-weight:600 !important;
}
section[data-testid="stSidebar"] input,
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"]{
  border-radius:10px !important;
}

/* ---------- Header ---------- */
.page-header{
  display:flex; align-items:flex-end; justify-content:space-between;
  gap:24px; padding: 6px 0 16px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 18px;
  animation: fadeUp .6s cubic-bezier(.22,1,.36,1) both;
}
.page-title h1{
  font-size:23px; font-weight:800; letter-spacing:-.65px; line-height:1.15;
  margin:0; color:#0B1B33;
}
.page-title p{font-size:12.8px; color:#64748B; margin:5px 0 0; font-weight:450;}
.live-chip{
  display:flex; align-items:center; gap:8px;
  padding: 7px 14px; border-radius:11px;
  background:#E8F7F1; border:1px solid #CBEBDE;
  font-size:12.5px; font-weight:650; color:#047857;
}
.live-dot{
  width:7px; height:7px; border-radius:50%; background:#0E9F6E;
  box-shadow: 0 0 0 0 rgba(14,159,110,.5);
  animation: livePulse 2s infinite;
}

/* ---------- KPI cards ---------- */
.kpi-grid{display:grid; grid-template-columns:repeat(4, 1fr); gap:16px; margin-bottom:18px;}
.kpi-card{
  background:#FFFFFF; border:1px solid var(--border);
  border-radius:18px; padding:18px 18px 14px;
  box-shadow: 0 1px 3px rgba(16,24,40,.06), 0 1px 2px rgba(16,24,40,.03);
  transition: transform .28s cubic-bezier(.22,1,.36,1), box-shadow .28s ease, border-color .28s;
  position:relative; overflow:hidden;
  animation: fadeUp .65s cubic-bezier(.22,1,.36,1) both;
}
.kpi-card:nth-child(1){animation-delay:.05s}
.kpi-card:nth-child(2){animation-delay:.12s}
.kpi-card:nth-child(3){animation-delay:.19s}
.kpi-card:nth-child(4){animation-delay:.26s}
.kpi-card:hover{
  transform: translateY(-3px);
  box-shadow: 0 22px 48px -18px rgba(11,27,51,.22), 0 6px 16px -8px rgba(11,27,51,.10);
  border-color:#DCE3EC;
}
.kpi-card::after{
  content:''; position:absolute; inset:0; border-radius:inherit; pointer-events:none;
  background: linear-gradient(180deg, rgba(14,159,110,.05), transparent 55%);
  opacity:0; transition:opacity .3s;
}
.kpi-card:hover::after{opacity:1;}
.kpi-top{display:flex; align-items:center; justify-content:space-between; margin-bottom:14px;}
.kpi-icon{
  width:38px; height:38px; border-radius:12px; display:grid; place-items:center;
}
.kpi-icon svg{width:18px; height:18px; stroke-width:2;}
.kpi-delta{
  display:flex; align-items:center; gap:4px;
  font-size:11.5px; font-weight:700; padding:3px 8px; border-radius:20px;
}
.delta-up{background:#E8F7F1; color:#047857;}
.delta-down{background:#FEECEC; color:#C0392B;}
.delta-flat{background:#F1F5F9; color:#64748B;}
.kpi-label{font-size:12.2px; font-weight:550; color:#64748B; margin-bottom:6px;}
.kpi-value{
  font-size:29px; font-weight:800; letter-spacing:-1.1px;
  line-height:1.05; color:#0B1B33;
  font-variant-numeric: tabular-nums;
}
.kpi-value .unit{font-size:15px; font-weight:650; color:#64748B; margin-left:2px;}
.kpi-foot{display:flex; align-items:flex-end; justify-content:space-between; margin-top:12px; gap:12px;}
.kpi-note{font-size:11.2px; color:#94A3B8; font-weight:500; line-height:1.4;}
.kpi-note b{color:#64748B; font-weight:650;}
.kpi-spark{width:90px; height:34px; flex-shrink:0;}
.kpi-spark svg{display:block; overflow:visible;}
.kpi-spark path{
  stroke-dasharray: 400; stroke-dashoffset: 400;
  animation: drawLine 1.6s cubic-bezier(.22,1,.36,1) .35s forwards;
}

/* ---------- Section cards ---------- */
.section-card{
  background:#FFFFFF; border:1px solid var(--border); border-radius:18px;
  padding:18px 20px; box-shadow: 0 1px 3px rgba(16,24,40,.06);
  animation: fadeUp .7s cubic-bezier(.22,1,.36,1) both;
  animation-delay:.15s;
}
.section-head{display:flex; align-items:flex-start; justify-content:space-between; gap:16px; margin-bottom:14px;}
.section-head h3{font-size:14.5px; font-weight:700; letter-spacing:-.25px; color:#0B1B33; margin:0;}
.section-head p{font-size:12px; color:#64748B; margin:3px 0 0; font-weight:450;}
.pill{
  display:inline-flex; align-items:center; gap:5px;
  font-size:10.5px; font-weight:700; padding:4px 10px; border-radius:20px;
}
.pill-amber{background:#FEF4E3; color:#B45309;}
.pill-green{background:#E8F7F1; color:#047857;}
.pill-red{background:#FEECEC; color:#C0392B;}

/* ---------- Gap panel big number ---------- */
.gap-hero{
  display:flex; align-items:center; gap:16px;
  padding: 6px 0 16px; border-bottom: 1px solid var(--border); margin-bottom: 12px;
}
.gap-big-num{
  font-size: 42px; font-weight: 800; letter-spacing: -1.8px; line-height: 1;
  color:#0B1B33; font-variant-numeric: tabular-nums;
}
.gap-big-sub{font-size:11.5px; font-weight:600; color:#94A3B8; letter-spacing:.4px; text-transform:uppercase; margin-top:6px;}
.gap-hero-text h4{font-size:13.5px; font-weight:700; color:#0B1B33; margin:0 0 5px;}
.gap-hero-text p{font-size:11.8px; color:#64748B; line-height:1.55; margin:0;}

/* ---------- Table ---------- */
.corridor-table{
  width:100%; border-collapse:separate; border-spacing:0; font-size:12.8px;
  animation: fadeUp .8s cubic-bezier(.22,1,.36,1) both; animation-delay:.3s;
}
.corridor-table th{
  text-align:left; font-size:10.5px; font-weight:700;
  letter-spacing:.65px; text-transform:uppercase; color:#94A3B8;
  padding: 8px 14px 11px; border-bottom: 1px solid var(--border);
}
.corridor-table td{
  padding: 13px 14px; border-bottom: 1px solid #F1F5F9; vertical-align: middle;
}
.corridor-table tr:hover td{background:#F8FAFC;}
.corridor-name{font-weight:650; font-size:12.8px; color:#0B1B33;}
.corridor-sub{font-size:11px; color:#94A3B8; font-weight:500; margin-top:1px;}
.cell-num{font-variant-numeric: tabular-nums; font-weight:650; letter-spacing:-.2px;}
.mini-bar{
  width:64px; height:5px; border-radius:20px; background:#F1F5F9;
  overflow:hidden; display:inline-block; vertical-align:middle; margin-right:9px;
}
.mini-bar i{display:block; height:100%; border-radius:20px;}
.status-pill{
  display:inline-flex; align-items:center; gap:6px;
  font-size:11px; font-weight:650; padding:4px 10px; border-radius:20px;
}
.sdot{width:6px; height:6px; border-radius:50%;}

/* ---------- Animations ---------- */
@keyframes fadeUp{
  from{opacity:0; transform: translateY(10px);}
  to{opacity:1; transform: translateY(0);}
}
@keyframes livePulse{
  0%{box-shadow: 0 0 0 0 rgba(14,159,110,.45);}
  70%{box-shadow: 0 0 0 7px rgba(14,159,110,0);}
  100%{box-shadow: 0 0 0 0 rgba(14,159,110,0);}
}
@keyframes drawLine{to{stroke-dashoffset:0;}}

/* ---------- Plotly container tweaks ---------- */
.js-plotly-plot .plotly .modebar{opacity:.35;}
.js-plotly-plot .plotly .modebar:hover{opacity:1;}

/* ---------- Divider ---------- */
hr{border:none; border-top:1px solid var(--border); margin: 22px 0;}

/* ---------- Hide Streamlit default metric look if it ever shows ---------- */
div[data-testid="stMetricValue"]{font-variant-numeric: tabular-nums;}
</style>
""", unsafe_allow_html=True)


# ============================================================
# BACKEND — data generation & metrics
# ============================================================

CITIES = [
    ("New Delhi","Delhi","North",28.61,77.21,1842,22,"DC Fast"),
    ("Chandigarh","Punjab","North",30.73,76.78,412,31,"AC Type-2"),
    ("Jaipur","Rajasthan","North",26.91,75.79,386,58,"AC Type-2"),
    ("Lucknow","Uttar Pradesh","North",26.85,80.95,298,71,"DC Fast"),
    ("Kanpur","Uttar Pradesh","North",26.45,80.33,164,76,"AC Slow"),
    ("Varanasi","Uttar Pradesh","North",25.32,82.97,142,68,"Bharat DC-001"),
    ("Patna","Bihar","East",25.59,85.14,118,82,"AC Slow"),
    ("Kolkata","West Bengal","East",22.57,88.36,874,38,"DC Fast"),
    ("Bhubaneswar","Odisha","East",20.30,85.82,226,64,"AC Type-2"),
    ("Guwahati","Assam","Northeast",26.14,91.74,132,73,"AC Slow"),
    ("Ahmedabad","Gujarat","West",23.03,72.58,692,29,"DC Fast"),
    ("Surat","Gujarat","West",21.17,72.83,448,34,"AC Type-2"),
    ("Mumbai","Maharashtra","West",19.08,72.88,2140,16,"DC Fast"),
    ("Pune","Maharashtra","West",18.52,73.86,786,24,"DC Fast"),
    ("Nagpur","Maharashtra","Central",21.15,79.09,312,52,"AC Type-2"),
    ("Bhopal","Madhya Pradesh","Central",23.26,77.41,224,61,"AC Slow"),
    ("Indore","Madhya Pradesh","Central",22.72,75.86,268,57,"DC Fast"),
    ("Raipur","Chhattisgarh","Central",21.25,81.63,176,66,"AC Type-2"),
    ("Hyderabad","Telangana","South",17.39,78.49,948,27,"DC Fast"),
    ("Visakhapatnam","Andhra Pradesh","South",17.69,83.22,284,49,"AC Type-2"),
    ("Vijayawada","Andhra Pradesh","South",16.51,80.65,196,54,"Bharat DC-001"),
    ("Bengaluru","Karnataka","South",12.97,77.59,2260,14,"DC Fast"),
    ("Chennai","Tamil Nadu","South",13.08,80.27,1180,21,"DC Fast"),
    ("Coimbatore","Tamil Nadu","South",11.02,76.96,342,44,"AC Type-2"),
    ("Kochi","Kerala","South",9.93,76.27,398,36,"AC Type-2"),
    ("Thiruvananthapuram","Kerala","South",8.52,76.94,286,33,"AC Slow"),
    ("Panaji","Goa","West",15.50,73.83,174,41,"AC Type-2"),
]

CORRIDORS = [
    {"name":"Delhi – Jaipur (NH-48)","sub":"Delhi · Haryana · Rajasthan","stations":84,"gap":34,"util":78,"status":"Operational","sc":"green",
     "lats":[28.61,26.91],"lons":[77.21,75.79]},
    {"name":"Mumbai – Pune Expressway","sub":"Maharashtra","stations":126,"gap":18,"util":86,"status":"Operational","sc":"green",
     "lats":[19.08,18.52],"lons":[72.88,73.86]},
    {"name":"Bengaluru – Mysuru (NH-275)","sub":"Karnataka","stations":62,"gap":26,"util":71,"status":"Operational","sc":"green",
     "lats":[12.97,12.30],"lons":[77.59,76.64]},
    {"name":"Delhi – Lucknow (NH-27)","sub":"Delhi · UP","stations":41,"gap":68,"util":52,"status":"Under Expansion","sc":"amber",
     "lats":[28.61,26.85],"lons":[77.21,80.95]},
    {"name":"Chennai – Coimbatore (NH-544)","sub":"Tamil Nadu","stations":38,"gap":47,"util":64,"status":"Under Expansion","sc":"amber",
     "lats":[13.08,11.02],"lons":[80.27,76.96]},
    {"name":"Kolkata – Durgapur (NH-19)","sub":"West Bengal","stations":22,"gap":74,"util":41,"status":"Critical Gap","sc":"red",
     "lats":[22.57,23.52],"lons":[88.36,87.31]},
    {"name":"Hyderabad – Vijayawada (NH-65)","sub":"Telangana · Andhra Pradesh","stations":29,"gap":61,"util":57,"status":"Under Expansion","sc":"amber",
     "lats":[17.39,16.51],"lons":[78.49,80.65]},
]


@st.cache_data
def load_stations() -> pd.DataFrame:
    df = pd.DataFrame(CITIES, columns=[
        "city","state","region","lat","lon","stations","gap_index","charger_type"
    ])
    # Derived metrics
    df["utilisation"] = (100 - df["gap_index"] * 0.7 + np.random.RandomState(42).randint(-6, 7, len(df))).clip(30, 95).round(0)
    df["online_pct"] = (97 + np.random.RandomState(7).rand(len(df)) * 3).round(1)
    return df


@st.cache_data
def load_sessions() -> pd.DataFrame:
    rng = np.random.RandomState(11)
    dates = pd.date_range(end=datetime.today(), periods=30, freq="D")
    base = 92 + np.arange(30) * 1.9
    sessions = (base + rng.normal(0, 6, 30)).clip(60, 180).round(0)
    util = (48 + np.arange(30) * 0.9 + rng.normal(0, 3, 30)).clip(40, 92).round(0)
    return pd.DataFrame({"date": dates, "sessions_k": sessions, "utilisation_pct": util})


@st.cache_data
def load_gap_states() -> pd.DataFrame:
    return pd.DataFrame([
        {"state":"Bihar","stations":118,"score":82,"color":"#EF4444"},
        {"state":"Uttar Pradesh","stations":604,"score":73,"color":"#EF4444"},
        {"state":"Jharkhand","stations":96,"score":69,"color":"#F59E0B"},
        {"state":"Assam","stations":132,"score":66,"color":"#F59E0B"},
        {"state":"Odisha","stations":226,"score":64,"color":"#F59E0B"},
        {"state":"Madhya Pradesh","stations":492,"score":59,"color":"#F59E0B"},
        {"state":"Rajasthan","stations":386,"score":58,"color":"#F59E0B"},
    ])


@st.cache_data
def load_charger_mix() -> pd.DataFrame:
    return pd.DataFrame([
        {"type":"DC Fast (≥60 kW)","value":7305,"color":"#0E9F6E"},
        {"type":"AC Type-2 (7–22 kW)","value":8809,"color":"#3B82F6"},
        {"type":"AC Slow (3.3 kW)","value":3223,"color":"#94A3B8"},
        {"type":"Bharat DC-001","value":2149,"color":"#F59E0B"},
    ])


@st.cache_data
def load_readiness() -> pd.DataFrame:
    return pd.DataFrame([
        {"region":"South","states":5,"value":88,"target":92,"color":"#0E9F6E"},
        {"region":"West","states":4,"value":79,"target":90,"color":"#0E9F6E"},
        {"region":"North","states":7,"value":71,"target":88,"color":"#3B82F6"},
        {"region":"Central","states":4,"value":52,"target":85,"color":"#F59E0B"},
        {"region":"East","states":5,"value":44,"target":80,"color":"#F59E0B"},
        {"region":"Northeast","states":8,"value":31,"target":75,"color":"#EF4444"},
    ])


# ============================================================
# HELPERS — SVG sparkline + KPI card HTML
# ============================================================

def sparkline_svg(values, color, w=90, h=34):
    vals = [float(v) for v in values]
    if len(vals) < 2:
        return ""
    mn, mx = min(vals), max(vals)
    rng = (mx - mn) or 1
    step = w / (len(vals) - 1)
    pts = [(i * step, h - 3 - ((v - mn) / rng) * (h - 6)) for i, v in enumerate(vals)]
    line = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"{line} L{w},{h} L0,{h} Z"
    gid = "sg" + str(abs(hash(tuple(vals))) % 99999)
    return (
        f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none" width="{w}" height="{h}">'
        f'<defs><linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{color}" stop-opacity="0.28"/>'
        f'<stop offset="100%" stop-color="{color}" stop-opacity="0"/>'
        f'</linearGradient></defs>'
        f'<path d="{area}" fill="url(#{gid})"/>'
        f'<path d="{line}" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
        f'<circle cx="{pts[-1][0]:.1f}" cy="{pts[-1][1]:.1f}" r="2.6" '
        f'fill="{color}" stroke="#fff" stroke-width="1.6"/>'
        f'</svg>'
    )


ICONS = {
    "bolt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4.09 12.69a1 1 0 0 0 .77 1.64H11l-1 7.67 8.91-10.69a1 1 0 0 0-.77-1.64H12l1-7.67Z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/></svg>',
    "alert": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9 2.5 17.4A2 2 0 0 0 4.2 20.4h15.6a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>',
    "chart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v16.5A2.5 2.5 0 0 0 5.5 22H21"/><path d="m7 14 4-5 3.5 3.5L21 6"/></svg>',
    "arrow_up": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" width="11" height="11"><path d="M12 19V5"/><path d="m5 12 7-7 7 7"/></svg>',
    "arrow_down": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" width="11" height="11"><path d="M12 5v14"/><path d="m19 12-7 7-7-7"/></svg>',
}


def kpi_card(icon_key, icon_bg, icon_fg, label, value, unit, delta_text, delta_kind, note, spark_values, spark_color):
    arrow = ICONS["arrow_up"] if delta_kind == "up" else ICONS["arrow_down"] if delta_kind == "down" else ""
    spark = sparkline_svg(spark_values, spark_color)
    return f'''
    <div class="kpi-card">
      <div class="kpi-top">
        <div class="kpi-icon" style="background:{icon_bg};color:{icon_fg}">{ICONS[icon_key]}</div>
        <div class="kpi-delta delta-{delta_kind}">{arrow}{delta_text}</div>
      </div>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}<span class="unit">{unit}</span></div>
      <div class="kpi-foot">
        <div class="kpi-note">{note}</div>
        <div class="kpi-spark">{spark}</div>
      </div>
    </div>
    '''


# ============================================================
# LOAD DATA
# ============================================================
stations_df = load_stations()
sessions_df = load_sessions()
gap_states = load_gap_states()
charger_mix = load_charger_mix()
readiness_df = load_readiness()


# ============================================================
# SIDEBAR FILTERS
# ============================================================
with st.sidebar:
    st.markdown('''
    <div class="brand">
      <div class="brand-mark">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M13 2 4.09 12.69a1 1 0 0 0 .77 1.64H11l-1 7.67 8.91-10.69a1 1 0 0 0-.77-1.64H12l1-7.67Z"/>
        </svg>
      </div>
      <div>
        <div class="brand-name">ChargeWise</div>
        <div class="brand-sub">India · EV Intel</div>
      </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown('<div class="side-label">Filters</div>', unsafe_allow_html=True)

    region_options = ["All India"] + sorted(stations_df["region"].unique().tolist())
    region_choice = st.selectbox("Region", region_options, index=0)

    charger_options = sorted(stations_df["charger_type"].unique().tolist())
    charger_choice = st.multiselect("Charger type", charger_options, default=charger_options)

    min_stations = int(stations_df["stations"].min())
    max_stations = int(stations_df["stations"].max())
    station_range = st.slider("Min. charging points", min_stations, max_stations, min_stations, step=50)

    st.markdown('<div class="side-label">Time period</div>', unsafe_allow_html=True)
    days_back = st.slider("Days of history", 7, 30, 14, step=1)

    st.markdown('<div class="side-label">Display</div>', unsafe_allow_html=True)
    show_gap_zones = st.checkbox("Show gap hotspots", value=True)
    show_corridors = st.checkbox("Show priority corridors", value=True)

    st.markdown("---")
    st.markdown('''
    <div style="background:linear-gradient(160deg,#F3FBF8,#EAF7F2); border:1px solid #D6EEE3; border-radius:14px; padding:14px; margin-top:6px;">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:9px;">
        <div style="font-size:11.5px;font-weight:700;color:#047857;letter-spacing:.2px;">Network Health</div>
        <div class="live-dot"></div>
      </div>
      <div style="font-size:22px;font-weight:800;letter-spacing:-.7px;color:#0B1B33;">98.2<span style="font-size:12px;font-weight:600;color:#64748B;">%</span></div>
      <div style="height:5px;border-radius:20px;background:#D8EEE4;margin-top:10px;overflow:hidden;">
        <div style="height:100%;width:98.2%;border-radius:20px;background:linear-gradient(90deg,#0E9F6E,#34D399);"></div>
      </div>
      <div style="font-size:11px;color:#64748B;margin-top:8px;">21,486 of 21,880 points online</div>
    </div>
    ''', unsafe_allow_html=True)


# ============================================================
# APPLY FILTERS
# ============================================================
filtered = stations_df.copy()
if region_choice != "All India":
    filtered = filtered[filtered["region"] == region_choice]
if charger_choice:
    filtered = filtered[filtered["charger_type"].isin(charger_choice)]
filtered = filtered[filtered["stations"] >= station_range]

# Sessions filtered by day count
sessions_show = sessions_df.tail(days_back).copy()


# ============================================================
# HEADER
# ============================================================
total_stations = int(filtered["stations"].sum())
n_states = filtered["state"].nunique()
avg_gap = round(filtered["gap_index"].mean(), 1) if len(filtered) else 0
total_sessions = round(sessions_show["sessions_k"].sum(), 1)
avg_util = round(sessions_show["utilisation_pct"].mean(), 1) if len(sessions_show) else 0

region_label = region_choice if region_choice != "All India" else "All India"
charger_label = "All Types" if len(charger_choice) == len(charger_options) else f"{len(charger_choice)} types"

st.markdown(f'''
<div class="page-header">
  <div class="page-title">
    <h1>National Overview</h1>
    <p>Real-time EV infrastructure coverage &amp; charging gap analysis across {region_label} · {charger_label}</p>
  </div>
  <div class="live-chip"><span class="live-dot"></span> Live · updated just now</div>
</div>
''', unsafe_allow_html=True)


# ============================================================
# KPI ROW
# ============================================================
kpi_html = '<div class="kpi-grid">'
kpi_html += kpi_card(
    "bolt", "#E8F7F1", "#047857",
    "Total Charging Points",
    f"{total_stations:,}",
    "",
    "+12.4%", "up",
    f"<b>{len(filtered)}</b> cities in view",
    [12,14,13,16,18,17,21,20,24,23,27,29],
    "#0E9F6E",
)
kpi_html += kpi_card(
    "pin", "#EAF2FE", "#1D4ED8",
    "States & UTs Covered",
    f"{n_states}",
    " / 36",
    f"+{max(1, n_states//14)}", "up",
    f"<b>{round(n_states/36*100,1)}%</b> national coverage",
    [14,15,16,17,18,19,20,22,23,25,26,n_states],
    "#3B82F6",
)
kpi_html += kpi_card(
    "alert", "#FEF4E3", "#B45309",
    "Avg. Charging Gap Index",
    f"{avg_gap}",
    "",
    "−3.2 pts", "down",
    "Moderate deficit · <b>improving</b>",
    [58,56,55,53,52,50,49,48,47,45,44,avg_gap],
    "#F59E0B",
)
kpi_html += kpi_card(
    "chart", "#F3EEFE", "#6D28D9",
    f"Charging Sessions · {days_back}d",
    f"{total_sessions:,}",
    "K",
    "+8.1%", "up",
    f"<b>{avg_util}%</b> avg utilisation",
    [88,92,86,98,105,101,112,108,119,124,121,128],
    "#8B5CF6",
)
kpi_html += '</div>'
st.markdown(kpi_html, unsafe_allow_html=True)


# ============================================================
# ROW 1 — MAP + GAP PANEL
# ============================================================
col_map, col_gap = st.columns([1.65, 1], gap="medium")

with col_map:
    st.markdown('''
    <div class="section-head" style="margin-bottom:8px;">
      <div>
        <h3>Infrastructure Coverage Map</h3>
        <p>Station density, gap hotspots &amp; priority corridors</p>
      </div>
    </div>
    ''', unsafe_allow_html=True)

    # Build Plotly geo map
    fig = go.Figure()

    # Gap zones (big translucent circles)
    if show_gap_zones:
        for _, row in filtered.iterrows():
            if row["gap_index"] >= 65:
                col = "rgba(239,68,68,0.18)"
                line_col = "rgba(239,68,68,0.35)"
            elif row["gap_index"] >= 45:
                col = "rgba(245,158,11,0.16)"
                line_col = "rgba(245,158,11,0.32)"
            else:
                col = "rgba(16,185,129,0.12)"
                line_col = "rgba(16,185,129,0.28)"
            fig.add_trace(go.Scattergeo(
                lat=[row["lat"]],
                lon=[row["lon"]],
                mode="markers",
                marker=dict(
                    size=max(30, row["stations"] / 12),
                    color=col,
                    line=dict(color=line_col, width=1),
                ),
                hoverinfo="skip",
                showlegend=False,
            ))

    # Corridor lines
    if show_corridors:
        for c in CORRIDORS:
            fig.add_trace(go.Scattergeo(
                lat=c["lats"], lon=c["lons"],
                mode="lines",
                line=dict(color="#0E9F6E", width=2, dash="dot"),
                hoverinfo="skip",
                showlegend=False,
                opacity=0.75,
            ))

    # Station markers
    if len(filtered):
        fig.add_trace(go.Scattergeo(
            lat=filtered["lat"],
            lon=filtered["lon"],
            mode="markers",
            text=filtered["city"],
            customdata=np.stack([
                filtered["state"],
                filtered["stations"],
                filtered["gap_index"],
                filtered["charger_type"],
            ], axis=-1),
            marker=dict(
                size=(filtered["stations"] ** 0.55) / 1.6 + 8,
                color=filtered["gap_index"],
                colorscale=[
                    [0.0, "#10B981"],
                    [0.45, "#F59E0B"],
                    [1.0, "#EF4444"],
                ],
                cmin=0, cmax=100,
                line=dict(color="#ffffff", width=1.6),
                opacity=0.95,
                colorbar=dict(
                    title=dict(text="Gap", font=dict(size=10, color="#64748B")),
                    thickness=8,
                    len=0.55,
                    x=0.99,
                    tickfont=dict(size=9, color="#94A3B8"),
                    outlinewidth=0,
                ),
            ),
            hovertemplate=(
                "<b>%{text}</b><br>"
                "%{customdata[0]}<br>"
                "Stations: <b>%{customdata[1]}</b><br>"
                "Gap index: <b>%{customdata[2]}</b><br>"
                "Type: %{customdata[3]}"
                "<extra></extra>"
            ),
            showlegend=False,
        ))

    fig.update_geos(
        scope="asia",
        center=dict(lat=22.5, lon=79),
        projection=dict(type="mercator", scale=4.6),
        showland=True, landcolor="#F1F8F5",
        showocean=True, oceancolor="#F8FBFE",
        showcountries=True, countrycolor="#D6E5DE",
        showcoastlines=True, coastlinecolor="#C9DDD4", coastlinewidth=0.8,
        showframe=False,
        bgcolor="rgba(0,0,0,0)",
        lataxis=dict(range=[5, 37], showgrid=False),
        lonaxis=dict(range=[66, 98], showgrid=False),
    )
    fig.update_layout(
        height=520,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=11, color="#0B1B33"),
        hoverlabel=dict(
            bgcolor="#0B1B33",
            bordercolor="#0B1B33",
            font=dict(color="#fff", family="Inter, sans-serif", size=12),
        ),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


with col_gap:
    st.markdown(f'''
    <div class="section-head" style="margin-bottom:8px;">
      <div>
        <h3>Charging Gap Index</h3>
        <p>Composite deficit score by state</p>
      </div>
      <span class="pill pill-amber">Action needed</span>
    </div>

    <div class="gap-hero">
      <div>
        <div class="gap-big-num">{avg_gap}</div>
        <div class="gap-big-sub">Moderate</div>
      </div>
      <div class="gap-hero-text">
        <h4>National deficit trending down</h4>
        <p>7 states remain below the 60% adequacy threshold. Bihar &amp; Jharkhand show the steepest shortfall.</p>
      </div>
    </div>
    ''', unsafe_allow_html=True)

    # Horizontal bar chart of gap states
    gap_sorted = gap_states.sort_values("score", ascending=True)
    fig_gap = go.Figure()
    fig_gap.add_trace(go.Bar(
        x=gap_sorted["score"],
        y=gap_sorted["state"],
        orientation="h",
        marker=dict(
            color=gap_sorted["color"],
            line=dict(width=0),
        ),
        text=[f"<b>{s}</b>" for s in gap_sorted["score"]],
        textposition="outside",
        textfont=dict(color="#0B1B33", size=12, family="Inter, sans-serif"),
        hovertemplate="<b>%{y}</b><br>Gap index: %{x}<extra></extra>",
        width=0.62,
    ))
    fig_gap.update_layout(
        height=280,
        margin=dict(l=0, r=30, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=11, color="#0B1B33"),
        xaxis=dict(
            range=[0, 100],
            showgrid=True, gridcolor="#F1F5F9", zeroline=False,
            showline=False, ticks="",
            tickfont=dict(size=10, color="#94A3B8"),
        ),
        yaxis=dict(
            showgrid=False, zeroline=False,
            tickfont=dict(size=11.5, color="#1D2E48"),
        ),
        bargap=0.35,
        hoverlabel=dict(bgcolor="#0B1B33", font=dict(color="#fff", family="Inter, sans-serif")),
    )
    st.plotly_chart(fig_gap, use_container_width=True, config={"displayModeBar": False})


# ============================================================
# ROW 2 — SESSIONS AREA CHART + (DONUT + READINESS)
# ============================================================
col_sessions, col_right = st.columns([1.6, 1], gap="medium")

with col_sessions:
    st.markdown('''
    <div class="section-head" style="margin-bottom:8px;">
      <div>
        <h3>Charging Sessions &amp; Grid Utilisation</h3>
        <p>Daily session volume against average charger utilisation</p>
      </div>
    </div>
    ''', unsafe_allow_html=True)

    fig_area = make_subplots(specs=[[{"secondary_y": True}]])

    fig_area.add_trace(
        go.Scatter(
            x=sessions_show["date"],
            y=sessions_show["sessions_k"],
            name="Sessions (K)",
            mode="lines",
            line=dict(color="#0E9F6E", width=2.6, shape="spline"),
            fill="tozeroy",
            fillcolor="rgba(14,159,110,0.14)",
            hovertemplate="<b>%{x|%b %d}</b><br>Sessions: %{y}K<extra></extra>",
        ),
        secondary_y=False,
    )
    fig_area.add_trace(
        go.Scatter(
            x=sessions_show["date"],
            y=sessions_show["utilisation_pct"],
            name="Utilisation (%)",
            mode="lines",
            line=dict(color="#1D2E48", width=1.9, dash="dash"),
            hovertemplate="<b>%{x|%b %d}</b><br>Utilisation: %{y}%<extra></extra>",
        ),
        secondary_y=True,
    )

    fig_area.update_layout(
        height=340,
        margin=dict(l=0, r=0, t=8, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=11, color="#0B1B33"),
        showlegend=False,
        hovermode="x unified",
        hoverlabel=dict(bgcolor="#0B1B33", font=dict(color="#fff", family="Inter, sans-serif")),
        xaxis=dict(
            showgrid=False, zeroline=False, showline=False, ticks="",
            tickfont=dict(size=10.5, color="#94A3B8"),
            tickformat="%b %d",
        ),
        yaxis=dict(
            showgrid=True, gridcolor="#F1F5F9", zeroline=False, showline=False, ticks="",
            tickfont=dict(size=10.5, color="#94A3B8"),
            title=dict(text="Sessions (K)", font=dict(size=10.5, color="#94A3B8")),
        ),
        yaxis2=dict(
            showgrid=False, zeroline=False, showline=False, ticks="",
            tickfont=dict(size=10.5, color="#94A3B8"),
            title=dict(text="Utilisation (%)", font=dict(size=10.5, color="#94A3B8")),
            range=[30, 100],
        ),
    )
    st.plotly_chart(fig_area, use_container_width=True, config={"displayModeBar": False})


with col_right:
    # ---- Donut chart ----
    st.markdown('''
    <div class="section-head" style="margin-bottom:6px;">
      <div>
        <h3>Charger Type Mix</h3>
        <p>Nationwide distribution</p>
      </div>
    </div>
    ''', unsafe_allow_html=True)

    fig_donut = go.Figure()
    fig_donut.add_trace(go.Pie(
        values=charger_mix["value"],
        labels=charger_mix["type"],
        hole=0.68,
        marker=dict(
            colors=charger_mix["color"],
            line=dict(color="#FFFFFF", width=3),
        ),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{value:,} points<br>%{percent}<extra></extra>",
        sort=False,
        direction="clockwise",
    ))

    total_points = int(charger_mix["value"].sum())
    fig_donut.update_layout(
        height=250,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=11, color="#0B1B33"),
        showlegend=False,
        hoverlabel=dict(bgcolor="#0B1B33", font=dict(color="#fff", family="Inter, sans-serif")),
        annotations=[
            dict(
                text=f"<b style='font-size:22px;color:#0B1B33;'>{total_points:,}</b><br>"
                     f"<span style='font-size:10px;color:#94A3B8;letter-spacing:0.5px;'>TOTAL POINTS</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(family="Inter, sans-serif"),
            )
        ],
    )
    st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

    # Legend under donut
    legend_html = '<div style="display:flex;flex-direction:column;gap:2px;margin-top:-8px;">'
    total_val = charger_mix["value"].sum()
    for _, row in charger_mix.iterrows():
        pct = round(row["value"] / total_val * 100)
        legend_html += f'''
        <div style="display:flex;align-items:center;gap:10px;padding:6px 8px;border-radius:9px;">
          <span style="width:9px;height:9px;border-radius:3px;background:{row["color"]};flex-shrink:0;"></span>
          <span style="font-size:12px;font-weight:550;color:#1D2E48;flex:1;">{row["type"]}</span>
          <span style="font-size:12px;font-weight:700;color:#0B1B33;font-variant-numeric:tabular-nums;">{row["value"]:,}</span>
          <span style="font-size:11px;color:#94A3B8;font-weight:600;min-width:34px;text-align:right;font-variant-numeric:tabular-nums;">{pct}%</span>
        </div>
        '''
    legend_html += '</div>'
    st.markdown(legend_html, unsafe_allow_html=True)

    st.markdown('<hr style="margin: 16px 0;"/>', unsafe_allow_html=True)

    # ---- Readiness bars ----
    st.markdown('''
    <div class="section-head" style="margin-bottom:10px;">
      <div>
        <h3>Regional Readiness</h3>
        <p>Coverage vs. 2027 target</p>
      </div>
    </div>
    ''', unsafe_allow_html=True)

    readiness_html = '<div style="display:flex;flex-direction:column;gap:14px;">'
    for _, r in readiness_df.iterrows():
        readiness_html += f'''
        <div>
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:7px;">
            <div style="font-size:12.3px;font-weight:600;color:#0B1B33;">
              {r["region"]} <em style="font-style:normal;font-size:10.5px;color:#94A3B8;font-weight:550;margin-left:5px;">{int(r["states"])} states</em>
            </div>
            <div style="font-size:12.3px;font-weight:750;color:{r["color"]};font-variant-numeric:tabular-nums;">{int(r["value"])}%</div>
          </div>
          <div style="height:7px;border-radius:20px;background:#F1F5F9;position:relative;">
            <div style="height:100%;width:{r["value"]}%;border-radius:20px;background:linear-gradient(90deg,{r["color"]}AA,{r["color"]});animation: growBar 1.2s cubic-bezier(.22,1,.36,1) both;"></div>
            <div style="position:absolute;top:-3px;left:{r["target"]}%;width:2px;height:13px;background:#0B1B33;border-radius:2px;opacity:.28;"></div>
          </div>
        </div>
        '''
    readiness_html += '</div>'
    st.markdown(readiness_html, unsafe_allow_html=True)


# ============================================================
# ROW 3 — CORRIDOR TABLE
# ============================================================
st.markdown('<hr/>', unsafe_allow_html=True)
st.markdown('''
<div class="section-head" style="margin-bottom:12px;">
  <div>
    <h3>Priority Charging Corridors</h3>
    <p>Highway corridors ranked by infrastructure gap severity &amp; traffic potential</p>
  </div>
</div>
''', unsafe_allow_html=True)

status_map = {
    "green": ("#E8F7F1", "#047857", "#10B981"),
    "amber": ("#FEF4E3", "#B45309", "#F59E0B"),
    "red":   ("#FEECEC", "#C0392B", "#EF4444"),
}

rows_html = ""
for c in CORRIDORS:
    bg, fg, dot = status_map[c["sc"]]
    gap_col = "#EF4444" if c["gap"] >= 65 else "#F59E0B" if c["gap"] >= 45 else "#10B981"
    rows_html += f'''
    <tr>
      <td>
        <div class="corridor-name">{c["name"]}</div>
        <div class="corridor-sub">{c["sub"]}</div>
      </td>
      <td class="cell-num">{c["stations"]}</td>
      <td>
        <span class="mini-bar"><i style="width:{c["gap"]}%;background:{gap_col};"></i></span>
        <span class="cell-num" style="color:{gap_col};">{c["gap"]}</span>
      </td>
      <td>
        <span class="mini-bar"><i style="width:{c["util"]}%;background:#0E9F6E;"></i></span>
        <span class="cell-num">{c["util"]}%</span>
      </td>
      <td>
        <span class="status-pill" style="background:{bg};color:{fg};">
          <span class="sdot" style="background:{dot};"></span>{c["status"]}
        </span>
      </td>
    </tr>
    '''

st.markdown(f'''
<table class="corridor-table">
  <thead>
    <tr>
      <th>Corridor</th>
      <th>Stations</th>
      <th>Gap Index</th>
      <th>Utilisation</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    {rows_html}
  </tbody>
</table>
''', unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================
st.markdown(f'''
<div style="margin-top:28px; padding-top:18px; border-top:1px solid #E7ECF2;
            display:flex; align-items:center; justify-content:space-between;
            font-size:11.5px; color:#94A3B8; font-weight:500;">
  <div>ChargeWise India · EV Infrastructure Intelligence Platform</div>
  <div>Last updated {datetime.now().strftime("%d %b %Y · %H:%M")} · {len(filtered)} cities in view</div>
</div>
''', unsafe_allow_html=True)
