"""
ChargeWise India — EV Infrastructure Mapping and Charging Gap Analysis Platform
Streamlit wrapper around the ChargeWise dashboard.
"""

import streamlit as st
import streamlit.components.v1 as components


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="ChargeWise India — EV Infrastructure Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------------------------
# Hide Streamlit chrome so the iframe is full-bleed
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
        #MainMenu, header[data-testid="stHeader"], footer {visibility: hidden; height: 0;}
        .block-container {padding: 0 !important; max-width: 100% !important;}
        section.main > div {padding: 0 !important;}
        iframe[title="streamlit_component"] {display: block; width: 100%; border: none;}
        body {margin: 0;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# The full ChargeWise dashboard (HTML + CSS + JS, self-contained)
# ---------------------------------------------------------------------------
DASHBOARD_HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>ChargeWise India — EV Infrastructure Intelligence</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#F6F8FB;
  --surface:#FFFFFF;
  --surface-2:#F8FAFC;
  --surface-3:#F1F5F9;
  --border:#E7ECF2;
  --border-2:#DCE3EC;
  --navy:#0B1B33;
  --navy-2:#1D2E48;
  --muted:#64748B;
  --muted-2:#94A3B8;
  --green:#0E9F6E;
  --green-d:#047857;
  --green-l:#E8F7F1;
  --green-l2:#D3F0E4;
  --amber:#F59E0B;
  --amber-l:#FEF4E3;
  --red:#EF4444;
  --red-l:#FEECEC;
  --blue:#3B82F6;
  --blue-l:#EAF2FE;
  --violet:#8B5CF6;
  --slate:#94A3B8;

  --r-sm:10px;
  --r:14px;
  --r-lg:18px;
  --r-xl:22px;

  --sh-xs:0 1px 2px rgba(16,24,40,.05);
  --sh-sm:0 1px 3px rgba(16,24,40,.06), 0 1px 2px rgba(16,24,40,.03);
  --sh-md:0 4px 14px -4px rgba(16,24,40,.10), 0 2px 5px -2px rgba(16,24,40,.05);
  --sh-lg:0 22px 48px -18px rgba(11,27,51,.22), 0 6px 16px -8px rgba(11,27,51,.10);
  --sh-glow:0 8px 24px -8px rgba(14,159,110,.45);
}

*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}

body{
  font-family:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:var(--bg);
  color:var(--navy);
  -webkit-font-smoothing:antialiased;
  -moz-osx-font-smoothing:grayscale;
  display:grid;
  grid-template-columns:256px minmax(0,1fr);
  height:100vh;
  overflow:hidden;
  font-size:14px;
  line-height:1.5;
}

