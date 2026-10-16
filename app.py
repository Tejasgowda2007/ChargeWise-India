import json
import math
import os

import pandas as pd
import plotly.express as px
import streamlit as st

# ----------------------------------------------------------------------------
# Design tokens
# Concept: highway wayfinding. Deep signal-board green, road-paper background,
# amber as the single "charging" accent. Condensed sign lettering for headlines,
# a plain humanist sans for data.
# ----------------------------------------------------------------------------
INK = "#1E3A34"      # deep green-grey, used for text only
PAPER = "#FBFCFA"    # page background, near white
MINT = "#E6F4EE"     # soft panel color (hero, hover states)
SLATE = "#5F7570"    # secondary text
RULE = "#DCE6E0"     # hairlines
AMBER = "#F6B73C"    # accent
TEAL = "#2FA58C"     # main data color
TIER_COLORS = {"Tier 1": "#4A90D9", "Tier 2": "#5BBFA3", "Tier 3": "#F6B73C"}

st.set_page_config(
    page_title="ChargeWise India",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

.stApp{background:%PAPER%;color:%INK%}
.stApp p,.stApp li,.stApp label,.stApp td,.stApp th,.stApp input,.stApp textarea,
[data-testid="stCaptionContainer"]{font-family:'IBM Plex Sans',sans-serif}
header[data-testid="stHeader"]{background:transparent}
[data-testid="stToolbar"],#MainMenu,footer{display:none !important}
.block-container{max-width:1180px;padding:1.4rem 2rem 3rem}

h1,h2,h3,h4{font-family:'Barlow Condensed',sans-serif !important;color:%INK% !important;
font-weight:700 !important;letter-spacing:0 !important}

/* top bar */
.topbar{display:flex;justify-content:space-between;align-items:center;padding:2px 0 16px}
.brand{display:flex;align-items:center;gap:10px;font-family:'Barlow Condensed',sans-serif;
font-weight:700;font-size:1.55rem;color:%INK%}
.mark{width:17px;height:22px;background:%AMBER%;
clip-path:polygon(55% 0,8% 56%,44% 56%,34% 100%,92% 40%,56% 40%)}
.meta{color:%SLATE%;font-size:.85rem;text-align:right}

/* hero */
.hero{background:%MINT%;border:1px solid %RULE%;border-radius:10px;padding:38px 42px 30px}
.hl{font-family:'Barlow Condensed',sans-serif;font-weight:700;
font-size:clamp(2.2rem,4.8vw,3.8rem);line-height:1.02;color:%INK%;max-width:780px}
.hsub{color:%SLATE%;font-size:1.02rem;margin-top:14px;max-width:660px;line-height:1.5}

/* segmented bars */
.segbar{display:flex;gap:2px;height:30px;margin-top:28px}
.segbar div{min-width:2px;border-radius:2px}
.seglegend{display:flex;flex-wrap:wrap;gap:6px 22px;margin-top:12px;font-size:.88rem}
.seglegend span i{display:inline-block;width:10px;height:10px;margin-right:7px;border-radius:1px}
.hero .seglegend{color:%SLATE%}

/* stat strip */
.stats{display:grid;grid-template-columns:repeat(4,1fr);border-bottom:1px solid %RULE%;margin-bottom:20px}
.stats div{padding:20px 24px 18px;border-left:1px solid %RULE%}
.stats div:first-child{border-left:0;padding-left:2px}
.stats b{display:block;font-family:'Barlow Condensed',sans-serif;font-size:2.5rem;
line-height:1;font-weight:700;color:%INK%}
.stats span{color:%SLATE%;font-size:.92rem}
@media (max-width:760px){.stats{grid-template-columns:repeat(2,1fr)}.hero{padding:26px 22px}}

/* section headings */
.sec-title{font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:1.9rem;
line-height:1.1;margin:28px 0 4px;color:%INK%}
.sec-sub{color:%SLATE%;margin:0 0 12px;max-width:72ch;line-height:1.5}

/* tabs */
.stTabs [data-baseweb="tab-list"]{gap:30px;border-bottom:1px solid %RULE%}
.stTabs [data-baseweb="tab"]{background:transparent;padding:10px 0;height:auto}
.stTabs [data-baseweb="tab"] p{font-family:'Barlow Condensed',sans-serif;font-size:1.25rem;
font-weight:600;color:%SLATE%}
.stTabs [aria-selected="true"] p{color:%INK%}
.stTabs [data-baseweb="tab-highlight"]{background:%AMBER%;height:3px}
.stTabs [data-baseweb="tab-border"]{background:transparent}

/* metrics, buttons */
[data-testid="stMetric"]{background:transparent;border-left:3px solid %AMBER%;padding:2px 14px}
[data-testid="stMetricValue"]{font-family:'Barlow Condensed',sans-serif;font-weight:700;color:%INK%}
.stDownloadButton button{border:1.5px solid %TEAL%;background:transparent;color:%INK%;
border-radius:8px;font-weight:600}
.stDownloadButton button:hover{background:%MINT%;color:%INK%;border-color:%TEAL%}
</style>
"""
for token, value in {"%PAPER%": PAPER, "%INK%": INK, "%SLATE%": SLATE,
                     "%RULE%": RULE, "%AMBER%": AMBER,
                     "%MINT%": MINT, "%TEAL%": TEAL}.items():
    CSS = CSS.replace(token, value)
st.markdown(CSS, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# Data
# Source: PIB / Ministry of Heavy Industries / BEE (reporting date 1 April 2025)
# State totals only, not individual station coordinates.
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

GEOJSON_FILE = "india_states.geojson"   # optional: place next to app.py
GEOJSON_KEY = "properties.ST_NM"        # change to match your file's state-name field


@st.cache_data
def load_data() -> pd.DataFrame:
    d = pd.DataFrame(DATA, columns=["State", "Tier 1", "Tier 2", "Tier 3", "Total"])
    d["Share of India (%)"] = (d["Total"] / d["Total"].sum() * 100).round(2)
    d["Rank"] = d["Total"].rank(ascending=False, method="min").astype(int)
    return d


df = load_data()
TOTAL = int(df["Total"].sum())
TIERS = ["Tier 1", "Tier 2", "Tier 3"]
tier_totals = {t: int(df[t].sum()) for t in TIERS}

# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------


def seg_bar(segments, legend):
    """Horizontal segmented bar. segments: (label, value, color); legend: (text, color)."""
    bars = "".join(
        f'<div title="{label}: {value:,}" style="flex:{value};background:{color}"></div>'
        for label, value, color in segments
    )
    keys = "".join(f'<span><i style="background:{c}"></i>{t}</span>' for t, c in legend)
    return f'<div class="segbar">{bars}</div><div class="seglegend">{keys}</div>'


def section(title, sub=""):
    sub_html = f'<p class="sec-sub">{sub}</p>' if sub else ""
    st.markdown(f'<div class="sec-title">{title}</div>{sub_html}', unsafe_allow_html=True)


def style(fig, height=420):
    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        margin=dict(l=0, r=10, t=10, b=10),
        font=dict(family="IBM Plex Sans, sans-serif", color=INK, size=13),
        legend=dict(orientation="h", y=1.08, x=0, title=None),
        bargap=0.35,
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E6EDE8", zeroline=False, title=None)
    fig.update_yaxes(showgrid=False, title=None)
    return fig


# ----------------------------------------------------------------------------
# Header, hero, stat strip
# ----------------------------------------------------------------------------
st.markdown(
    '<div class="topbar"><div class="brand"><span class="mark"></span>ChargeWise India</div>'
    '<div class="meta">Public charging stations by state<br>'
    "Source: Bureau of Energy Efficiency, via PIB. Reported 1 April 2025</div></div>",
    unsafe_allow_html=True,
)

by_total = df.sort_values("Total", ascending=False).reset_index(drop=True)
top3 = by_total.head(3)
top3_sum = int(top3["Total"].sum())
top3_share = top3_sum / TOTAL * 100
small_states = int((df["Total"] < 100).sum())
names = f"{top3.loc[0, 'State']}, {top3.loc[1, 'State']} and {top3.loc[2, 'State']}"

hero_colors = ["#2FA58C", "#5BBFA3", "#9AD8C6"]
REST = "#CBDDD4"
segments = []
for i, row in by_total.iterrows():
    segments.append((row["State"], int(row["Total"]), hero_colors[i] if i < 3 else REST))
legend = [(f"{top3.loc[i, 'State']} {top3.loc[i, 'Total'] / TOTAL * 100:.0f}%", hero_colors[i]) for i in range(3)]
legend.append((f"All other states and UTs {100 - top3_share:.0f}%", REST))

st.markdown(
    f'<div class="hero"><div class="hl">{names} hold {top3_share:.0f}% of India\'s public chargers.</div>'
    f'<div class="hsub">{top3_sum:,} of {TOTAL:,} reported stations. '
    f"{small_states} of {len(df)} states and UTs report fewer than 100.</div>"
    f"{seg_bar(segments, legend)}</div>",
    unsafe_allow_html=True,
)

tier3_share = tier_totals["Tier 3"] / TOTAL * 100
st.markdown(
    '<div class="stats">'
    f"<div><b>{TOTAL:,}</b><span>public charging stations</span></div>"
    f"<div><b>{len(df)}</b><span>states and union territories</span></div>"
    f'<div><b>{by_total.loc[0, "Total"]:,}</b><span>in {by_total.loc[0, "State"]}, the highest</span></div>'
    f"<div><b>{tier3_share:.0f}%</b><span>of stations are in Tier 3 cities</span></div>"
    "</div>",
    unsafe_allow_html=True,
)

f1, _ = st.columns([2, 3])
tier_pick = f1.multiselect("City tiers shown in the views below", TIERS, default=TIERS)
if not tier_pick:
    st.warning("Choose at least one city tier to see the charts.")
    st.stop()

df["Selected"] = df[tier_pick].sum(axis=1)
SEL_TOTAL = int(df["Selected"].sum())
ranked = df.sort_values("Selected", ascending=False).reset_index(drop=True)

tab_over, tab_state, tab_gap, tab_proj, tab_data = st.tabs(
    ["Overview", "State comparison", "Gap finder", "Scenarios", "Data and method"]
)

# ---------------------------- OVERVIEW --------------------------------------
with tab_over:
    lead, lead_n = ranked.loc[0, "State"], int(ranked.loc[0, "Selected"])
    section(
        f"{lead} leads with {lead_n:,} stations, {lead_n / SEL_TOTAL * 100:.0f}% of the total",
        "The 15 states and UTs with the most public charging stations, split by city tier.",
    )
    top15 = ranked.head(15)
    order = top15["State"].tolist()
    long = df[df["State"].isin(order)].melt(
        id_vars="State", value_vars=tier_pick, var_name="Tier", value_name="Stations"
    )
    fig = px.bar(
        long, x="Stations", y="State", color="Tier", orientation="h",
        color_discrete_map=TIER_COLORS, category_orders={"State": order[::-1], "Tier": TIERS},
    )
    for _, r in top15.iterrows():
        fig.add_annotation(x=r["Selected"], y=r["State"], text=f"{int(r['Selected']):,}",
                           showarrow=False, xanchor="left", xshift=6, font=dict(size=12, color=SLATE))
    fig.update_xaxes(range=[0, top15["Selected"].max() * 1.13])
    st.plotly_chart(style(fig, 520), use_container_width=True)

    section(
        "How stations split across city tiers",
        "Tier 1 cities are the largest metros; Tier 3 covers smaller cities and towns.",
    )
    tier_segments = [(t, tier_totals[t], TIER_COLORS[t]) for t in tier_pick]
    tier_legend = [
        (f"{t}: {tier_totals[t]:,} ({tier_totals[t] / SEL_TOTAL * 100:.0f}%)", TIER_COLORS[t])
        for t in tier_pick
    ]
    st.markdown(seg_bar(tier_segments, tier_legend), unsafe_allow_html=True)

    if os.path.exists(GEOJSON_FILE):
        section("Stations by state on the map")
        with open(GEOJSON_FILE, encoding="utf-8") as f:
            geo = json.load(f)
        fig3 = px.choropleth(
            df, geojson=geo, locations="State", featureidkey=GEOJSON_KEY,
            color="Selected", color_continuous_scale=["#E6F4EE", TEAL],
        )
        fig3.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(style(fig3, 560), use_container_width=True)
    else:
        st.caption(
            f"To add a state map here, place an India state boundary file named "
            f"{GEOJSON_FILE} next to app.py."
        )

# ---------------------------- STATE COMPARISON ------------------------------
with tab_state:
    section("Compare states side by side", "Pick the states to compare and how to sort them.")
    c1, c2 = st.columns([3, 1])
    selected = c1.multiselect(
        "States",
        df["State"].tolist(),
        default=["Karnataka", "Maharashtra", "Uttar Pradesh", "Tamil Nadu", "Kerala"],
    )
    sort_by = c2.selectbox(
        "Sort by", ["Selected"] + tier_pick,
        format_func=lambda x: "Total in chosen tiers" if x == "Selected" else x,
    )

    if selected:
        f = df[df["State"].isin(selected)].sort_values(sort_by, ascending=False)
        long = f.melt(id_vars="State", value_vars=tier_pick, var_name="Tier", value_name="Stations")
        fig = px.bar(
            long, x="State", y="Stations", color="Tier", barmode="group",
            color_discrete_map=TIER_COLORS,
            category_orders={"State": f["State"].tolist(), "Tier": TIERS},
        )
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=True)
        st.plotly_chart(style(fig, 420), use_container_width=True)

        st.dataframe(
            f[["Rank", "State"] + tier_pick + ["Selected", "Share of India (%)"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Selected": st.column_config.ProgressColumn(
                    "Total in chosen tiers", min_value=0,
                    max_value=int(df["Selected"].max()), format="%d",
                ),
                "Share of India (%)": st.column_config.NumberColumn(format="%.2f%%"),
            },
        )
    else:
        st.info("Choose at least one state to compare.")

# ---------------------------- GAP FINDER ------------------------------------
with tab_gap:
    section(
        "Find where chargers fall behind EV demand",
        "Station counts alone do not show a gap. Add EV registrations for each state to see "
        "EVs per station and how many more stations a target ratio would need.",
    )
    template = pd.DataFrame({"State": df["State"], "EVs": ""})
    cA, cB = st.columns([1, 2])
    cA.download_button(
        "Download CSV template",
        template.to_csv(index=False).encode("utf-8"),
        "ev_registrations_template.csv",
        "text/csv",
    )
    up = cB.file_uploader("Upload your filled CSV (columns: State, EVs)", type="csv")

    if up is not None:
        ev = pd.read_csv(up)
        ev.columns = [c.strip() for c in ev.columns]
        if not {"State", "EVs"}.issubset(ev.columns):
            st.error("The CSV needs two columns named State and EVs. Download the template to start.")
        else:
            ev["EVs"] = pd.to_numeric(ev["EVs"], errors="coerce")
            ev = ev.dropna(subset=["EVs"])
            ev["key"] = ev["State"].str.strip().str.lower()
            base = df.assign(key=df["State"].str.lower())
            gap = base.merge(ev[["key", "EVs"]], on="key", how="inner")

            unmatched = sorted(set(ev["State"]) - set(gap["State"]))
            if unmatched:
                st.warning("These names did not match the dataset: " + ", ".join(unmatched))

            if gap.empty:
                st.error("No states matched. Check that state names match the template.")
            else:
                target = st.slider(
                    "Target EVs per public charging station", 5, 100, 20,
                    help="Your planning assumption. Change it to test scenarios.",
                )
                gap["EVs per station"] = (gap["EVs"] / gap["Total"].where(gap["Total"] > 0)).round(1)
                gap["Stations needed"] = gap.apply(
                    lambda r: max(0, math.ceil(r["EVs"] / target - r["Total"])), axis=1
                )
                gap = gap.sort_values("EVs per station", ascending=False)

                g1, g2, g3 = st.columns(3)
                g1.metric("States analysed", len(gap))
                g2.metric("Most stretched", gap.iloc[0]["State"],
                          f"{gap.iloc[0]['EVs per station']} EVs per station", delta_color="off")
                g3.metric("Extra stations to reach target", f"{int(gap['Stations needed'].sum()):,}")

                section("States with the most EVs per charging station")
                top = gap.head(15)
                fig = px.bar(
                    top, x="EVs per station", y="State", orientation="h",
                    color_discrete_sequence=[TEAL],
                    category_orders={"State": top["State"].tolist()[::-1]},
                )
                fig.add_vline(x=target, line_dash="dash", line_color=AMBER, line_width=2,
                              annotation_text="target", annotation_font_color=AMBER)
                st.plotly_chart(style(fig, 480), use_container_width=True)

                cols = ["State", "EVs", "Total", "EVs per station", "Stations needed"]
                st.dataframe(gap[cols], use_container_width=True, hide_index=True)
                st.download_button(
                    "Download gap results",
                    gap[cols].to_csv(index=False).encode("utf-8"),
                    "chargewise_gap_results.csv", "text/csv",
                )
    else:
        section("What the station data shows on its own")
        only_t3 = df[(df["Tier 1"] == 0) & (df["Tier 2"] == 0) & (df["Tier 3"] > 0)]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Lowest reported totals**")
            st.dataframe(df.sort_values("Total").head(10)[["State", "Total"]],
                         use_container_width=True, hide_index=True)
        with c2:
            st.markdown("**States with stations only in Tier 3 cities**")
            st.dataframe(only_t3[["State", "Tier 3"]].sort_values("Tier 3", ascending=False),
                         use_container_width=True, hide_index=True)
        st.caption(
            "A full gap model also needs EV registrations, population, traffic, road access, "
            "charger capacity and distance to the nearest charger."
        )

# ---------------------------- SCENARIOS -------------------------------------
with tab_proj:
    section("Test a growth scenario", "An illustration based on your assumptions. It is not an official forecast.")
    p1, p2, p3 = st.columns(3)
    start = p1.number_input("Starting station count", min_value=1, value=TOTAL, step=100)
    rate = p2.slider("Annual growth (%)", 0, 50, 15)
    years = p3.slider("Years to project", 1, 15, 5)

    proj = pd.DataFrame({"Year": range(years + 1)})
    proj["Illustrative count"] = (start * (1 + rate / 100) ** proj["Year"]).round().astype(int)
    end_count = int(proj["Illustrative count"].iloc[-1])

    m1, m2 = st.columns(2)
    m1.metric(f"Stations after {years} years", f"{end_count:,}")
    m2.metric("Stations added", f"{end_count - int(start):,}")

    fig = px.area(proj, x="Year", y="Illustrative count")
    fig.update_traces(line_color=TEAL, fillcolor="rgba(47,165,140,0.18)")
    st.plotly_chart(style(fig, 380), use_container_width=True)

    st.download_button(
        "Download projection CSV",
        proj.to_csv(index=False).encode("utf-8"),
        "chargewise_projection.csv", "text/csv",
    )

# ---------------------------- DATA AND METHOD -------------------------------
with tab_data:
    section("Data and method")
    full = df.drop(columns=["Selected"]).sort_values("Total", ascending=False)
    st.dataframe(full, use_container_width=True, hide_index=True)
    st.download_button(
        "Download state-wise dataset CSV",
        full.to_csv(index=False).encode("utf-8"),
        "chargewise_official_state_counts_apr2025.csv", "text/csv",
    )
    st.markdown(
        """
**Source.** Bureau of Energy Efficiency data, published by the Ministry of Heavy Industries
through the Press Information Bureau.

**Reporting date.** 1 April 2025.

**Coverage.** Public charging stations in Tier 1, Tier 2 and Tier 3 cities.

**Limits.** These are aggregated state and UT counts. They do not include station names,
coordinates, connector types or operating status, and they are not a live inventory.

**Gap calculation (when EV data is uploaded).** EVs per station = EVs divided by stations.
Stations needed = EVs divided by the target ratio, minus existing stations, never below zero.
"""
    )
    st.markdown(
        "[Open the official PIB data release]"
        "(https://www.pib.gov.in/PressReleasePage.aspx?PRID=2118894&lang=2&reg=48)"
    )

st.markdown(
    f'<p class="meta" style="text-align:left;margin-top:36px;border-top:1px solid {RULE};padding-top:12px">'
    "ChargeWise India. Public charging infrastructure analysis prototype.</p>",
    unsafe_allow_html=True,
)
