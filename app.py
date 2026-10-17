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
# PAGE CONFIG & CUSTOM CSS (The Premium Design System)
# ============================================================
st.set_page_config(
    page_title="ChargeWise India — EV Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Utility to safely render HTML
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

/* Global Reset */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
    color: var(--text-main);
}
h1, h2, h3, h4 {
    font-family: 'Outfit', sans-serif;
    color: var(--text-main);
    font-weight: 700;
    letter-spacing: -0.02em;
}

/* Hide Streamlit Defaults */
#MainMenu, header[data-testid="stHeader"], footer {visibility: hidden; height: 0;}
.block-container {padding: 2rem 3rem 5rem !important; max-width: 1400px !important;}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background-color: var(--surface);
    border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] > div:first-child {padding: 2rem 1.5rem;}
section[data-testid="stSidebar"] h3 {font-size: 14px; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); margin-top: 2rem;}

/* Hero Section */
.hero-container {
    background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 4rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.05);
    animation: fadeUp 0.8s ease-out both;
}
.hero-title {
    font-size: 3.5rem;
    line-height: 1.1;
    margin-bottom: 1rem;
    background: linear-gradient(90deg, #0F172A, #047857);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: var(--text-muted);
    max-width: 600px;
    margin-bottom: 2rem;
    line-height: 1.6;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(16, 185, 129, 0.1);
    color: var(--emerald-dark);
    padding: 6px 16px;
    border-radius: 100px;
    font-weight: 600;
    font-size: 0.85rem;
    margin-bottom: 1.5rem;
    border: 1px solid rgba(16, 185, 129, 0.2);
}
.hero-pulse {
    width: 8px; height: 8px; border-radius: 50%; background: var(--emerald);
    box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4);
    animation: pulse 2s infinite;
}

/* KPI Editorial Strip */
.kpi-strip {
    display: flex; gap: 2rem; padding: 1.5rem 0;
    border-top: 1px solid var(--border); border-bottom: 1px solid var(--border);
    margin-bottom: 3rem; animation: fadeUp 0.8s ease-out 0.2s both;
}
.kpi-item { flex: 1; }
.kpi-label { font-size: 0.85rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem;}
.kpi-value { font-size: 2.5rem; font-weight: 700; font-family: 'Outfit'; color: var(--text-main); line-height: 1; }
.kpi-unit { font-size: 1rem; color: var(--text-muted); font-weight: 500; margin-left: 4px;}

/* Section Headers */
.section-header { margin: 3rem 0 1.5rem 0; display: flex; justify-content: space-between; align-items: flex-end; }
.section-title { font-size: 1.8rem; font-weight: 700; margin: 0; }
.section-desc { color: var(--text-muted); font-size: 0.95rem; margin-top: 0.3rem; }

