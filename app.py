import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import re
from datetime import datetime

# ============================================================
# PAGE CONFIG & CUSTOM CSS
# ============================================================
st.set_page_config(
    page_title="ChargeWise India — EV Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed", # Collapsed to give map more room
)

def md(html):
    st.markdown(re.sub(r"\n\s*", "", html).strip(), unsafe_allow_html=True)

# Inject CSS
md("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #F8FAFC;
    --surface: #FFFFFF;
    --text-main: #0F172A;
    --text-muted: #64748B;
    --emerald: #10B981;
    --emerald-dark: #047857;
    --forest: #064E3B;
    --border: #E2E8F0;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
    color: var(--text-main);
}
h1, h2, h3, h4 { font-family: 'Outfit', sans-serif; font-weight: 700; letter-spacing: -0.02em; }

#MainMenu, header[data-testid="stHeader"], footer {visibility: hidden; height: 0;}
.block-container {padding: 1rem 2rem 4rem !important; max-width: 1600px !important;}

/* Compact Hero */
.hero-container {
    background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    display: flex; justify-content: space-between; align-items: center;
    animation: fadeUp 0.8s ease-out both;
}
.hero-title { font-size: 2.8rem; line-height: 1.1; margin-bottom: 0.5rem; background: linear-gradient(90deg, #0F172A, #047857); -webkit-background-clip: text; -webkit-text-fill-color: transparent;}
.hero-subtitle { font-size: 1rem; color: var(--text-muted); max-width: 600px; line-height: 1.5; margin:0;}
.hero-badge { display: inline-flex; align-items: center; gap: 8px; background: rgba(16, 185, 129, 0.1); color: var(--emerald-dark); padding: 6px 14px; border-radius: 100px; font-weight: 600; font-size: 0.8rem; margin-bottom: 1rem; border: 1px solid rgba(16, 185, 129, 0.2);}
.hero-pulse { width: 8px; height: 8px; border-radius: 50%; background: var(--emerald); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); animation: pulse 2s infinite;}

/* KPI Strip */
.kpi-strip { display: flex; gap: 2rem; padding: 1.5rem; background: var(--surface); border: 1px solid var(--border); border-radius: 16px; margin-bottom: 1.5rem; animation: fadeUp 0.8s ease-out 0.1s both;}
.kpi-item { flex: 1; border-right: 1px solid var(--border); padding-right: 1.5rem;}
.kpi-item:last-child { border-right: none; }
.kpi-label { font-size: 0.8rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.4rem;}
.kpi-value { font-size: 2.2rem; font-weight: 800; font-family: 'Outfit'; color: var(--text-main); line-height: 1; }
.kpi-unit { font-size: 1rem; color: var(--text-muted); font-weight: 500; margin-left: 4px;}

/* Panel Cards */
.panel-card { background: var(--surface); border: 1px solid var(--border); border-radius: 16px; padding: 1.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02);}
.panel-title { font-size: 1.2rem; margin-bottom: 0.2rem;}
.panel-desc { font-size: 0.85rem; color: var(--text-muted); margin-bottom: 1.2rem;}

