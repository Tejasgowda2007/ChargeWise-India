import math
import os

import pandas as pd
import plotly.express as px
import streamlit as st

# ----------------------------------------------------------------------------
# Page setup + theme
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="ChargeWise India",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

PRIMARY = "#38bdf8"
BG = "#0b1120"
CARD = "#172238"
BORDER = "#263852"
TIER_COLORS = {"Tier 1": "#38bdf8", "Tier 2": "#818cf8", "Tier 3": "#34d399"}

st.markdown(
    f"""
<style>
.stApp {{background:{BG};color:#f1f5f9}}
.block-container {{padding-top:1.5rem;max-width:1400px}}
section[data-testid="stSidebar"] {{background:#0f172a;border-right:1px solid {BORDER}}}
[data-testid="stMetric"] {{
    background:linear-gradient(145deg,{CARD},#111c30);
    padding:16px 18px;border-radius:14px;border:1px solid {BORDER};
}}
[data-testid="stMetricLabel"] {{color:#94a3b8}}
[data-testid="stMetricValue"] {{color:#f8fafc;font-weight:700}}
h1,h2,h3 {{color:#f8fafc !important;letter-spacing:-0.01em}}
.hero {{
    background:linear-gradient(120deg,#0c4a6e 0%,#1e1b4b 100%);
    border:1px solid {BORDER};border-radius:18px;padding:26px 30px;margin-bottom:18px;
}}
.hero h1 {{margin:0;font-size:2.1rem;color:#fff !important}}
.hero p {{margin:6px 0 0 0;color:#cbd5e1;font-size:1.02rem}}
.badge {{
    display:inline-block;background:#0ea5e922;color:{PRIMARY};border:1px solid #0ea5e955;
    padding:3px 12px;border-radius:999px;font-size:0.78rem;margin-top:12px;margin-right:6px;
}}
.insight {{
    background:{CARD};border-left:4px solid {PRIMARY};border-radius:8px;
    padding:12px 16px;margin:8px 0;color:#e2e8f0;
}}
.stTabs [data-baseweb="tab-list"] {{gap:6px}}
.stTabs [data-baseweb="tab"] {{
    background:{CARD};border-radius:10px 10px 0 0;padding:8px 18px;color:#94a3b8;
}}
.stTabs [aria-selected="true"] {{color:{PRIMARY} !important;border-bottom:2px solid {PRIMARY}}}
footer {{visibility:hidden}}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Data
# Source: PIB / Ministry of Heavy Industries / BEE (reporting date 1 April 2025)
# State totals only - not individual station coordinates.
# ----------------------------------------------------------------------------
DATA = [
    ("Andaman and Nicobar Islands", 4, 0, 0, 4),
    ("Andhra Pradesh", 0, 153, 463, 616),
    ("Arunachal Pradesh", 0, 0, 42, 42),
    ("Assam", 0, 22, 279, 301),
    ("Bihar", 0, 34, 360, 394),
    ("Chandigarh", 0, 14, 0, 14),
    ("Chhattisgarh", 0, 82, 218, 300),
    ("Delhi", 1951, 0, 0, 1951),
    ("Dadra and Nagar Haveli and Daman and Diu", 0, 0, 6, 6),
    ("Goa", 0, 0, 155, 155),
    ("Gujarat", 192, 254, 562, 1008),
    ("Haryana", 0, 191, 617, 808),
    ("Himachal Pradesh", 0, 0, 95, 95),
    ("Jammu and Kashmir", 0, 42, 116, 158),
    ("Jharkhand", 0, 100, 177, 277),
    ("Karnataka", 4626, 285, 969, 5880),
    ("Kerala", 0, 711, 577, 1288),
    ("Lakshadweep", 0, 0, 1, 1),
    ("Madhya Pradesh", 0, 220, 834, 1054),
    ("Maharashtra", 2454, 508, 784, 3746),
    ("Manipur", 0, 0, 50, 50),
    ("Meghalaya", 0, 0, 43, 43),
    ("Mizoram", 0, 0, 13, 13),
    ("Nagaland", 0, 0, 36, 36),
    ("Odisha", 0, 82, 451, 533),
    ("Puducherry", 0, 39, 3, 42),
    ("Punjab", 0, 161, 446, 607),
    ("Rajasthan", 0, 373, 877, 1250),
    ("Sikkim", 0, 0, 11, 11),
    ("Tamil Nadu", 218, 459, 847, 1524),
    ("Telangana", 238, 47, 691, 976),
    ("Tripura", 0, 0, 54, 54),
    ("Uttar Pradesh", 0, 756, 1381, 2137),
    ("Uttarakhand", 0, 71, 131, 202),
    ("West Bengal", 23, 21, 747, 791),
]

GEOJSON_FILE = "india_states.geojson"      # optional: put this file next to app.py
GEOJSON_KEY = "properties.ST_NM"           # change to match your GeoJSON's state-name field


@st.cache_data
def load_data() -> pd.DataFrame:
    d = pd.DataFrame(DATA, columns=["State", "Tier 1", "Tier 2", "Tier 3", "Total"])
    d["Share of India (%)"] = (d["Total"] / d["Total"].sum() * 100).round(2)
    d["Rank"] = d["Total"].rank(ascending=False, method="min").astype(int)
    return d


df = load_data()
TOTAL = int(df["Total"].sum())
tier_totals = {t: int(df[t].sum()) for t in ["Tier 1", "Tier 2", "Tier 3"]}


def style(fig, height=420):
    """Apply one consistent look to every chart."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=10, r=10, t=50, b=10),
        font=dict(family="Inter, sans-serif", color="#e2e8f0"),
        title_font=dict(size=16),
        legend=dict(orientation="h", y=-0.15),
    )
    fig.update_xaxes(gridcolor="#1e293b")
    fig.update_yaxes(gridcolor="#1e293b")
    return fig