::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:#D8E0EA;border-radius:20px;border:3px solid var(--bg)}
::-webkit-scrollbar-thumb:hover{background:#C3CEDB}

.sidebar{
  background:var(--surface);
  border-right:1px solid var(--border);
  display:flex;
  flex-direction:column;
  padding:22px 14px 18px;
  overflow-y:auto;
  position:relative;
  z-index:30;
}
.brand{
  display:flex;align-items:center;gap:11px;
  padding:0 8px 4px;
  margin-bottom:26px;
}
.brand-mark{
  width:38px;height:38px;border-radius:11px;
  background:linear-gradient(145deg,#0E9F6E,#0B8A5F);
  display:grid;place-items:center;
  box-shadow:var(--sh-glow);
  flex-shrink:0;
}
.brand-mark svg{width:20px;height:20px;color:#fff}
.brand-name{font-size:15.5px;font-weight:800;letter-spacing:-.3px;line-height:1.15}
.brand-sub{font-size:10.5px;color:var(--muted-2);font-weight:500;letter-spacing:.25px;text-transform:uppercase;margin-top:1px}

.nav-label{
  font-size:10px;font-weight:700;letter-spacing:.9px;text-transform:uppercase;
  color:var(--muted-2);padding:0 10px;margin:4px 0 8px;
}
.nav{display:flex;flex-direction:column;gap:2px;margin-bottom:22px}
.nav-item{
  display:flex;align-items:center;gap:11px;
  padding:9.5px 11px;border-radius:11px;
  color:var(--muted);font-weight:550;font-size:13.5px;
  cursor:pointer;border:none;background:none;width:100%;
  text-align:left;font-family:inherit;position:relative;
  transition:background .18s ease,color .18s ease;
}
.nav-item svg{width:17px;height:17px;flex-shrink:0;stroke-width:1.9}
.nav-item:hover{background:var(--surface-3);color:var(--navy-2)}
.nav-item.active{background:var(--green-l);color:var(--green-d);font-weight:650}
.nav-item.active::before{
  content:'';position:absolute;left:-14px;top:50%;transform:translateY(-50%);
  width:3px;height:20px;border-radius:0 4px 4px 0;background:var(--green);
}
.nav-badge{
  margin-left:auto;font-size:10.5px;font-weight:700;
  background:var(--green);color:#fff;border-radius:20px;
  padding:1.5px 7px;line-height:1.5;
}

.sidebar-foot{margin-top:auto;display:flex;flex-direction:column;gap:12px}
.health-card{
  background:linear-gradient(160deg,#F3FBF8,#EAF7F2);
  border:1px solid #D6EEE3;
  border-radius:var(--r);
  padding:14px;
}
.health-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:9px}
.health-title{font-size:11.5px;font-weight:700;color:var(--green-d);letter-spacing:.2px}
.live-dot{
  width:7px;height:7px;border-radius:50%;background:var(--green);
  box-shadow:0 0 0 0 rgba(14,159,110,.5);
  animation:livePulse 2s infinite;
}
@keyframes livePulse{
  0%{box-shadow:0 0 0 0 rgba(14,159,110,.45)}
  70%{box-shadow:0 0 0 7px rgba(14,159,110,0)}
  100%{box-shadow:0 0 0 0 rgba(14,159,110,0)}
}
.health-val{font-size:22px;font-weight:800;letter-spacing:-.7px;color:var(--navy);font-variant-numeric:tabular-nums}
.health-val span{font-size:12px;font-weight:600;color:var(--muted);letter-spacing:0}
.health-bar{height:5px;border-radius:20px;background:#D8EEE4;margin-top:10px;overflow:hidden}
.health-bar i{display:block;height:100%;width:0;border-radius:20px;background:linear-gradient(90deg,#0E9F6E,#34D399);transition:width 1.4s cubic-bezier(.22,1,.36,1)}
.health-meta{font-size:11px;color:var(--muted);margin-top:8px}

.user-card{
  display:flex;align-items:center;gap:10px;
  padding:9px 10px;border-radius:12px;border:1px solid var(--border);
  background:var(--surface-2);cursor:pointer;transition:.18s;
}
.user-card:hover{background:var(--surface-3);border-color:var(--border-2)}
.avatar{
  width:32px;height:32px;border-radius:10px;flex-shrink:0;
  background:linear-gradient(140deg,#1D2E48,#0B1B33);
  color:#fff;display:grid;place-items:center;
  font-size:11.5px;font-weight:700;letter-spacing:.3px;
}
.user-name{font-size:12.5px;font-weight:650;line-height:1.2}
.user-role{font-size:10.5px;color:var(--muted-2);font-weight:500}

.main{
  overflow-y:auto;
  padding:0 30px 44px;
  background:
    radial-gradient(1100px 420px at 12% -8%, rgba(14,159,110,.055), transparent 62%),
    radial-gradient(900px 380px at 92% -12%, rgba(59,130,246,.045), transparent 60%),
    var(--bg);
}

.topbar{
  position:sticky;top:0;z-index:25;
  display:flex;align-items:flex-end;justify-content:space-between;gap:24px;
  padding:24px 0 18px;
  background:linear-gradient(180deg,rgba(246,248,251,.96) 62%,rgba(246,248,251,0));
  backdrop-filter:blur(14px);
  -webkit-backdrop-filter:blur(14px);
}
.page-title h1{
  font-size:23px;font-weight:800;letter-spacing:-.65px;line-height:1.15;
}
.page-title p{font-size:12.8px;color:var(--muted);margin-top:5px;font-weight:450}
.topbar-actions{display:flex;align-items:center;gap:10px;flex-shrink:0}

.search{
  display:flex;align-items:center;gap:8px;
  background:var(--surface);border:1px solid var(--border);
  border-radius:11px;padding:0 12px;height:38px;width:250px;
  transition:.2s;box-shadow:var(--sh-xs);
}
.search:focus-within{border-color:var(--green);box-shadow:0 0 0 3.5px rgba(14,159,110,.11)}
.search svg{width:15px;height:15px;color:var(--muted-2);flex-shrink:0}
.search input{
  border:none;outline:none;background:none;font-family:inherit;
  font-size:13px;color:var(--navy);width:100%;font-weight:500;
}
.search input::placeholder{color:var(--muted-2);font-weight:450}
.kbd{
  font-size:10px;font-weight:600;color:var(--muted-2);
  border:1px solid var(--border-2);border-radius:5px;
  padding:1px 5px;background:var(--surface-2);flex-shrink:0;
}

.icon-btn{
  width:38px;height:38px;border-radius:11px;
  border:1px solid var(--border);background:var(--surface);
  display:grid;place-items:center;cursor:pointer;
  color:var(--muted);transition:.18s;position:relative;box-shadow:var(--sh-xs);
}
.icon-btn:hover{background:var(--surface-3);color:var(--navy);border-color:var(--border-2)}
.icon-btn svg{width:17px;height:17px;stroke-width:1.9}
.icon-btn .dot{
  position:absolute;top:8px;right:9px;width:6px;height:6px;border-radius:50%;
  background:var(--red);border:1.5px solid #fff;
}
.live-chip{
  display:flex;align-items:center;gap:7px;height:38px;padding:0 14px;
  border-radius:11px;background:var(--green-l);border:1px solid #CBEBDE;
  font-size:12.5px;font-weight:650;color:var(--green-d);
}
.live-chip .live-dot{background:var(--green)}

.filterbar{
  display:flex;align-items:center;gap:10px;flex-wrap:wrap;
  margin-bottom:20px;
}
.filter{
  display:flex;align-items:center;gap:8px;
  background:var(--surface);border:1px solid var(--border);
  border-radius:11px;height:38px;padding:0 12px;
  font-size:12.8px;font-weight:550;color:var(--navy-2);
  cursor:pointer;transition:.18s;box-shadow:var(--sh-xs);
  font-family:inherit;
}
.filter:hover{border-color:var(--border-2);background:var(--surface-2)}
.filter svg{width:14px;height:14px;color:var(--muted-2);stroke-width:2}
.filter .chev{width:12px;height:12px;color:var(--muted-2);margin-left:2px}
.filter-label{color:var(--muted-2);font-weight:500;font-size:11.5px;text-transform:uppercase;letter-spacing:.4px}
.filter strong{font-weight:650;color:var(--navy)}
.btn-primary{
  margin-left:auto;display:flex;align-items:center;gap:8px;
  height:38px;padding:0 18px;border-radius:11px;border:none;
  background:linear-gradient(145deg,#0E9F6E,#0B8A5F);
  color:#fff;font-size:13px;font-weight:650;font-family:inherit;
  cursor:pointer;box-shadow:var(--sh-glow);transition:.2s;
}
.btn-primary:hover{transform:translateY(-1px);box-shadow:0 12px 26px -8px rgba(14,159,110,.55)}
.btn-primary:active{transform:translateY(0)}
.btn-primary svg{width:15px;height:15px;stroke-width:2.2}

.card{
  background:var(--surface);
  border:1px solid var(--border);
  border-radius:var(--r-lg);
  box-shadow:var(--sh-sm);
  padding:20px;
  transition:box-shadow .25s ease, border-color .25s ease;
  position:relative;
}
.card:hover{box-shadow:var(--sh-md)}
.card-head{
  display:flex;align-items:flex-start;justify-content:space-between;
  gap:16px;margin-bottom:18px;
}
.card-head h3{font-size:14.5px;font-weight:700;letter-spacing:-.25px}
.card-head p{font-size:12px;color:var(--muted);margin-top:3px;font-weight:450}

.kpis{
  display:grid;grid-template-columns:repeat(4,minmax(0,1fr));
  gap:16px;margin-bottom:20px;
}
.kpi{
  background:var(--surface);border:1px solid var(--border);
  border-radius:var(--r-lg);padding:18px 18px 14px;
  box-shadow:var(--sh-sm);position:relative;overflow:hidden;
  transition:.25s cubic-bezier(.22,1,.36,1);
}
.kpi::after{
  content:'';position:absolute;inset:0;border-radius:inherit;pointer-events:none;
  background:linear-gradient(180deg,rgba(14,159,110,.05),transparent 55%);
  opacity:0;transition:opacity .3s;
}
.kpi:hover{transform:translateY(-3px);box-shadow:var(--sh-lg);border-color:var(--border-2)}
.kpi:hover::after{opacity:1}
.kpi-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}
.kpi-icon{
  width:38px;height:38px;border-radius:12px;display:grid;place-items:center;
}
.kpi-icon svg{width:18px;height:18px;stroke-width:2}
.kpi-delta{
  display:flex;align-items:center;gap:4px;
  font-size:11.5px;font-weight:700;padding:3px 8px;border-radius:20px;
}
.kpi-delta svg{width:11px;height:11px;stroke-width:2.6}
.delta-up{background:var(--green-l);color:var(--green-d)}
.delta-down{background:var(--red-l);color:#C0392B}
.delta-flat{background:var(--surface-3);color:var(--muted)}

.kpi-label{font-size:12.2px;font-weight:550;color:var(--muted);margin-bottom:6px;letter-spacing:.1px}
.kpi-value{
  font-size:29px;font-weight:800;letter-spacing:-1.1px;
  line-height:1.05;font-variant-numeric:tabular-nums;
}
.kpi-value .unit{font-size:15px;font-weight:650;color:var(--muted);letter-spacing:-.3px;margin-left:2px}
.kpi-foot{
  display:flex;align-items:flex-end;justify-content:space-between;
  margin-top:12px;gap:12px;
}
.kpi-note{font-size:11.2px;color:var(--muted-2);font-weight:500;line-height:1.4}
.kpi-note b{color:var(--muted);font-weight:650}
.spark{width:88px;height:34px;flex-shrink:0}
.spark svg{display:block;width:100%;height:100%;overflow:visible}

.grid-main{
  display:grid;grid-template-columns:minmax(0,1.62fr) minmax(0,1fr);
  gap:18px;margin-bottom:18px;
}
.grid-split{
  display:grid;grid-template-columns:minmax(0,1.68fr) minmax(0,1fr);
  gap:18px;margin-bottom:18px;
}
.col-stack{display:flex;flex-direction:column;gap:18px}

.seg{
  display:flex;gap:3px;background:var(--surface-3);
  padding:3px;border-radius:10px;flex-shrink:0;
}
.seg-btn{
  border:none;background:none;font-family:inherit;
  font-size:11.8px;font-weight:600;color:var(--muted);
  padding:6px 11px;border-radius:7px;cursor:pointer;
  transition:.18s;white-space:nowrap;
}
.seg-btn:hover{color:var(--navy)}
.seg-btn.active{background:var(--surface);color:var(--green-d);box-shadow:var(--sh-xs)}

.map-wrap{
  position:relative;border-radius:var(--r);
  background:
    radial-gradient(700px 420px at 50% 40%, #FBFDFC 0%, #F7FAF9 60%, #F4F8F7 100%);
  border:1px solid #EDF2F0;
  overflow:hidden;
  padding:6px;
}
.map-wrap::before{
  content:'';position:absolute;inset:0;
  background-image:
    linear-gradient(rgba(148,163,184,.07) 1px, transparent 1px),
    linear-gradient(90deg, rgba(148,163,184,.07) 1px, transparent 1px);
  background-size:34px 34px;
  mask-image:radial-gradient(ellipse 78% 72% at 50% 46%, #000 42%, transparent 100%);
  -webkit-mask-image:radial-gradient(ellipse 78% 72% at 50% 46%, #000 42%, transparent 100%);
  pointer-events:none;
}
#indiaMap{display:block;width:100%;height:auto;position:relative;z-index:1}

.india-land{
  fill:url(#landGrad);
  stroke:#C9E2D8;
  stroke-width:1.6;
  stroke-linejoin:round;
  filter:drop-shadow(0 10px 22px rgba(11,27,51,.07));
}
.gap-zone{opacity:.55;mix-blend-mode:multiply;transition:opacity .3s}
.gap-zone.hidden{opacity:0}
.corridor{
  fill:none;stroke:#0E9F6E;stroke-width:2.1;
  stroke-dasharray:6 5;stroke-linecap:round;opacity:.6;
  animation:dashFlow 22s linear infinite;
  transition:opacity .3s;
}
@keyframes dashFlow{to{stroke-dashoffset:-220}}
.corridor.hidden{opacity:0}

.station{cursor:pointer;transition:opacity .3s}
.station.hidden{opacity:0;pointer-events:none}
.station .pulse{
  transform-box:fill-box;transform-origin:center;
  animation:pulseRing 2.8s cubic-bezier(.2,.6,.4,1) infinite;
}
.station:nth-child(3n) .pulse{animation-delay:.6s}
.station:nth-child(3n+1) .pulse{animation-delay:1.2s}
@keyframes pulseRing{
  0%{transform:scale(.35);opacity:.65}
  75%{transform:scale(2.6);opacity:0}
  100%{transform:scale(2.6);opacity:0}
}
.station .halo{transition:r .3s ease, opacity .3s ease}
.station .core{transition:r .25s ease, stroke-width .25s ease}
.station:hover .core{r:6.4;stroke-width:2.6}

.legend{
  position:absolute;left:14px;bottom:14px;z-index:4;
  background:rgba(255,255,255,.9);
  backdrop-filter:blur(10px);
  border:1px solid var(--border);
  border-radius:11px;padding:10px 13px;
  display:flex;flex-direction:column;gap:7px;
  box-shadow:var(--sh-sm);
}
.legend-title{
  font-size:9.5px;font-weight:700;letter-spacing:.7px;
  text-transform:uppercase;color:var(--muted-2);margin-bottom:1px;
}
.legend-item{display:flex;align-items:center;gap:8px;font-size:11.3px;font-weight:550;color:var(--navy-2)}
.legend-swatch{width:9px;height:9px;border-radius:50%;flex-shrink:0}

.map-stat{
  position:absolute;right:14px;top:14px;z-index:4;
  background:rgba(255,255,255,.92);
  backdrop-filter:blur(10px);
  border:1px solid var(--border);border-radius:12px;
  padding:11px 14px;box-shadow:var(--sh-sm);
  display:flex;flex-direction:column;gap:9px;min-width:150px;
}
.ms-row{display:flex;align-items:center;justify-content:space-between;gap:16px}
.ms-label{font-size:11px;color:var(--muted);font-weight:550}
.ms-val{font-size:13px;font-weight:750;font-variant-numeric:tabular-nums;letter-spacing:-.2px}

.map-foot{
  display:flex;align-items:center;gap:16px;
  margin-top:16px;padding-top:16px;border-top:1px solid var(--border);
}
.map-foot label{font-size:12px;font-weight:600;color:var(--navy-2);white-space:nowrap}
.range-wrap{flex:1;display:flex;align-items:center;gap:12px}
input[type=range]{
  -webkit-appearance:none;appearance:none;
  width:100%;height:4px;border-radius:20px;
  background:linear-gradient(90deg,var(--green) var(--fill,50%),var(--surface-3) var(--fill,50%));
  outline:none;cursor:pointer;
}
input[type=range]::-webkit-slider-thumb{
  -webkit-appearance:none;appearance:none;
  width:16px;height:16px;border-radius:50%;
  background:#fff;border:3px solid var(--green);
  box-shadow:0 2px 6px rgba(14,159,110,.35);cursor:grab;
  transition:transform .15s;
}
input[type=range]::-webkit-slider-thumb:hover{transform:scale(1.15)}
input[type=range]::-moz-range-thumb{
  width:16px;height:16px;border-radius:50%;background:#fff;
  border:3px solid var(--green);box-shadow:0 2px 6px rgba(14,159,110,.35);cursor:grab;
}
.range-val{
  font-size:12px;font-weight:700;color:var(--green-d);
  font-variant-numeric:tabular-nums;min-width:52px;text-align:right;
}

.gap-hero{
  display:flex;align-items:center;gap:18px;
  padding:4px 0 18px;border-bottom:1px solid var(--border);margin-bottom:16px;
}
.gauge-wrap{position:relative;width:132px;height:78px;flex-shrink:0}
.gauge-wrap svg{width:100%;height:100%;overflow:visible}
.gauge-center{
  position:absolute;left:0;right:0;bottom:-2px;text-align:center;
}
.gauge-center .gv{font-size:26px;font-weight:800;letter-spacing:-1px;line-height:1;font-variant-numeric:tabular-nums}
.gauge-center .gl{font-size:10px;font-weight:650;color:var(--muted-2);letter-spacing:.5px;text-transform:uppercase;margin-top:3px}
.gap-hero-text h4{font-size:13.5px;font-weight:700;letter-spacing:-.2px;margin-bottom:5px}
.gap-hero-text p{font-size:11.8px;color:var(--muted);line-height:1.55}
.pill{
  display:inline-flex;align-items:center;gap:5px;
  font-size:10.5px;font-weight:700;padding:3px 9px;border-radius:20px;
  letter-spacing:.2px;
}
.pill-amber{background:var(--amber-l);color:#B45309}
.pill-green{background:var(--green-l);color:var(--green-d)}
.pill-red{background:var(--red-l);color:#C0392B}
.pill-blue{background:var(--blue-l);color:#1D4ED8}

.gap-list{display:flex;flex-direction:column;gap:2px}
.gap-item{
  display:grid;grid-template-columns:26px 1fr 46px;
  align-items:center;gap:11px;
  padding:9px 8px;border-radius:10px;cursor:pointer;
  transition:background .18s;
}
.gap-item:hover{background:var(--surface-2)}
.gap-rank{
  font-size:11px;font-weight:750;color:var(--muted-2);
  font-variant-numeric:tabular-nums;text-align:center;
}
.gap-info{min-width:0}
.gap-name{font-size:12.6px;font-weight:600;margin-bottom:5px;display:flex;align-items:center;gap:7px}
.gap-name span{font-size:10.5px;color:var(--muted-2);font-weight:500}
.gap-track{height:5px;border-radius:20px;background:var(--surface-3);overflow:hidden}
.gap-fill{
  height:100%;border-radius:20px;width:0;
  transition:width 1.15s cubic-bezier(.22,1,.36,1);
}
.gap-score{
  font-size:14px;font-weight:750;text-align:right;
  font-variant-numeric:tabular-nums;letter-spacing:-.3px;
}

.donut-wrap{display:flex;flex-direction:column;align-items:center;gap:16px}
.donut-svg{width:190px;height:190px;position:relative}
.donut-svg svg{width:100%;height:100%;transform:rotate(-90deg);overflow:visible}
.donut-seg{
  fill:none;stroke-linecap:round;
  transition:stroke-width .25s ease, opacity .25s ease;
  cursor:pointer;
}
.donut-seg:hover{stroke-width:26}
.donut-center{
  position:absolute;inset:0;display:flex;flex-direction:column;
  align-items:center;justify-content:center;pointer-events:none;
}
.donut-center .dv{font-size:25px;font-weight:800;letter-spacing:-1.1px;line-height:1;font-variant-numeric:tabular-nums}
.donut-center .dl{font-size:10.5px;font-weight:600;color:var(--muted-2);letter-spacing:.5px;text-transform:uppercase;margin-top:5px}
.donut-legend{width:100%;display:flex;flex-direction:column;gap:2px}
.dl-item{
  display:flex;align-items:center;gap:10px;
  padding:7px 9px;border-radius:9px;transition:background .18s;cursor:pointer;
}
.dl-item:hover{background:var(--surface-2)}
.dl-swatch{width:9px;height:9px;border-radius:3px;flex-shrink:0}
.dl-name{font-size:12.2px;font-weight:550;color:var(--navy-2);flex:1}
.dl-val{font-size:12.2px;font-weight:700;font-variant-numeric:tabular-nums}
.dl-pct{font-size:11px;color:var(--muted-2);font-weight:600;min-width:34px;text-align:right;font-variant-numeric:tabular-nums}

.readiness{display:flex;flex-direction:column;gap:14px}
.rr-row{display:flex;flex-direction:column;gap:7px}
.rr-top{display:flex;align-items:center;justify-content:space-between}
.rr-name{font-size:12.3px;font-weight:600;display:flex;align-items:center;gap:7px}
.rr-name em{font-style:normal;font-size:10.5px;color:var(--muted-2);font-weight:550}
.rr-val{font-size:12.3px;font-weight:750;font-variant-numeric:tabular-nums;letter-spacing:-.2px}
.rr-track{
  height:7px;border-radius:20px;background:var(--surface-3);
  position:relative;overflow:visible;
}
.rr-fill{
  height:100%;border-radius:20px;width:0;
  transition:width 1.2s cubic-bezier(.22,1,.36,1);
}
.rr-target{
  position:absolute;top:-3px;width:2px;height:13px;
  background:var(--navy);border-radius:2px;opacity:.28;
}
.rr-target::after{
  content:'target';position:absolute;top:-14px;left:50%;transform:translateX(-50%);
  font-size:8.5px;font-weight:700;color:var(--muted-2);
  letter-spacing:.4px;text-transform:uppercase;white-space:nowrap;
}

.chart-legend{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.cl-item{display:flex;align-items:center;gap:7px;font-size:11.8px;font-weight:550;color:var(--muted)}
.cl-line{width:14px;height:3px;border-radius:3px}
.cl-dash{width:14px;height:0;border-top:2px dashed var(--navy-2);opacity:.55}
.area-svg{display:block;width:100%;height:auto;overflow:visible}
.grid-line{stroke:#EDF1F6;stroke-width:1}
.axis-label{font-size:10.5px;fill:#94A3B8;font-weight:550;font-family:'Inter',sans-serif}
.hit{fill:transparent;cursor:crosshair}
.crosshair{stroke:#CBD5E1;stroke-width:1;stroke-dasharray:3 3;opacity:0;transition:opacity .15s}
.hover-dot{opacity:0;transition:opacity .15s}

.table-wrap{overflow-x:auto;margin:0 -20px -20px;padding:0 20px 8px}
table{width:100%;border-collapse:separate;border-spacing:0;font-size:12.8px}
thead th{
  text-align:left;font-size:10.5px;font-weight:700;
  letter-spacing:.65px;text-transform:uppercase;color:var(--muted-2);
  padding:0 14px 11px;border-bottom:1px solid var(--border);
  white-space:nowrap;
}
thead th.sortable{cursor:pointer;user-select:none;transition:color .18s}
thead th.sortable:hover{color:var(--navy)}
thead th .sort-ico{
  display:inline-block;margin-left:5px;opacity:.35;
  font-size:9px;transition:.18s;
}
thead th.sorted .sort-ico{opacity:1;color:var(--green)}
tbody td{padding:13px 14px;border-bottom:1px solid #F1F5F9;vertical-align:middle}
tbody tr{transition:background .16s}
tbody tr:hover{background:var(--surface-2)}
tbody tr:last-child td{border-bottom:none}

.cell-corridor{display:flex;align-items:center;gap:11px}
.corridor-icon{
  width:32px;height:32px;border-radius:10px;flex-shrink:0;
  display:grid;place-items:center;background:var(--green-l);color:var(--green-d);
}
.corridor-icon svg{width:15px;height:15px;stroke-width:2}
.corridor-name{font-weight:650;font-size:12.8px;letter-spacing:-.1px}
.corridor-sub{font-size:11px;color:var(--muted-2);font-weight:500;margin-top:1px}

.cell-num{font-variant-numeric:tabular-nums;font-weight:650;letter-spacing:-.2px}
.mini-bar{
  width:64px;height:5px;border-radius:20px;background:var(--surface-3);
  overflow:hidden;display:inline-block;vertical-align:middle;margin-right:9px;
}
.mini-bar i{display:block;height:100%;border-radius:20px}

.status-pill{
  display:inline-flex;align-items:center;gap:6px;
  font-size:11px;font-weight:650;padding:4px 10px;border-radius:20px;
  white-space:nowrap;
}
.status-pill .sdot{width:6px;height:6px;border-radius:50%}

.row-action{
  width:30px;height:30px;border-radius:9px;border:1px solid var(--border);
  background:var(--surface);display:grid;place-items:center;
  color:var(--muted-2);cursor:pointer;transition:.18s;
}
.row-action:hover{color:var(--green-d);border-color:var(--green-l2);background:var(--green-l)}
.row-action svg{width:14px;height:14px;stroke-width:2}

#tip{
  position:fixed;z-index:999;pointer-events:none;
  background:rgba(11,27,51,.96);
  color:#fff;border-radius:11px;padding:11px 13px;
  font-size:12px;line-height:1.5;
  box-shadow:0 16px 36px -10px rgba(11,27,51,.5);
  opacity:0;transform:translateY(4px) scale(.97);
  transition:opacity .16s ease, transform .16s cubic-bezier(.22,1,.36,1);
  backdrop-filter:blur(8px);min-width:150px;
}
#tip.show{opacity:1;transform:translateY(0) scale(1)}
#tip .tt-name{font-weight:700;font-size:12.8px;letter-spacing:-.2px;margin-bottom:2px}
#tip .tt-sub{font-size:10.8px;color:#94A3B8;font-weight:500;margin-bottom:8px}
#tip .tt-row{
  display:flex;align-items:center;justify-content:space-between;
  gap:18px;font-size:11.4px;color:#CBD5E1;padding:2.5px 0;
}
#tip .tt-row b{color:#fff;font-weight:700;font-variant-numeric:tabular-nums}
#tip .tt-div{height:1px;background:rgba(255,255,255,.12);margin:7px 0}

#toast{
  position:fixed;bottom:26px;left:50%;transform:translate(-50%,18px);
  background:var(--navy);color:#fff;padding:12px 20px;border-radius:12px;
  font-size:12.8px;font-weight:600;box-shadow:var(--sh-lg);
  opacity:0;pointer-events:none;transition:.3s cubic-bezier(.22,1,.36,1);
  z-index:1000;display:flex;align-items:center;gap:9px;
}
#toast.show{opacity:1;transform:translate(-50%,0)}
#toast svg{width:15px;height:15px;color:#34D399}

@media (max-width:1360px){
  .kpis{grid-template-columns:repeat(2,minmax(0,1fr))}
  .grid-main,.grid-split{grid-template-columns:minmax(0,1fr)}
}
@media (max-width:1080px){
  body{grid-template-columns:72px minmax(0,1fr)}
  .brand-text,.nav-label,.nav-item span,.sidebar-foot .health-card,.user-card div{display:none}
  .nav-item{justify-content:center;padding:11px}
  .sidebar{padding:18px 10px}
  .brand{justify-content:center;padding:0}
  .search{width:170px}
}
@media (max-width:820px){
  .main{padding:0 16px 32px}
  .kpis{grid-template-columns:1fr}
  .topbar{flex-direction:column;align-items:flex-start;gap:14px}
  .topbar-actions{width:100%}
  .search{flex:1;width:auto}
}
</style>
</head>
<body>

<aside class="sidebar">
  <div class="brand">
    <div class="brand-mark">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M13 2 4.09 12.69a1 1 0 0 0 .77 1.64H11l-1 7.67 8.91-10.69a1 1 0 0 0-.77-1.64H12l1-7.67Z"/>
      </svg>
    </div>
    <div class="brand-text">
      <div class="brand-name">ChargeWise</div>
      <div class="brand-sub">India · EV Intel</div>
    </div>
  </div>

  <div class="nav-label">Analytics</div>
  <nav class="nav" id="mainNav">
    <button class="nav-item active" data-target="top" data-title="National Overview" data-sub="Real-time EV infrastructure coverage & charging gap analysis across India">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/></svg>
      <span>Overview</span>
    </button>
    <button class="nav-item" data-target="mapSection" data-title="Infrastructure Map" data-sub="Geospatial station density, coverage radius & live network topology">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/></svg>
      <span>Coverage Map</span>
    </button>
    <button class="nav-item" data-target="gapSection" data-title="Charging Gap Analysis" data-sub="Identifying underserved regions and infrastructure deficit hotspots">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l5-6 4 4 5-8 4 5"/><path d="M3 21h18"/></svg>
      <span>Gap Analysis</span>
      <span class="nav-badge">7</span>
    </button>
    <button class="nav-item" data-target="corridorSection" data-title="Priority Corridors" data-sub="Highway charging corridors ranked by infrastructure readiness">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="19" r="2.5"/><circle cx="18" cy="5" r="2.5"/><path d="M8.5 19H14a3.5 3.5 0 0 0 0-7h-4a3.5 3.5 0 0 1 0-7h5.5"/></svg>
      <span>Corridors</span>
    </button>
    <button class="nav-item" data-target="mixSection" data-title="Charger Mix" data-sub="Distribution of charger technologies and power classes nationwide">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M9 2v8"/><path d="M15 2v8"/><path d="M6 2h12v6a6 6 0 0 1-12 0V2Z"/><path d="M12 14v8"/></svg>
      <span>Charger Mix</span>
    </button>
  </nav>

  <div class="nav-label">Operations</div>
  <nav class="nav">
    <button class="nav-item" data-toast="Report builder is generating your PDF export…">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6.5A2.5 2.5 0 0 0 4 4.5v15A2.5 2.5 0 0 0 6.5 22h11a2.5 2.5 0 0 0 2.5-2.5V8Z"/><path d="M14 2v6h6"/><path d="M9 15h6"/><path d="M9 11h3"/></svg>
      <span>Reports</span>
    </button>
    <button class="nav-item" data-toast="Settings panel synced with your workspace.">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .34 1.87l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.7 1.7 0 0 0-1.87-.34 1.7 1.7 0 0 0-1 1.55V21a2 2 0 1 1-4 0v-.09A1.7 1.7 0 0 0 9 19.4a1.7 1.7 0 0 0-1.87.34l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-1.55-1H3a2 2 0 1 1 0-4h.09A1.7 1.7 0 0 0 4.6 9a1.7 1.7 0 0 0-.34-1.87l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-1.55V3a2 2 0 1 1 4 0v.09a1.7 1.7 0 0 0 1 1.55 1.7 1.7 0 0 0 1.87-.34l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.7 1.7 0 0 0 19.4 9v.09a1.7 1.7 0 0 0 1.55 1H21a2 2 0 1 1 0 4h-.09a1.7 1.7 0 0 0-1.51 1Z"/></svg>
      <span>Settings</span>
    </button>
  </nav>

  <div class="sidebar-foot">
    <div class="health-card">
      <div class="health-top">
        <div class="health-title">Network Health</div>
        <div class="live-dot"></div>
      </div>
      <div class="health-val">98.2<span>%</span></div>
      <div class="health-bar"><i data-w="98.2"></i></div>
      <div class="health-meta">21,486 of 21,880 points online</div>
    </div>
    <div class="user-card">
      <div class="avatar">AR</div>
      <div>
        <div class="user-name">Arjun Rao</div>
        <div class="user-role">Policy Analyst</div>
      </div>
    </div>
  </div>
</aside>

<main class="main" id="top">

  <header class="topbar">
    <div class="page-title">
      <h1 id="pageTitle">National Overview</h1>
      <p id="pageSub">Real-time EV infrastructure coverage &amp; charging gap analysis across India</p>
    </div>
    <div class="topbar-actions">
      <div class="search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.2-3.2"/></svg>
        <input type="text" placeholder="Search stations, states, corridors…" id="globalSearch" />
        <span class="kbd">⌘K</span>
      </div>
      <button class="icon-btn" title="Notifications">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/></svg>
        <span class="dot"></span>
      </button>
      <div class="live-chip"><span class="live-dot"></span> Live</div>
    </div>
  </header>

  <div class="filterbar">
    <button class="filter">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/></svg>
      <span class="filter-label">Region</span>
      <strong>All India</strong>
      <svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
    </button>
    <button class="filter">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4.09 12.69a1 1 0 0 0 .77 1.64H11l-1 7.67 8.91-10.69a1 1 0 0 0-.77-1.64H12l1-7.67Z"/></svg>
      <span class="filter-label">Charger</span>
      <strong>All Types</strong>
      <svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
    </button>
    <button class="filter">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4.5" width="18" height="16" rx="2.5"/><path d="M8 3v3M16 3v3M3 10h18"/></svg>
      <span class="filter-label">Period</span>
      <strong>Last 14 days</strong>
      <svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
    </button>
    <button class="filter">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M4 6h16M7 12h10M10 18h4"/></svg>
      <span class="filter-label">Status</span>
      <strong>Operational</strong>
      <svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
    </button>
    <button class="btn-primary" id="analyzeBtn">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17l5-6 4 4 5-8 4 5"/><path d="M3 21h18"/></svg>
      Run Analysis
    </button>
  </div>

  <section class="kpis">
    <article class="kpi">
      <div class="kpi-top">
        <div class="kpi-icon" style="background:var(--green-l);color:var(--green-d)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4.09 12.69a1 1 0 0 0 .77 1.64H11l-1 7.67 8.91-10.69a1 1 0 0 0-.77-1.64H12l1-7.67Z"/></svg>
        </div>
        <div class="kpi-delta delta-up">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5"/><path d="m5 12 7-7 7 7"/></svg>
          12.4%
        </div>
      </div>
      <div class="kpi-label">Total Charging Points</div>
      <div class="kpi-value" data-count="21486">0</div>
      <div class="kpi-foot">
        <div class="kpi-note"><b>+2,371</b> added this quarter</div>
        <div class="spark" data-spark="12,14,13,16,18,17,21,20,24,23,27,29" data-color="#0E9F6E"></div>
      </div>
    </article>

    <article class="kpi">
      <div class="kpi-top">
        <div class="kpi-icon" style="background:var(--blue-l);color:#1D4ED8">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s7-5.6 7-11a7 7 0 1 0-14 0c0 5.4 7 11 7 11Z"/><circle cx="12" cy="10" r="2.6"/></svg>
        </div>
        <div class="kpi-delta delta-up">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5"/><path d="m5 12 7-7 7 7"/></svg>
          +2
        </div>
      </div>
      <div class="kpi-label">States &amp; UTs Covered</div>
      <div class="kpi-value"><span data-count="28">0</span><span class="unit">/ 36</span></div>
      <div class="kpi-foot">
        <div class="kpi-note"><b>77.8%</b> national coverage</div>
        <div class="spark" data-spark="14,15,16,17,18,19,20,22,23,25,26,28" data-color="#3B82F6"></div>
      </div>
    </article>

    <article class="kpi">
      <div class="kpi-top">
        <div class="kpi-icon" style="background:var(--amber-l);color:#B45309">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M10.3 3.9 2.5 17.4A2 2 0 0 0 4.2 20.4h15.6a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
        </div>
        <div class="kpi-delta delta-down">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5v14"/><path d="m19 12-7 7-7-7"/></svg>
          3.2 pts
        </div>
      </div>
      <div class="kpi-label">Avg. Charging Gap Index</div>
      <div class="kpi-value" data-count="42.8" data-decimals="1">0</div>
      <div class="kpi-foot">
        <div class="kpi-note">Moderate deficit · <b>improving</b></div>
        <div class="spark" data-spark="58,56,55,53,52,50,49,48,47,45,44,42.8" data-color="#F59E0B"></div>
      </div>
    </article>

    <article class="kpi">
      <div class="kpi-top">
        <div class="kpi-icon" style="background:#F3EEFE;color:#6D28D9">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v16.5A2.5 2.5 0 0 0 5.5 22H21"/><path d="m7 14 4-5 3.5 3.5L21 6"/></svg>
        </div>
        <div class="kpi-delta delta-up">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5"/><path d="m5 12 7-7 7 7"/></svg>
          8.1%
        </div>
      </div>
      <div class="kpi-label">Daily Charging Sessions</div>
      <div class="kpi-value"><span data-count="128.4" data-decimals="1">0</span><span class="unit">K</span></div>
      <div class="kpi-foot">
        <div class="kpi-note"><b>9.6K</b> avg. per hour peak</div>
        <div class="spark" data-spark="88,92,86,98,105,101,112,108,119,124,121,128" data-color="#8B5CF6"></div>
      </div>
    </article>
  </section>

  <section class="grid-main" id="mapSection">
    <article class="card">
      <div class="card-head">
        <div>
          <h3>Infrastructure Coverage Map</h3>
          <p>Live station density, gap hotspots &amp; priority corridors · updated 2 min ago</p>
        </div>
        <div class="seg" id="layerSeg">
          <button class="seg-btn active" data-layer="stations">Stations</button>
          <button class="seg-btn active" data-layer="gaps">Gap Zones</button>
          <button class="seg-btn active" data-layer="corridors">Corridors</button>
        </div>
      </div>

      <div class="map-wrap">
        <svg id="indiaMap" viewBox="0 0 500 560" role="img" aria-label="India EV charging infrastructure map"></svg>

        <div class="map-stat">
          <div class="ms-row"><span class="ms-label">Hotspots</span><span class="ms-val" style="color:#C0392B">7</span></div>
          <div class="ms-row"><span class="ms-label">Stations plotted</span><span class="ms-val" id="plottedCount">0</span></div>
          <div class="ms-row"><span class="ms-label">Corridors</span><span class="ms-val">5</span></div>
        </div>

        <div class="legend">
          <div class="legend-title">Legend</div>
          <div class="legend-item"><span class="legend-swatch" style="background:#10B981"></span> Adequate coverage</div>
          <div class="legend-item"><span class="legend-swatch" style="background:#F59E0B"></span> Moderate deficit</div>
          <div class="legend-item"><span class="legend-swatch" style="background:#EF4444"></span> Critical gap</div>
          <div class="legend-item"><span class="legend-swatch" style="background:#0E9F6E;border-radius:2px;height:2px;width:14px"></span> Priority corridor</div>
        </div>
      </div>

      <div class="map-foot">
        <label for="radius">Coverage radius</label>
        <div class="range-wrap">
          <input type="range" id="radius" min="4" max="30" value="12" step="1" style="--fill:31%" />
          <span class="range-val" id="radiusVal">12 km</span>
        </div>
      </div>
    </article>

    <article class="card" id="gapSection">
      <div class="card-head">
        <div>
          <h3>Charging Gap Index</h3>
          <p>Composite deficit score by state (higher = worse)</p>
        </div>
        <span class="pill pill-amber">Action needed</span>
      </div>

      <div class="gap-hero">
        <div class="gauge-wrap">
          <svg viewBox="0 0 132 78">
            <defs>
              <linearGradient id="gaugeGrad" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stop-color="#10B981"/>
                <stop offset="55%" stop-color="#F59E0B"/>
                <stop offset="100%" stop-color="#EF4444"/>
              </linearGradient>
            </defs>
            <path d="M 14 70 A 52 52 0 0 1 118 70" fill="none" stroke="#EDF1F6" stroke-width="11" stroke-linecap="round"/>
            <path id="gaugeArc" d="M 14 70 A 52 52 0 0 1 118 70" fill="none" stroke="url(#gaugeGrad)"
                  stroke-width="11" stroke-linecap="round"
                  stroke-dasharray="163.4" stroke-dashoffset="163.4"
                  style="transition:stroke-dashoffset 1.6s cubic-bezier(.22,1,.36,1)"/>
          </svg>
          <div class="gauge-center">
            <div class="gv">42.8</div>
            <div class="gl">Moderate</div>
          </div>
        </div>
        <div class="gap-hero-text">
          <h4>National deficit down 3.2 pts</h4>
          <p>7 states remain below the 60% infrastructure adequacy threshold. Bihar &amp; Jharkhand show the steepest shortfall.</p>
        </div>
      </div>

      <div class="gap-list" id="gapList"></div>
    </article>
  </section>

  <section class="grid-split">
    <article class="card">
      <div class="card-head">
        <div>
          <h3>Charging Sessions &amp; Grid Utilisation</h3>
          <p>Daily session volume against average charger utilisation</p>
        </div>
        <div class="chart-legend">
          <div class="cl-item"><span class="cl-line" style="background:#0E9F6E"></span> Sessions (K)</div>
          <div class="cl-item"><span class="cl-dash"></span> Utilisation (%)</div>
        </div>
      </div>
      <svg class="area-svg" id="areaChart" viewBox="0 0 660 268" preserveAspectRatio="xMidYMid meet"></svg>
    </article>

    <div class="col-stack">
      <article class="card" id="mixSection">
        <div class="card-head">
          <div>
            <h3>Charger Type Mix</h3>
            <p>Nationwide distribution</p>
          </div>
        </div>
        <div class="donut-wrap">
          <div class="donut-svg" id="donutWrap">
            <svg viewBox="0 0 200 200" id="donutSvg"></svg>
            <div class="donut-center">
              <div class="dv">21,486</div>
              <div class="dl">Total points</div>
            </div>
          </div>
          <div class="donut-legend" id="donutLegend"></div>
        </div>
      </article>

      <article class="card">
        <div class="card-head">
          <div>
            <h3>Regional Readiness</h3>
            <p>Coverage vs. 2027 target</p>
          </div>
        </div>
        <div class="readiness" id="readiness"></div>
      </article>
    </div>
  </section>

  <section class="card" id="corridorSection">
    <div class="card-head">
      <div>
        <h3>Priority Charging Corridors</h3>
        <p>Highway corridors ranked by infrastructure gap severity &amp; traffic potential</p>
      </div>
      <button class="filter" style="margin:0">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12"/><path d="m7 10 5 5 5-5"/><path d="M5 21h14"/></svg>
        Export CSV
      </button>
    </div>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Corridor</th>
            <th class="sortable" data-sort="stations">Stations <span class="sort-ico">▼</span></th>
            <th class="sortable" data-sort="gap">Gap Index <span class="sort-ico">▼</span></th>
            <th class="sortable" data-sort="util">Utilisation <span class="sort-ico">▼</span></th>
            <th>Status</th>
            <th style="text-align:right">Action</th>
          </tr>
        </thead>
        <tbody id="corridorBody"></tbody>
      </table>
    </div>
  </section>

</main>

<div id="tip"></div>
<div id="toast">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
  <span id="toastMsg">Done</span>
</div>

<script>
const $  = (s, el = document) => el.querySelector(s);
const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));

const tooltip = $('#tip');
function showTip(html, x, y){
  tooltip.innerHTML = html;
  tooltip.classList.add('show');
  const r = tooltip.getBoundingClientRect();
  let left = x + 16, top = y - r.height / 2;
  if (left + r.width > window.innerWidth - 12) left = x - r.width - 16;
  top = Math.max(10, Math.min(top, window.innerHeight - r.height - 10));
  tooltip.style.left = left + 'px';
  tooltip.style.top  = top + 'px';
}
function hideTip(){ tooltip.classList.remove('show'); }

let toastTimer;
function toast(msg){
  $('#toastMsg').textContent = msg;
  const t = $('#toast');
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 2600);
}

const stations = [
  { n:'New Delhi',        s:'Delhi NCR',      x:200, y:145, c:1842, g:22, k:'good' },
  { n:'Chandigarh',       s:'Punjab',         x:205, y:118, c:412,  g:31, k:'good' },
  { n:'Jaipur',           s:'Rajasthan',      x:180, y:165, c:386,  g:58, k:'warn' },
  { n:'Lucknow',          s:'Uttar Pradesh',  x:255, y:165, c:298,  g:71, k:'bad'  },
  { n:'Kanpur',           s:'Uttar Pradesh',  x:250, y:178, c:164,  g:76, k:'bad'  },
  { n:'Varanasi',         s:'Uttar Pradesh',  x:285, y:185, c:142,  g:68, k:'warn' },
  { n:'Patna',            s:'Bihar',          x:315, y:180, c:118,  g:82, k:'bad'  },
  { n:'Kolkata',          s:'West Bengal',    x:370, y:215, c:874,  g:38, k:'good' },
  { n:'Bhubaneswar',      s:'Odisha',         x:350, y:255, c:226,  g:64, k:'warn' },
  { n:'Guwahati',         s:'Assam',          x:420, y:155, c:132,  g:73, k:'bad'  },
  { n:'Ahmedabad',        s:'Gujarat',        x:145, y:235, c:692,  g:29, k:'good' },
  { n:'Surat',            s:'Gujarat',        x:170, y:255, c:448,  g:34, k:'good' },
  { n:'Mumbai',           s:'Maharashtra',    x:185, y:295, c:2140, g:16, k:'good' },
  { n:'Pune',             s:'Maharashtra',    x:200, y:305, c:786,  g:24, k:'good' },
  { n:'Nagpur',           s:'Maharashtra',    x:245, y:260, c:312,  g:52, k:'warn' },
  { n:'Bhopal',           s:'Madhya Pradesh', x:215, y:225, c:224,  g:61, k:'warn' },
  { n:'Indore',           s:'Madhya Pradesh', x:190, y:240, c:268,  g:57, k:'warn' },
  { n:'Raipur',           s:'Chhattisgarh',   x:280, y:265, c:176,  g:66, k:'warn' },
  { n:'Hyderabad',        s:'Telangana',      x:245, y:330, c:948,  g:27, k:'good' },
  { n:'Visakhapatnam',    s:'Andhra Pradesh', x:315, y:310, c:284,  g:49, k:'warn' },
  { n:'Vijayawada',       s:'Andhra Pradesh', x:275, y:345, c:196,  g:54, k:'warn' },
  { n:'Bengaluru',        s:'Karnataka',      x:255, y:415, c:2260, g:14, k:'good' },
  { n:'Chennai',          s:'Tamil Nadu',     x:305, y:400, c:1180, g:21, k:'good' },
  { n:'Coimbatore',       s:'Tamil Nadu',     x:250, y:440, c:342,  g:44, k:'good' },
  { n:'Kochi',            s:'Kerala',         x:243, y:470, c:398,  g:36, k:'good' },
  { n:'Thiruvananthapuram',s:'Kerala',        x:252, y:505, c:286,  g:33, k:'good' },
  { n:'Panaji',           s:'Goa',            x:188, y:350, c:174,  g:41, k:'good' }
];

const gapZones = [
  { x:315, y:180, r:62, c:'#EF4444' },
  { x:253, y:168, r:74, c:'#EF4444' },
  { x:340, y:216, r:46, c:'#F59E0B' },
  { x:344, y:256, r:44, c:'#F59E0B' },
  { x:214, y:228, r:56, c:'#F59E0B' },
  { x:172, y:162, r:58, c:'#F59E0B' },
  { x:420, y:152, r:42, c:'#EF4444' }
];

const corridors = [
  { pts:[[200,145],[180,165],[145,235],[185,295]] },
  { pts:[[200,145],[255,165],[315,180],[370,215]] },
  { pts:[[255,415],[305,400]] },
  { pts:[[245,330],[255,415]] },
  { pts:[[185,295],[245,260],[280,265],[370,215]] }
];

const gapStates = [
  { name:'Bihar',           note:'118 stations', score:82, color:'#EF4444' },
  { name:'Uttar Pradesh',   note:'604 stations', score:73, color:'#EF4444' },
  { name:'Jharkhand',       note:'96 stations',  score:69, color:'#F59E0B' },
  { name:'Assam',           note:'132 stations', score:66, color:'#F59E0B' },
  { name:'Odisha',          note:'226 stations', score:64, color:'#F59E0B' },
  { name:'Madhya Pradesh',  note:'492 stations', score:59, color:'#F59E0B' },
  { name:'Rajasthan',       note:'386 stations', score:58, color:'#F59E0B' }
];

const chargerMix = [
  { name:'DC Fast (≥60 kW)',     value:7305, pct:34, color:'#0E9F6E' },
  { name:'AC Type-2 (7–22 kW)',  value:8809, pct:41, color:'#3B82F6' },
  { name:'AC Slow (3.3 kW)',     value:3223, pct:15, color:'#94A3B8' },
  { name:'Bharat DC-001',        value:2149, pct:10, color:'#F59E0B' }
];

const readiness = [
  { name:'South',     note:'5 states',  value:88, target:92, color:'#0E9F6E' },
  { name:'West',      note:'4 states',  value:79, target:90, color:'#0E9F6E' },
  { name:'North',     note:'7 states',  value:71, target:88, color:'#3B82F6' },
  { name:'Central',   note:'4 states',  value:52, target:85, color:'#F59E0B' },
  { name:'East',      note:'5 states',  value:44, target:80, color:'#F59E0B' },
  { name:'Northeast', note:'8 states',  value:31, target:75, color:'#EF4444' }
];

const corridorRows = [
  { name:'Delhi – Jaipur (NH-48)',      sub:'Delhi · Haryana · Rajasthan',  stations:84,  gap:34, util:78, status:'Operational', sc:'green' },
  { name:'Mumbai – Pune Expressway',    sub:'Maharashtra',                   stations:126, gap:18, util:86, status:'Operational', sc:'green' },
  { name:'Bengaluru – Mysuru (NH-275)', sub:'Karnataka',                     stations:62,  gap:26, util:71, status:'Operational', sc:'green' },
  { name:'Delhi – Lucknow (NH-27)',     sub:'Delhi · UP',                    stations:41,  gap:68, util:52, status:'Under Expansion', sc:'amber' },
  { name:'Chennai – Coimbatore (NH-544)',sub:'Tamil Nadu',                   stations:38,  gap:47, util:64, status:'Under Expansion', sc:'amber' },
  { name:'Kolkata – Durgapur (NH-19)',  sub:'West Bengal',                   stations:22,  gap:74, util:41, status:'Critical Gap', sc:'red' },
  { name:'Hyderabad – Vijayawada (NH-65)',sub:'Telangana · Andhra Pradesh',  stations:29,  gap:61, util:57, status:'Under Expansion', sc:'amber' }
];

function animateCounters(){
  $$('[data-count]').forEach(el => {
    const target = parseFloat(el.dataset.count);
    const dec = parseInt(el.dataset.decimals || '0', 10);
    const dur = 1500;
    const start = performance.now();
    function tick(now){
      const p = Math.min((now - start) / dur, 1);
      const eased = 1 - Math.pow(1 - p, 3);
      const v = target * eased;
      el.textContent = dec
        ? v.toFixed(dec)
        : Math.round(v).toLocaleString('en-IN');
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
}

function renderSparklines(){
  $$('.spark').forEach(el => {
    const data = el.dataset.spark.split(',').map(Number);
    const color = el.dataset.color || '#0E9F6E';
    const w = 88, h = 34, pad = 4;
    const min = Math.min(...data), max = Math.max(...data);
    const range = (max - min) || 1;
    const step = (w - pad * 2) / (data.length - 1);

    const pts = data.map((v, i) => {
      const x = pad + i * step;
      const y = h - pad - ((v - min) / range) * (h - pad * 2);
      return [x, y];
    });

    const line = pts.map((p, i) => (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1)).join(' ');
    const area = line + ' L ' + pts[pts.length-1][0].toFixed(1) + ' ' + h + ' L ' + pts[0][0].toFixed(1) + ' ' + h + ' Z';
    const gid = 'sg' + Math.random().toString(36).slice(2, 9);

    el.innerHTML = '<svg viewBox="0 0 ' + w + ' ' + h + '" preserveAspectRatio="none">' +
      '<defs><linearGradient id="' + gid + '" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0%" stop-color="' + color + '" stop-opacity="0.24"/>' +
        '<stop offset="100%" stop-color="' + color + '" stop-opacity="0"/>' +
      '</linearGradient></defs>' +
      '<path d="' + area + '" fill="url(#' + gid + ')"/>' +
      '<path d="' + line + '" fill="none" stroke="' + color + '" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="stroke-dasharray:400;stroke-dashoffset:400;animation:drawLine 1.5s cubic-bezier(.22,1,.36,1) forwards"/>' +
      '<circle cx="' + pts[pts.length-1][0].toFixed(1) + '" cy="' + pts[pts.length-1][1].toFixed(1) + '" r="2.6" fill="' + color + '" stroke="#fff" stroke-width="1.6"/>' +
      '</svg>';
  });
}

const styleTag = document.createElement('style');
styleTag.textContent = '@keyframes drawLine{to{stroke-dashoffset:0}}';
document.head.appendChild(styleTag);

const INDIA_PATH = 'M 175 30 C 190 42, 205 48, 222 52 L 250 68 L 285 78 L 315 88 L 345 100 L 375 108 L 400 122 L 428 118 L 452 132 L 440 158 L 418 168 L 412 192 L 396 214 L 388 248 L 368 286 L 348 326 L 330 364 L 312 404 L 296 448 L 280 488 L 266 520 L 250 500 L 240 460 L 228 420 L 214 380 L 198 340 L 184 300 L 168 264 L 142 250 L 108 236 L 86 216 L 112 200 L 140 194 L 150 176 L 122 160 L 136 130 L 154 110 L 160 80 Z';

const STATUS_COLOR = { good:'#10B981', warn:'#F59E0B', bad:'#EF4444' };

function renderMap(){
  const svg = $('#indiaMap');
  let html = '<defs>' +
      '<linearGradient id="landGrad" x1="0" y1="0" x2="0.4" y2="1">' +
        '<stop offset="0%" stop-color="#F6FBF9"/>' +
        '<stop offset="55%" stop-color="#EFF8F4"/>' +
        '<stop offset="100%" stop-color="#E9F4EF"/>' +
      '</linearGradient>' +
      '<radialGradient id="gapRed">' +
        '<stop offset="0%" stop-color="#EF4444" stop-opacity="0.42"/>' +
        '<stop offset="70%" stop-color="#EF4444" stop-opacity="0.10"/>' +
        '<stop offset="100%" stop-color="#EF4444" stop-opacity="0"/>' +
      '</radialGradient>' +
      '<radialGradient id="gapAmber">' +
        '<stop offset="0%" stop-color="#F59E0B" stop-opacity="0.38"/>' +
        '<stop offset="70%" stop-color="#F59E0B" stop-opacity="0.09"/>' +
        '<stop offset="100%" stop-color="#F59E0B" stop-opacity="0"/>' +
      '</radialGradient>' +
      '<filter id="stationGlow" x="-120%" y="-120%" width="340%" height="340%">' +
        '<feGaussianBlur stdDeviation="3" result="b"/>' +
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>' +
      '</filter>' +
    '</defs>' +
    '<path class="india-land" d="' + INDIA_PATH + '"/>' +
    '<g id="layer-gaps">';

  gapZones.forEach(z => {
    const grad = z.c === '#EF4444' ? 'url(#gapRed)' : 'url(#gapAmber)';
    html += '<circle class="gap-zone" cx="' + z.x + '" cy="' + z.y + '" r="' + z.r + '" fill="' + grad + '"/>';
  });

  html += '</g><g id="layer-corridors">';

  corridors.forEach(c => {
    const d = c.pts.map((p, i) => (i ? 'L' : 'M') + p[0] + ' ' + p[1]).join(' ');
    html += '<path class="corridor" d="' + d + '"/>';
  });

  html += '</g><g id="layer-stations">';

  stations.forEach((st, i) => {
    const col = STATUS_COLOR[st.k];
    html += '<g class="station" data-i="' + i + '">' +
        '<circle class="pulse" cx="' + st.x + '" cy="' + st.y + '" r="5" fill="' + col + '" opacity="0.5"/>' +
        '<circle class="halo coverage-ring" cx="' + st.x + '" cy="' + st.y + '" r="12" fill="' + col + '" fill-opacity="0.07" stroke="' + col + '" stroke-opacity="0.18" stroke-width="1"/>' +
        '<circle class="core" cx="' + st.x + '" cy="' + st.y + '" r="4.2" fill="' + col + '" stroke="#fff" stroke-width="1.8" filter="url(#stationGlow)"/>' +
      '</g>';
  });

  html += '</g>';
  svg.innerHTML = html;

  const pc = $('#plottedCount');
  let n = 0;
  const step = Math.max(1, Math.round(stations.length / 22));
  const iv = setInterval(() => {
    n = Math.min(n + step, stations.length);
    pc.textContent = n;
    if (n >= stations.length) clearInterval(iv);
  }, 45);

  $$('.station', svg).forEach(g => {
    const st = stations[+g.dataset.i];
    g.addEventListener('mouseenter', e => {
      const sev = st.g >= 65 ? ['Critical', '#EF4444'] : st.g >= 45 ? ['Moderate', '#F59E0B'] : ['Adequate', '#10B981'];
      showTip(
        '<div class="tt-name">' + st.n + '</div>' +
        '<div class="tt-sub">' + st.s + '</div>' +
        '<div class="tt-row"><span>Charging points</span><b>' + st.c.toLocaleString('en-IN') + '</b></div>' +
        '<div class="tt-row"><span>Gap index</span><b style="color:' + sev[1] + '">' + st.g + ' · ' + sev[0] + '</b></div>' +
        '<div class="tt-div"></div>' +
        '<div class="tt-row"><span>Status</span><b>' + (st.k === 'good' ? 'Online' : st.k === 'warn' ? 'Strained' : 'Deficit') + '</b></div>',
        e.clientX, e.clientY
      );
    });
    g.addEventListener('mousemove', e => showTip(tooltip.innerHTML, e.clientX, e.clientY));
    g.addEventListener('mouseleave', hideTip);
  });
}

function initLayerToggles(){
  $$('#layerSeg .seg-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      btn.classList.toggle('active');
      const layer = btn.dataset.layer;
      const on = btn.classList.contains('active');
      const targets = {
        stations:  $$('#indiaMap .station'),
        gaps:      $$('#indiaMap .gap-zone'),
        corridors: $$('#indiaMap .corridor')
      }[layer];
      targets.forEach(t => t.classList.toggle('hidden', !on));
    });
  });
}

function initRadiusSlider(){
  const input = $('#radius');
  const label = $('#radiusVal');
  function update(){
    const v = +input.value;
    const pct = ((v - input.min) / (input.max - input.min)) * 100;
    input.style.setProperty('--fill', pct + '%');
    label.textContent = v + ' km';
    $$('#indiaMap .coverage-ring').forEach(c => {
      c.setAttribute('r', v);
      c.setAttribute('fill-opacity', Math.max(0.03, 0.12 - v / 400));
    });
  }
  input.addEventListener('input', update);
  update();
}

function animateGauge(){
  const arc = $('#gaugeArc');
  if (!arc) return;
  const L = 163.4;
  const pct = 0.428;
  setTimeout(() => { arc.style.strokeDashoffset = L - L * pct; }, 220);
}

function renderGapList(){
  const wrap = $('#gapList');
  wrap.innerHTML = gapStates.map((g, i) => (
    '<div class="gap-item">' +
      '<div class="gap-rank">' + String(i + 1).padStart(2, '0') + '</div>' +
      '<div class="gap-info">' +
        '<div class="gap-name">' + g.name + ' <span>' + g.note + '</span></div>' +
        '<div class="gap-track"><div class="gap-fill" data-w="' + g.score + '" style="background:linear-gradient(90deg,' + g.color + '99,' + g.color + ')"></div></div>' +
      '</div>' +
      '<div class="gap-score" style="color:' + g.color + '">' + g.score + '</div>' +
    '</div>'
  )).join('');

  setTimeout(() => {
    $$('.gap-fill', wrap).forEach(el => { el.style.width = el.dataset.w + '%'; });
  }, 320);
}

function renderDonut(){
  const svg = $('#donutSvg');
  const legend = $('#donutLegend');
  const R = 68;
  const C = 2 * Math.PI * R;
  const gap = 3.2;

  let offset = 0;
  let paths = '';

  chargerMix.forEach((seg, i) => {
    const len = (seg.pct / 100) * C - gap;
    paths += '<circle class="donut-seg" data-i="' + i + '" cx="100" cy="100" r="' + R + '" stroke="' + seg.color + '" stroke-width="20" stroke-dasharray="0 ' + C + '" stroke-dashoffset="' + (-offset).toFixed(2) + '" data-final-dash="' + len.toFixed(2) + ' ' + (C - len).toFixed(2) + '"/>';
    offset += (seg.pct / 100) * C;
  });

  svg.innerHTML = paths;

  setTimeout(() => {
    $$('.donut-seg', svg).forEach(el => {
      el.style.transition = 'stroke-dasharray 1.1s cubic-bezier(.22,1,.36,1)';
      el.style.strokeDasharray = el.dataset.finalDash;
    });
  }, 80);

  legend.innerHTML = chargerMix.map((seg, i) => (
    '<div class="dl-item" data-i="' + i + '">' +
      '<span class="dl-swatch" style="background:' + seg.color + '"></span>' +
      '<span class="dl-name">' + seg.name + '</span>' +
      '<span class="dl-val">' + seg.value.toLocaleString('en-IN') + '</span>' +
      '<span class="dl-pct">' + seg.pct + '%</span>' +
    '</div>'
  )).join('');

  $$('.dl-item', legend).forEach(item => {
    const i = +item.dataset.i;
    item.addEventListener('mouseenter', () => {
      $$('.donut-seg', svg).forEach(s => {
        s.style.opacity = (+s.dataset.i === i) ? '1' : '0.25';
      });
    });
    item.addEventListener('mouseleave', () => {
      $$('.donut-seg', svg).forEach(s => s.style.opacity = '1');
    });
  });
}

function renderAreaChart(){
  const svg = $('#areaChart');
  const W = 660, H = 268;
  const padL = 46, padR = 46, padT = 16, padB = 40;
  const iw = W - padL - padR;
  const ih = H - padT - padB;

  const sessions = [86, 92, 88, 104, 118, 112, 96, 102, 121, 134, 128, 142, 155, 148];
  const util     = [48, 52, 50, 58, 64, 61, 54, 57, 66, 71, 68, 74, 79, 76];
  const labels   = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14'];
  const n = sessions.length;

  const maxS = 180;
  const minU = 40, maxU = 90;

  const x  = i => padL + (i * iw) / (n - 1);
  const yS = v => padT + ih - (v / maxS) * ih;
  const yU = v => padT + ih - ((v - minU) / (maxU - minU)) * ih;

  const linePath = sessions.map((v, i) => (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + yS(v).toFixed(1)).join(' ');
  const areaPath = linePath + ' L ' + x(n-1).toFixed(1) + ' ' + (padT + ih) + ' L ' + x(0).toFixed(1) + ' ' + (padT + ih) + ' Z';
  const utilPath = util.map((v, i) => (i ? 'L' : 'M') + x(i).toFixed(1) + ' ' + yU(v).toFixed(1)).join(' ');

  let grid = '';
  [0, 45, 90, 135, 180].forEach(v => {
    const y = yS(v);
    grid += '<line class="grid-line" x1="' + padL + '" y1="' + y.toFixed(1) + '" x2="' + (W - padR) + '" y2="' + y.toFixed(1) + '"/>';
    grid += '<text class="axis-label" x="' + (padL - 10) + '" y="' + (y + 3.5).toFixed(1) + '" text-anchor="end">' + v + 'K</text>';
  });

  let xLabels = '';
  labels.forEach((l, i) => {
    if (i % 2 !== 0 && i !== n - 1) return;
    xLabels += '<text class="axis-label" x="' + x(i).toFixed(1) + '" y="' + (H - 14) + '" text-anchor="middle">Apr ' + l + '</text>';
  });

  const step = iw / (n - 1);
  let hits = '';
  for (let i = 0; i < n; i++) {
    hits += '<rect class="hit" data-i="' + i + '" x="' + (x(i) - step / 2).toFixed(1) + '" y="' + padT + '" width="' + step.toFixed(1) + '" height="' + ih + '"/>';
  }

  svg.innerHTML =
    '<defs>' +
      '<linearGradient id="areaFill" x1="0" y1="0" x2="0" y2="1">' +
        '<stop offset="0%" stop-color="#0E9F6E" stop-opacity="0.28"/>' +
        '<stop offset="60%" stop-color="#0E9F6E" stop-opacity="0.08"/>' +
        '<stop offset="100%" stop-color="#0E9F6E" stop-opacity="0"/>' +
      '</linearGradient>' +
      '<linearGradient id="lineStroke" x1="0" y1="0" x2="1" y2="0">' +
        '<stop offset="0%" stop-color="#0B8A5F"/>' +
        '<stop offset="100%" stop-color="#34D399"/>' +
      '</linearGradient>' +
    '</defs>' +
    grid +
    xLabels +
    '<path d="' + areaPath + '" fill="url(#areaFill)"/>' +
    '<path d="' + linePath + '" fill="none" stroke="url(#lineStroke)" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>' +
    '<path d="' + utilPath + '" fill="none" stroke="#1D2E48" stroke-width="1.9" stroke-dasharray="5 4" stroke-linecap="round" opacity="0.6"/>' +
    '<g id="hoverLayer" style="opacity:0">' +
      '<line class="crosshair" x1="0" y1="' + padT + '" x2="0" y2="' + (padT + ih) + '" style="opacity:1"/>' +
      '<circle class="hover-dot" r="5" fill="#0E9F6E" stroke="#fff" stroke-width="2.4" style="opacity:1"/>' +
      '<circle class="hover-dot" r="4" fill="#1D2E48" stroke="#fff" stroke-width="2" style="opacity:1"/>' +
    '</g>' +
    hits;

  const hoverLayer = $('#hoverLayer', svg);
  const chLine = hoverLayer.querySelector('line');
  const dots = hoverLayer.querySelectorAll('circle');

  $$('.hit', svg).forEach(rect => {
    rect.addEventListener('mouseenter', e => {
      const i = +rect.dataset.i;
      hoverLayer.style.opacity = '1';
      chLine.setAttribute('x1', x(i));
      chLine.setAttribute('x2', x(i));
      dots[0].setAttribute('cx', x(i));
      dots[0].setAttribute('cy', yS(sessions[i]));
      dots[1].setAttribute('cx', x(i));
      dots[1].setAttribute('cy', yU(util[i]));

      showTip(
        '<div class="tt-name">April ' + labels[i] + ', 2025</div>' +
        '<div class="tt-sub">National network performance</div>' +
        '<div class="tt-row"><span>Sessions</span><b>' + sessions[i] + 'K</b></div>' +
        '<div class="tt-row"><span>Utilisation</span><b>' + util[i] + '%</b></div>' +
        '<div class="tt-div"></div>' +
        '<div class="tt-row"><span>Peak load</span><b>' + (sessions[i] * 0.31).toFixed(1) + ' MW</b></div>',
        e.clientX, e.clientY
      );
    });
    rect.addEventListener('mousemove', e => {
      const r = tooltip.getBoundingClientRect();
      let left = e.clientX + 16, top = e.clientY - r.height / 2;
      if (left + r.width > window.innerWidth - 12) left = e.clientX - r.width - 16;
      top = Math.max(10, Math.min(top, window.innerHeight - r.height - 10));
      tooltip.style.left = left + 'px';
      tooltip.style.top = top + 'px';
    });
    rect.addEventListener('mouseleave', () => {
      hoverLayer.style.opacity = '0';
      hideTip();
    });
  });
}

function renderReadiness(){
  const wrap = $('#readiness');
  wrap.innerHTML = readiness.map(r => (
    '<div class="rr-row">' +
      '<div class="rr-top">' +
        '<div class="rr-name">' + r.name + ' <em>' + r.note + '</em></div>' +
        '<div class="rr-val" style="color:' + r.color + '">' + r.value + '%</div>' +
      '</div>' +
      '<div class="rr-track">' +
        '<div class="rr-fill" data-w="' + r.value + '" style="background:linear-gradient(90deg,' + r.color + 'AA,' + r.color + ')"></div>' +
        '<div class="rr-target" style="left:' + r.target + '%"></div>' +
      '</div>' +
    '</div>'
  )).join('');

  setTimeout(() => {
    $$('.rr-fill', wrap).forEach(el => { el.style.width = el.dataset.w + '%'; });
  }, 400);
}

const STATUS_MAP = {
  green: { bg:'var(--green-l)', c:'var(--green-d)', dot:'#10B981' },
  amber: { bg:'var(--amber-l)', c:'#B45309', dot:'#F59E0B' },
  red:   { bg:'var(--red-l)',   c:'#C0392B', dot:'#EF4444' }
};

function renderTable(rows){
  const body = $('#corridorBody');
  body.innerHTML = rows.map(r => {
    const s = STATUS_MAP[r.sc];
    const gapColor = r.gap >= 65 ? '#EF4444' : r.gap >= 45 ? '#F59E0B' : '#10B981';
    return (
      '<tr>' +
        '<td>' +
          '<div class="cell-corridor">' +
            '<div class="corridor-icon">' +
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="19" r="2.5"/><circle cx="18" cy="5" r="2.5"/><path d="M8.5 19H14a3.5 3.5 0 0 0 0-7h-4a3.5 3.5 0 0 1 0-7h5.5"/></svg>' +
            '</div>' +
            '<div>' +
              '<div class="corridor-name">' + r.name + '</div>' +
              '<div class="corridor-sub">' + r.sub + '</div>' +
            '</div>' +
          '</div>' +
        '</td>' +
        '<td class="cell-num">' + r.stations + '</td>' +
        '<td><span class="mini-bar"><i style="width:' + r.gap + '%;background:' + gapColor + '"></i></span><span class="cell-num" style="color:' + gapColor + '">' + r.gap + '</span></td>' +
        '<td><span class="mini-bar"><i style="width:' + r.util + '%;background:#0E9F6E"></i></span><span class="cell-num">' + r.util + '%</span></td>' +
        '<td><span class="status-pill" style="background:' + s.bg + ';color:' + s.c + '"><span class="sdot" style="background:' + s.dot + '"></span>' + r.status + '</span></td>' +
        '<td style="text-align:right"><button class="row-action" title="View details"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg></button></td>' +
      '</tr>'
    );
  }).join('');
}

function initTableSort(){
  let sortKey = null, dir = 1;
  $$('thead th.sortable').forEach(th => {
    th.addEventListener('click', () => {
      const key = th.dataset.sort;
      if (sortKey === key) dir *= -1; else { sortKey = key; dir = 1; }

      $$('thead th.sortable').forEach(t => {
        t.classList.remove('sorted');
        t.querySelector('.sort-ico').textContent = '▼';
      });
      th.classList.add('sorted');
      th.querySelector('.sort-ico').textContent = dir === 1 ? '▼' : '▲';

      const sorted = corridorRows.slice().sort((a, b) => {
        const map = { stations:'stations', gap:'gap', util:'util' };
        return (a[map[key]] - b[map[key]]) * dir;
      });
      renderTable(sorted);
    });
  });
}

function initNav(){
  $$('#mainNav .nav-item').forEach(btn => {
    btn.addEventListener('click', () => {
      $$('.nav-item').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const titleEl = $('#pageTitle');
      const subEl = $('#pageSub');
      titleEl.textContent = btn.dataset.title;
      subEl.textContent = btn.dataset.sub;

      const target = btn.dataset.target;
      if (target === 'top') {
        $('.main').scrollTo({ top: 0, behavior: 'smooth' });
      } else {
        const el = document.getElementById(target);
        if (el) {
          const y = el.offsetTop - 96;
          $('.main').scrollTo({ top: y, behavior: 'smooth' });
        }
      }
    });
  });

  $$('.nav-item[data-toast]').forEach(btn => {
    btn.addEventListener('click', () => {
      $$('.nav-item').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      toast(btn.dataset.toast);
    });
  });
}

function initMisc(){
  setTimeout(() => {
    const bar = $('.health-bar i');
    if (bar) bar.style.width = bar.dataset.w + '%';
  }, 500);

  const search = $('#globalSearch');
  search.addEventListener('keydown', e => {
    if (e.key === 'Enter' && search.value.trim()) {
      toast('Searching "' + search.value.trim() + '" across 27 regions…');
    }
  });
  document.addEventListener('keydown', e => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      search.focus();
    }
  });

  $('#analyzeBtn').addEventListener('click', () => {
    toast('Recomputing gap index across 21,486 charging points…');
  });

  $$('.card-head .filter').forEach(b => {
    if (b.textContent.includes('Export')) {
      b.addEventListener('click', () => toast('Corridor dataset exported as CSV.'));
    }
  });

  document.addEventListener('click', e => {
    const btn = e.target.closest('.row-action');
    if (btn) toast('Opening corridor detail view…');
  });

  document.addEventListener('click', e => {
    const item = e.target.closest('.gap-item');
    if (item) {
      const name = item.querySelector('.gap-name').textContent.split(' ')[0];
      toast('Filtering dashboard for ' + name + '…');
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  renderMap();
  initLayerToggles();
  initRadiusSlider();
  renderGapList();
  animateGauge();
  renderDonut();
  renderAreaChart();
  renderReadiness();
  renderTable(corridorRows);
  initTableSort();
  initNav();
  initMisc();

  requestAnimationFrame(() => {
    renderSparklines();
    animateCounters();
  });
});
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------
components.html(DASHBOARD_HTML, height=2600, scrolling=True)