/* Gap List Items */
.gap-item { display: flex; align-items: center; gap: 1rem; padding: 0.8rem; border-bottom: 1px solid var(--border);}
.gap-item:last-child { border-bottom: none;}
.gap-rank { font-size: 1.2rem; font-weight: 800; color: #CBD5E1; width: 30px; font-family: 'Outfit';}
.gap-info h4 { margin: 0; font-size: 1rem;}
.gap-info p { margin: 0; font-size: 0.8rem; color: var(--text-muted);}
.gap-score { margin-left: auto; text-align: right;}
.gap-score span { font-size: 1.1rem; font-weight: 700; color: #EF4444;}

@keyframes fadeUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
@keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); } 100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); } }
</style>
""")

# ============================================================
# BACKEND: ROBUST DATA PIPELINE
# ============================================================

@st.cache_data(show_spinner=False)
def load_geojson():
    """Fetch high-quality India GeoJSON. Falls back safely."""
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json()
    except:
        return None

@st.cache_data
def generate_backend_data():
    """Simulates a real database of 500+ EV stations across India."""
    np.random.seed(42)
    
    # Real state centers and realistic base stats
    states = {
        "Maharashtra": (19.75, 75.71, 90, 15000), "Karnataka": (15.31, 75.71, 80, 12000),
        "Tamil Nadu": (11.12, 78.65, 75, 11000), "Delhi": (28.61, 77.20, 95, 18000),
        "Uttar Pradesh": (26.84, 80.94, 40, 8000), "Gujarat": (22.25, 71.19, 65, 9000),
        "Rajasthan": (27.02, 74.21, 35, 5000), "West Bengal": (22.98, 87.85, 60, 7000),
        "Telangana": (18.11, 79.01, 70, 10000), "Kerala": (10.85, 76.27, 55, 6000),
        "Madhya Pradesh": (22.97, 78.65, 45, 4000), "Bihar": (25.09, 85.31, 20, 3000),
        "Punjab": (31.14, 75.34, 50, 4500), "Haryana": (29.05, 76.08, 60, 6500),
        "Odisha": (20.95, 85.09, 35, 3500), "Assam": (26.20, 92.93, 25, 2000),
    }
    
    records = []
    for state, (lat, lon, base_gap, base_ev) in states.items():
        # Generate 15-25 stations per state
        n_stations = np.random.randint(15, 25)
        for _ in range(n_stations):
            # Slight coordinate jitter to spread stations naturally
            s_lat = lat + np.random.normal(0, 1.2)
            s_lon = lon + np.random.normal(0, 1.2)
            
            gap = int(np.clip(base_gap + np.random.normal(0, 10), 10, 98))
            ev_adopt = int(base_ev + np.random.normal(0, 1000))
            stations = int(np.random.randint(5, 50))
            
            # Logic: Priority = High Gap + High EV Adoption
            priority = (gap * 0.6) + ((ev_adopt / 20000) * 100 * 0.4)
            
            records.append({
                "state": state, "lat": s_lat, "lon": s_lon,
                "gap_index": gap, "ev_adoption": max(500, ev_adopt),
                "stations": stations, "priority_score": priority,
                "charger_type": np.random.choice(["DC Fast", "AC Type-2", "AC Slow"], p=[0.5, 0.35, 0.15])
            })
            
    return pd.DataFrame(records)

# Load Data
india_geo = load_geojson()
df_raw = generate_backend_data()

# ============================================================
# SIDEBAR FILTERS (The Engine Controls)
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ Data Controls")
    
    # Region Filter
    regions = ["All India", "North", "South", "East", "West", "Central", "Northeast"]
    selected_region = st.selectbox("Filter by Region", regions)
    
    # If a region is selected, filter states dynamically
    if selected_region != "All India":
        region_states = {
            "North": ["Delhi", "Uttar Pradesh", "Rajasthan", "Punjab", "Haryana"],
            "South": ["Karnataka", "Tamil Nadu", "Telangana", "Kerala"],
            "East": ["West Bengal", "Bihar", "Odisha"],
            "West": ["Maharashtra", "Gujarat"],
            "Central": ["Madhya Pradesh"],
            "Northeast": ["Assam"]
        }[selected_region]
        state_options = ["All States"] + region_states
    else:
        state_options = ["All States"] + sorted(df_raw["state"].unique().tolist())
        
    selected_state = st.selectbox("Filter by State", state_options)
    
    st.markdown("---")
    st.markdown("### 🗺️ Map Layers")
    show_choropleth = st.toggle("State Gap Heatmap", value=True)
    show_stations = st.toggle("Station Density", value=True)
    
    st.markdown("---")
    st.caption("Backend Engine: Active 🟢")
    st.caption(f"Processing {len(df_raw)} records.")

# ============================================================
# APPLY FILTERS (The Backend Logic)
# ============================================================
df_filtered = df_raw.copy()

# Apply Region
if selected_region != "All India":
    # Reverse lookup state to region for filtering
    state_to_region = {
        "Delhi": "North", "Uttar Pradesh": "North", "Rajasthan": "North", "Punjab": "North", "Haryana": "North",
        "Karnataka": "South", "Tamil Nadu": "South", "Telangana": "South", "Kerala": "South",
        "West Bengal": "East", "Bihar": "East", "Odisha": "East",
        "Maharashtra": "West", "Gujarat": "West",
        "Madhya Pradesh": "Central", "Assam": "Northeast"
    }
    df_filtered = df_filtered[df_filtered["state"].map(state_to_region) == selected_region]

# Apply State
if selected_state != "All States":
    df_filtered = df_filtered[df_filtered["state"] == selected_state]

# Calculate Live KPIs
total_stations = int(df_filtered["stations"].sum())
avg_gap = round(df_filtered["gap_index"].mean(), 1) if len(df_filtered) > 0 else 0
states_covered = df_filtered["state"].nunique()
critical_zones = len(df_filtered[df_filtered["gap_index"] > 70])

# ============================================================
# UI: HERO
# ============================================================
md(f"""
<div class="hero-container">
    <div>
        <div class="hero-badge"><div class="hero-pulse"></div> System Online · {len(df_filtered)} Nodes Active</div>
        <h1 class="hero-title">Powering India's Electric Future.</h1>
        <p class="hero-subtitle">Discover charging infrastructure, uncover underserved regions, and explore the next frontier of India's EV mobility network.</p>
    </div>
    <div style="text-align:right; display:none;">
        <!-- Hidden element to balance flexbox -->
    </div>