# ----------------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚡ ChargeWise India")
    st.caption("EV infrastructure planning prototype")
    st.divider()
    tier_pick = st.multiselect(
        "City tiers to include",
        ["Tier 1", "Tier 2", "Tier 3"],
        default=["Tier 1", "Tier 2", "Tier 3"],
        help="Recalculates totals across the whole dashboard.",
    )
    st.divider()
    st.caption("Data: BEE / Ministry of Heavy Industries via PIB")
    st.caption("Reported: 1 April 2025 (not a live count)")

if not tier_pick:
    st.warning("Select at least one city tier in the sidebar.")
    st.stop()

# Recompute "Selected" total from the chosen tiers
df["Selected"] = df[tier_pick].sum(axis=1)
SEL_TOTAL = int(df["Selected"].sum())

# ----------------------------------------------------------------------------
# Hero + KPIs
# ----------------------------------------------------------------------------
st.markdown(
    """
<div class="hero">
  <h1>⚡ ChargeWise India</h1>
  <p>EV infrastructure mapping &amp; charging gap analysis across Indian states and UTs</p>
  <span class="badge">Official BEE data</span>
  <span class="badge">As of 1 April 2025</span>
  <span class="badge">35 states &amp; UTs</span>
</div>
""",
    unsafe_allow_html=True,
)

ranked = df.sort_values("Selected", ascending=False).reset_index(drop=True)
top_state = ranked.loc[0, "State"]
top3_share = ranked.head(3)["Selected"].sum() / SEL_TOTAL * 100
tier3_share = df["Tier 3"].sum() / TOTAL * 100

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Public charging stations", f"{SEL_TOTAL:,}")
k2.metric("States & UTs", len(df))
k3.metric("Leading state", top_state, f"{ranked.loc[0, 'Selected']:,} stations", delta_color="off")
k4.metric("Top-3 states' share", f"{top3_share:.0f}%")
k5.metric("Tier 3 share (all tiers)", f"{tier3_share:.0f}%")

# ----------------------------------------------------------------------------
# Tabs
# ----------------------------------------------------------------------------
tab_over, tab_state, tab_gap, tab_proj, tab_data = st.tabs(
    ["📊 Overview", "🗺️ State Explorer", "🎯 Gap Analysis", "📈 Projection", "📚 Data & Method"]
)