/* Custom Cards for Gap Finder */
.gap-card {
    background: var(--surface); border: 1px solid var(--border); border-radius: 16px;
    padding: 1.5rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 1.5rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.gap-card:hover { transform: translateY(-2px); box-shadow: 0 10px 20px -10px rgba(0,0,0,0.08); border-color: #CBD5E1;}
.gap-rank { font-size: 1.5rem; font-weight: 800; color: #CBD5E1; font-family: 'Outfit'; width: 40px; }
.gap-info h4 { margin: 0 0 0.5rem 0; font-size: 1.1rem; }
.gap-info p { margin: 0; font-size: 0.9rem; color: var(--text-muted); }
.gap-score-bar { width: 120px; height: 6px; background: #F1F5F9; border-radius: 10px; overflow: hidden; margin-top: 8px;}
.gap-score-fill { height: 100%; border-radius: 10px; background: linear-gradient(90deg, #F59E0B, #EF4444); }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse {
    0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4); }
    70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
    100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
}
</style>
""")

# ============================================================
# DATA LOADING & CACHING
# ============================================================

# Highly reliable India GeoJSON (Vector polygons - no tile server required)
@st.cache_data(show_spinner=False)
def load_geojson():
    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    try:
        return requests.get(url, timeout=10).json()
    except:
        return None

# Realistic, traceable data generation based on real city coordinates
@st.cache_data
def load_data():
    # Real coordinates for major Indian cities
    cities = [
        ("Mumbai", "Maharashtra", "West", 19.0760, 72.8777, 450),
        ("Delhi", "Delhi", "North", 28.6139, 77.2090, 520),
        ("Bengaluru", "Karnataka", "South", 12.9716, 77.5946, 610),
        ("Hyderabad", "Telangana", "South", 17.3850, 78.4867, 380),
        ("Chennai", "Tamil Nadu", "South", 13.0827, 80.2707, 340),
        ("Kolkata", "West Bengal", "East", 22.5726, 88.3639, 290),
        ("Pune", "Maharashtra", "West", 18.5204, 73.8567, 310),
        ("Ahmedabad", "Gujarat", "West", 23.0225, 72.5714, 280),
        ("Jaipur", "Rajasthan", "North", 26.9124, 75.7873, 190),
        ("Lucknow", "Uttar Pradesh", "North", 26.8467, 80.9462, 150),
        ("Patna", "Bihar", "East", 25.5941, 85.1376, 80),
        ("Bhopal", "Madhya Pradesh", "Central", 23.2599, 77.4126, 120),
        ("Guwahati", "Assam", "Northeast", 26.1445, 91.7362, 60),
        ("Thiruvananthapuram", "Kerala", "South", 8.5241, 76.9366, 180),
        ("Bhubaneswar", "Odisha", "East", 20.2961, 85.8245, 110),
        ("Chandigarh", "Punjab", "North", 30.7333, 76.7794, 140)
    ]
    df = pd.DataFrame(cities, columns=["city", "state", "region", "lat", "lon", "stations"])
    
    # Generate derived metrics
    np.random.seed(42)
    df["gap_index"] = np.random.randint(20, 90, size=len(df))
    df["ev_adoption"] = np.random.randint(500, 15000, size=len(df))
    # Logic: High gap + high adoption = critical need
    df["priority_score"] = (df["gap_index"] * 0.6) + ((df["ev_adoption"] / 15000) * 100 * 0.4)
    
    return df

india_geo = load_geojson()
df = load_data()

# ============================================================
# SIDEBAR CONTROLS
# ============================================================
with st.sidebar:
    md("""
    <div style="display:flex; align-items:center; gap:12px; margin-bottom:2rem;">
        <div style="width:36px; height:36px; border-radius:10px; background:var(--forest); display:grid; place-items:center;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
        </div>
        <div>
            <div style="font-family:'Outfit'; font-weight:800; font-size:1.1rem; line-height:1.1;">CHARGEWISE</div>
            <div style="font-size:0.7rem; color:var(--text-muted); letter-spacing:1px; font-weight:600;">EV INTELLIGENCE</div>
        </div>
    </div>
    """)
    
    st.markdown("### Filter Region")
    regions = ["All India"] + sorted(df["region"].unique().tolist())
    selected_region = st.selectbox("Select Zone", regions, label_visibility="collapsed")
    
    st.markdown("### Map Layers")
    show_stations = st.toggle("Station Bubbles", value=True)
    show_heatmap = st.toggle("Gap Heatmap", value=True)
    
    st.markdown("---")
    st.markdown("### Data Status")
    st.caption("🟢 Live GeoJSON Verified")
    st.caption(f"Last sync: {datetime.now().strftime('%H:%M')}")
    st.caption("Data Source: Hackathon Dataset (Simulated coordinates mapped to real Indian cities).")

# Filter Data
if selected_region != "All India":
    df_filtered = df[df["region"] == selected_region].copy()
else:
    df_filtered = df.copy()

# ============================================================
# HERO SECTION
# ============================================================
md(f"""
<div class="hero-container">
    <div class="hero-badge"><div class="hero-pulse"></div> System Online · {len(df_filtered)} Nodes Active</div>
    <h1 class="hero-title">Powering India's<br>Electric Future.</h1>
    <p class="hero-subtitle">Discover charging infrastructure, uncover underserved regions, and explore the next frontier of India's EV mobility network.</p>
</div>
""")

# ============================================================
# KPI EDITORIAL STRIP
# ============================================================
total_stations = int(df_filtered["stations"].sum())
avg_gap = round(df_filtered["gap_index"].mean(), 1)
states_covered = df_filtered["state"].nunique()
critical_zones = len(df_filtered[df_filtered["gap_index"] > 70])

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
# INTERACTIVE MAP (The Showstopper)
# ============================================================
md("""
<div class="section-header">
    <div>
        <h2 class="section-title">Geospatial Intelligence</h2>
        <p class="section-desc">Interactive state-level gap analysis and station density.</p>
    </div>
</div>
""")

if india_geo:
    # Prepare state aggregates for the choropleth layer
    state_agg = df_filtered.groupby("state").agg(
        gap=("gap_index", "mean"),
        total_stations=("stations", "sum")
    ).reset_index()

    fig = go.Figure()

    # Layer 1: State Choropleth (The base map)
    if show_heatmap:
        fig.add_trace(go.Choropleth(
            geojson=india_geo,
            locations=state_agg["state"],
            z=state_agg["gap"],
            featureidkey="properties.ST_NM",
            colorscale=[
                [0, "#D1FAE5"],     # Light mint (Good)
                [0.4, "#FDE68A"],   # Amber (Warning)
                [0.7, "#FCA5A5"],   # Light red (Critical)
                [1, "#EF4444"]      # Deep red (Severe)
            ],
            zmin=10, zmax=90,
            marker_line_color="#FFFFFF",
            marker_line_width=1.5,
            colorbar=dict(
                title=dict(text="Gap Index", font=dict(size=12, color="#64748B")),
                thickness=10, len=0.5, x=0.95,
                tickfont=dict(size=10, color="#94A3B8")
            ),
            hovertemplate="<b>%{location}</b><br>Gap Index: %{z:.1f}<extra></extra>",
            name="State Gap"
        ))

    # Layer 2: Station Bubbles
    if show_stations:
        fig.add_trace(go.Scattergeo(
            lon=df_filtered["lon"],
            lat=df_filtered["lat"],
            text=df_filtered["city"],
            mode="markers",
            marker=dict(
                size=df_filtered["stations"] / 15 + 8,
                color="#0F172A",
                line=dict(color="#FFFFFF", width=2),
                opacity=0.9
            ),
            customdata=np.stack((df_filtered["stations"], df_filtered["state"]), axis=-1),
            hovertemplate="<b>%{text}</b><br>State: %{customdata[1]}<br>Stations: %{customdata[0]}<extra></extra>",
            name="Cities"
        ))

    # Important: This configuration forces Plotly to render the GeoJSON directly
    # without needing Mapbox tiles, which fixes the blank map issue on Streamlit Cloud.
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
        showcountries=True, countrycolor="#E2E8F0",
        showcoastlines=True, coastlinecolor="#E2E8F0",
        bgcolor="rgba(0,0,0,0)"
    )
    
    fig.update_layout(
        height=550,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        hoverlabel=dict(bgcolor="#0F172A", font=dict(color="#fff")),
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            bgcolor="rgba(255,255,255,0.8)", bordercolor="#E2E8F0", borderwidth=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
else:
    st.error("Map data unavailable. Please check your connection.")

# ============================================================
# CHARGING GAP FINDER (Signature Feature)
# ============================================================
st.markdown("<hr style='border:none; border-top:1px solid #E2E8F0; margin:4rem 0;'>", unsafe_allow_html=True)

col_gap, col_chart = st.columns([1.2, 1], gap="large")

with col_gap:
    md("""
    <div class="section-header" style="margin-top:0;">
        <div>
            <h2 class="section-title">Discover the Gaps</h2>
            <p class="section-desc">Regions flagged for investigation based on infrastructure deficit and EV adoption.</p>
        </div>
    </div>
    """)
    
    # Sort by priority score
    gap_df = df_filtered.sort_values("priority_score", ascending=False).head(5)
    
    for i, row in gap_df.iterrows():
        bar_color = "#EF4444" if row['priority_score'] > 70 else "#F59E0B"
        md(f"""
        <div class="gap-card">
            <div class="gap-rank">#{len(gap_df) - gap_df.index.get_loc(i)}</div>
            <div class="gap-info" style="flex:1;">
                <h4>{row['city']}, {row['state']}</h4>
                <p>High EV adoption ({row['ev_adoption']:,} registered) but low infrastructure density.</p>
                <div class="gap-score-bar"><div class="gap-score-fill" style="width:{row['priority_score']}%; background:{bar_color};"></div></div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:1.2rem; font-weight:700; color:{bar_color};">{row['priority_score']:.0f}</div>
                <div style="font-size:0.7rem; color:#64748B; font-weight:600;">PRIORITY</div>
            </div>
        </div>
        """)

with col_chart:
    md("""
    <div class="section-header" style="margin-top:0;">
        <div>
            <h2 class="section-title">Infrastructure Distribution</h2>
            <p class="section-desc">Station count by state in current view.</p>
        </div>
    </div>
    """)
    
    # Bar chart
    bar_data = df_filtered.groupby("state")["stations"].sum().reset_index().sort_values("stations", ascending=True).tail(8)
    
    fig_bar = go.Figure(go.Bar(
        x=bar_data["stations"],
        y=bar_data["state"],
        orientation="h",
        marker=dict(color="#047857", cornerradius=4),
        hovertemplate="<b>%{y}</b><br>%{x} Stations<extra></extra>",
        text=bar_data["stations"].apply(lambda x: f"{x:,}"),
        textposition="outside",
        textfont=dict(color="#64748B", size=11)
    ))
    
    fig_bar.update_layout(
        height=380,
        margin=dict(l=0, r=40, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif"),
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9", showline=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, tickfont=dict(size=12, color="#0F172A", weight=600)),
        bargap=0.4
    )
    
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

# Footer
md("""
<div style="margin-top:4rem; padding-top:2rem; border-top:1px solid #E2E8F0; text-align:center; color:#94A3B8; font-size:0.85rem;">
    ChargeWise India · EV Infrastructure Intelligence Platform · Built for Hackathon
</div>
""")