</div>
""")

# ============================================================
# UI: KPI STRIP
# ============================================================
md(f"""
<div class="kpi-strip">
    <div class="kpi-item">
        <div class="kpi-label">Total Charging Points</div>
        <div class="kpi-value">{total_stations:,}</div>
    </div>
    <div class="kpi-item">
        <div class="kpi-label">States Represented</div>
        <div class="kpi-value">{states_covered}<span class="kpi-unit">/ 36</span></div>
    </div>
    <div class="kpi-item">
        <div class="kpi-label">Avg Network Gap</div>
        <div class="kpi-value">{avg_gap}<span class="kpi-unit">/ 100</span></div>
    </div>
    <div class="kpi-item">
        <div class="kpi-label">Zones Flagged</div>
        <div class="kpi-value" style="color:#EF4444;">{critical_zones}</div>
    </div>
</div>
""")

# ============================================================
# UI: THE INTERACTIVE MAP & GAP FINDER (Command Center)
# ============================================================
col_map, col_gap = st.columns([1.8, 1], gap="large")

with col_map:
    md("""
    <div class="panel-card" style="margin-bottom: 1rem; padding-bottom:0;">
        <h3 class="panel-title">Geospatial Intelligence</h3>
        <p class="panel-desc">Interactive state-level gap analysis and station density.</p>
    </div>
    """)
    
    if india_geo:
        # State aggregates for choropleth
        state_agg = df_filtered.groupby("state").agg(
            gap=("gap_index", "mean"),
            stations=("stations", "sum")
        ).reset_index()

        fig = go.Figure()

        # Layer 1: State Gap Choropleth
        if show_choropleth:
            fig.add_trace(go.Choropleth(
                geojson=india_geo,
                locations=state_agg["state"],
                z=state_agg["gap"],
                featureidkey="properties.ST_NM",
                colorscale=[
                    [0, "#D1FAE5"], [0.4, "#FDE68A"], [0.7, "#FCA5A5"], [1, "#EF4444"]
                ],
                zmin=10, zmax=90,
                marker_line_color="#FFFFFF", marker_line_width=1,
                colorbar=dict(title="Gap Index", thickness=10, len=0.6, x=1.0),
                hovertemplate="<b>%{location}</b><br>Gap Index: %{z:.1f}<extra></extra>",
                name="State Gap"
            ))

        # Layer 2: Station Bubbles
        if show_stations:
            fig.add_trace(go.Scattergeo(
                lon=df_filtered["lon"], lat=df_filtered["lat"],
                mode="markers",
                marker=dict(
                    size=df_filtered["stations"] / 10 + 4,
                    color="#0F172A", line=dict(color="#FFFFFF", width=1), opacity=0.8
                ),
                hovertemplate="<b>Station</b><br>%{customdata[0]}<br>Stations: %{customdata[1]}<extra></extra>",
                customdata=np.stack((df_filtered["state"], df_filtered["stations"]), axis=-1),
                name="Stations"
            ))

        # VECTOR MAP RENDERING (Fixes Streamlit Cloud blank map)
        fig.update_geos(
            fitbounds="locations", visible=False, projection_type="mercator",
            showcountries=True, countrycolor="#E2E8F0", showcoastlines=True, coastlinecolor="#E2E8F0"
        )
        
        fig.update_layout(
            height=500, margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter"), hoverlabel=dict(bgcolor="#0F172A", font=dict(color="#fff"))
        )
        
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.error("Map data offline.")

with col_gap:
    md("""
    <div class="panel-card" style="height: 100%;">
        <h3 class="panel-title">Charging Gap Finder</h3>
        <p class="panel-desc">Regions flagged for investigation based on high EV adoption but low infrastructure.</p>
    """)
    
    # Gap logic
    gap_df = df_filtered.sort_values("priority_score", ascending=False).head(6)
    
    for i, (_, row) in enumerate(gap_df.iterrows()):
        bar_color = "#EF4444" if row['priority_score'] > 70 else "#F59E0B"
        md(f"""
        <div class="gap-item">
            <div class="gap-rank">#{i+1}</div>
            <div class="gap-info">
                <h4>{row['state']}</h4>
                <p>{row['ev_adoption']:,} EVs vs {row['stations']} points</p>
            </div>
            <div class="gap-score">
                <span style="color:{bar_color};">{row['priority_score']:.0f}</span>
                <div style="font-size:0.65rem; color:#64748B;">SCORE</div>
            </div>
        </div>
        """)
    
    md("</div>")

# ============================================================
# CHARTS SECTION
# ============================================================
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns(2, gap="large")

with col1:
    md("""
    <div class="panel-card">
        <h3 class="panel-title">Infrastructure Distribution</h3>
        <p class="panel-desc">Station count by state in current view.</p>
    </div>
    """)
    
    bar_data = df_filtered.groupby("state")["stations"].sum().reset_index().sort_values("stations", ascending=True).tail(8)
    fig_bar = go.Figure(go.Bar(
        x=bar_data["stations"], y=bar_data["state"], orientation="h",
        marker=dict(color="#047857", cornerradius=4),
        hovertemplate="<b>%{y}</b><br>%{x} Stations<extra></extra>"
    ))
    fig_bar.update_layout(
        height=300, margin=dict(l=0, r=0, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False), yaxis=dict(showgrid=False, tickfont=dict(size=12, color="#0F172A"))
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

with col2:
    md("""
    <div class="panel-card">
        <h3 class="panel-title">Charger Type Mix</h3>
        <p class="panel-desc">Distribution of charger technologies.</p>
    </div>
    """)
    
    pie_data = df_filtered.groupby("charger_type")["stations"].sum().reset_index()
    fig_pie = go.Figure(go.Pie(
        labels=pie_data["charger_type"], values=pie_data["stations"], hole=0.6,
        marker=dict(colors=["#047857", "#10B981", "#94A3B8"]),
        textinfo="percent", textfont=dict(size=12, color="#fff")
    ))
    fig_pie.update_layout(
        height=300, margin=dict(l=0, r=0, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True, legend=dict(orientation="h", y=-0.1)
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