# ---------------------------- OVERVIEW --------------------------------------
with tab_over:
    st.markdown(
        f"""
<div class="insight"><b>Key insight:</b> The top 3 states ({', '.join(ranked.head(3)['State'])})
hold <b>{top3_share:.0f}%</b> of reported stations, so infrastructure is heavily concentrated.</div>
<div class="insight"><b>Coverage:</b> {int((df['Selected'] < 100).sum())} of {len(df)} states/UTs
report fewer than 100 stations in the selected tiers.</div>
""",
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.5, 1])
    with left:
        top12 = ranked.head(12)["State"].tolist()
        long = (
            df[df["State"].isin(top12)]
            .melt(id_vars="State", value_vars=tier_pick, var_name="Tier", value_name="Stations")
        )
        fig = px.bar(
            long,
            x="Stations",
            y="State",
            color="Tier",
            orientation="h",
            color_discrete_map=TIER_COLORS,
            category_orders={"State": top12[::-1]},
            title="Top 12 states by public charging stations (stacked by tier)",
        )
        st.plotly_chart(style(fig, 460), use_container_width=True)

    with right:
        tdf = pd.DataFrame(
            {"Tier": tier_pick, "Stations": [tier_totals[t] for t in tier_pick]}
        )
        fig2 = px.pie(
            tdf, names="Tier", values="Stations", hole=0.55,
            color="Tier", color_discrete_map=TIER_COLORS,
            title="Stations by city tier",
        )
        fig2.update_traces(textinfo="percent+label")
        st.plotly_chart(style(fig2, 460), use_container_width=True)

    # Optional choropleth: only shown if a GeoJSON file is present in the repo
    if os.path.exists(GEOJSON_FILE):
        import json

        with open(GEOJSON_FILE, encoding="utf-8") as f:
            geo = json.load(f)
        fig3 = px.choropleth(
            df, geojson=geo, locations="State", featureidkey=GEOJSON_KEY,
            color="Selected", color_continuous_scale="Blues",
            title="Public charging stations by state",
        )
        fig3.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(style(fig3, 560), use_container_width=True)
    else:
        st.caption(
            f"💡 Add `{GEOJSON_FILE}` (India state boundaries) next to app.py "
            "to enable the state choropleth map here."
        )

# ---------------------------- STATE EXPLORER --------------------------------
with tab_state:
    c1, c2 = st.columns([3, 1])
    selected = c1.multiselect(
        "Compare states",
        df["State"].tolist(),
        default=["Karnataka", "Maharashtra", "Uttar Pradesh", "Tamil Nadu", "Kerala"],
    )
    sort_by = c2.selectbox("Sort by", ["Selected"] + tier_pick)

    if selected:
        f = df[df["State"].isin(selected)].sort_values(sort_by)
        long = f.melt(id_vars="State", value_vars=tier_pick, var_name="Tier", value_name="Stations")
        fig = px.bar(
            long, x="State", y="Stations", color="Tier", barmode="group",
            color_discrete_map=TIER_COLORS,
            category_orders={"State": f["State"].tolist()},
            title="Stations by tier for selected states",
        )
        st.plotly_chart(style(fig, 420), use_container_width=True)

        st.dataframe(
            f[["Rank", "State"] + tier_pick + ["Selected", "Share of India (%)"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Selected": st.column_config.ProgressColumn(
                    "Total (selected tiers)", min_value=0,
                    max_value=int(df["Selected"].max()), format="%d",
                ),
                "Share of India (%)": st.column_config.NumberColumn(format="%.2f%%"),
            },
        )
    else:
        st.info("Pick at least one state to compare.")

# ---------------------------- GAP ANALYSIS ----------------------------------
with tab_gap:
    st.subheader("Charging Gap Finder")
    st.caption(
        "Station counts alone don't prove a gap. Upload EV registrations (e.g. from VAHAN) "
        "to compute EVs per charging station and the chargers needed to hit a target ratio."
    )

    template = pd.DataFrame({"State": df["State"], "EVs": ""})
    cA, cB = st.columns([1, 2])
    cA.download_button(
        "⬇️ Download CSV template",
        template.to_csv(index=False).encode("utf-8"),
        "ev_registrations_template.csv",
        "text/csv",
    )
    up = cB.file_uploader("Upload EV registrations CSV (columns: State, EVs)", type="csv")

    if up is not None:
        ev = pd.read_csv(up)
        ev.columns = [c.strip() for c in ev.columns]
        if not {"State", "EVs"}.issubset(ev.columns):
            st.error("CSV must have the columns `State` and `EVs`.")
        else:
            ev["EVs"] = pd.to_numeric(ev["EVs"], errors="coerce")
            ev = ev.dropna(subset=["EVs"])
            ev["key"] = ev["State"].str.strip().str.lower()
            base = df.assign(key=df["State"].str.lower())
            gap = base.merge(ev[["key", "EVs"]], on="key", how="inner")

            unmatched = sorted(set(ev["State"]) - set(gap["State"]))
            if unmatched:
                st.warning("Names not matched to the dataset: " + ", ".join(unmatched))

            target = st.slider(
                "Target: EVs per public charging station", 5, 100, 20,
                help="Your planning assumption; change it to test scenarios.",
            )
            gap["EVs per station"] = (gap["EVs"] / gap["Total"].replace(0, pd.NA)).astype(float).round(1)
            gap["Stations needed"] = gap.apply(
                lambda r: max(0, math.ceil(r["EVs"] / target - r["Total"])), axis=1
            )
            gap = gap.sort_values("EVs per station", ascending=False)

            g1, g2, g3 = st.columns(3)
            g1.metric("States analysed", len(gap))
            g2.metric("Most stretched", gap.iloc[0]["State"], f"{gap.iloc[0]['EVs per station']} EVs/station", delta_color="off")
            g3.metric("Extra stations to hit target", f"{int(gap['Stations needed'].sum()):,}")

            fig = px.bar(
                gap.head(15), x="EVs per station", y="State", orientation="h",
                color="EVs per station", color_continuous_scale="Reds",
                category_orders={"State": gap.head(15)["State"].tolist()[::-1]},
                title="Most stretched states (EVs per public charging station)",
            )
            fig.update_layout(coloraxis_showscale=False)
            fig.add_vline(x=target, line_dash="dash", line_color="#fbbf24",
                          annotation_text="target", annotation_font_color="#fbbf24")
            st.plotly_chart(style(fig, 480), use_container_width=True)

            st.dataframe(
                gap[["State", "EVs", "Total", "EVs per station", "Stations needed"]],
                use_container_width=True, hide_index=True,
            )
            st.download_button(
                "⬇️ Download gap results",
                gap[["State", "EVs", "Total", "EVs per station", "Stations needed"]]
                .to_csv(index=False).encode("utf-8"),
                "chargewise_gap_results.csv", "text/csv",
            )
    else:
        st.markdown("#### Screening without EV data")
        only_t3 = df[(df["Tier 1"] == 0) & (df["Tier 2"] == 0) & (df["Tier 3"] > 0)]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Lowest reported totals**")
            st.dataframe(
                df.sort_values("Total").head(10)[["State", "Total"]],
                use_container_width=True, hide_index=True,
            )
        with c2:
            st.markdown("**States with stations only in Tier 3 cities**")
            st.dataframe(
                only_t3[["State", "Tier 3"]].sort_values("Tier 3", ascending=False),
                use_container_width=True, hide_index=True,
            )
        st.info(
            "A full gap model also needs EV registrations, population, traffic, road access, "
            "charger capacity and distance to the nearest charger."
        )

# ---------------------------- PROJECTION ------------------------------------
with tab_proj:
    st.subheader("Scenario Explorer")
    st.caption("Illustrative scenario - not an official forecast.")

    p1, p2, p3 = st.columns(3)
    start = p1.number_input("Starting station count", min_value=1, value=TOTAL, step=100)
    rate = p2.slider("Assumed annual growth (%)", 0, 50, 15)
    years = p3.slider("Projection period (years)", 1, 15, 5)

    proj = pd.DataFrame({"Year": range(years + 1)})
    proj["Illustrative count"] = (start * (1 + rate / 100) ** proj["Year"]).round().astype(int)

    m1, m2 = st.columns(2)
    m1.metric("Stations after projection", f"{int(proj['Illustrative count'].iloc[-1]):,}")
    m2.metric("Added stations", f"{int(proj['Illustrative count'].iloc[-1] - start):,}")

    fig = px.area(proj, x="Year", y="Illustrative count", markers=True,
                  title="Hypothetical infrastructure growth scenario")
    fig.update_traces(line_color=PRIMARY, fillcolor="rgba(56,189,248,0.18)")
    st.plotly_chart(style(fig, 400), use_container_width=True)

    st.download_button(
        "⬇️ Download projection CSV",
        proj.to_csv(index=False).encode("utf-8"),
        "chargewise_projection.csv", "text/csv",
    )

# ---------------------------- DATA & METHOD ---------------------------------
with tab_data:
    st.subheader("Data and Methodology")
    st.dataframe(df.drop(columns=["Selected"]).sort_values("Total", ascending=False),
                 use_container_width=True, hide_index=True)
    st.download_button(
        "⬇️ Download state-wise dataset CSV",
        df.drop(columns=["Selected"]).to_csv(index=False).encode("utf-8"),
        "chargewise_official_state_counts_apr2025.csv", "text/csv",
    )

    st.markdown(
        """
**Primary source:** Bureau of Energy Efficiency data, published by the Ministry of Heavy
Industries through the Press Information Bureau.

**Reporting date:** 1 April 2025.

**Coverage:** Public charging stations in Tier 1, Tier 2 and Tier 3 cities.

**Limitations:** Aggregated state/UT counts, not individual station names, coordinates,
connector types or operating status. Not a live inventory.

**Gap score (when EV data is uploaded):** `EVs per station = EVs / stations`;
`Stations needed = max(0, ceil(EVs / target ratio - stations))`.
"""
    )
    st.markdown(
        "[Open the official PIB data release]"
        "(https://www.pib.gov.in/PressReleasePage.aspx?PRID=2118894&lang=2&reg=48)"
    )

st.divider()
st.caption("ChargeWise India | Public charging infrastructure analysis prototype")
