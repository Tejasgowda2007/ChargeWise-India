import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="ChargeWise India",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
.stApp {background:#0b1120;color:#f1f5f9}
[data-testid="stMetric"] {
    background:#172238;padding:18px;border-radius:12px;
    border:1px solid #263852
}
h1,h2,h3 {color:#38bdf8 !important}
section[data-testid="stSidebar"] {background:#151d2e}
</style>
""", unsafe_allow_html=True)

# Official state-wise public charging-station counts
# Source: PIB / Ministry of Heavy Industries / BEE
# Reporting date: 1 April 2025
# These are state totals, not individual station coordinates.

data = [
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

df = pd.DataFrame(
    data,
    columns=[
        "State", "Tier 1", "Tier 2", "Tier 3", "Total"
    ]
)

st.title("⚡ CHARGEWISE INDIA")
st.subheader("EV Infrastructure Mapping & Charging Gap Analysis")
st.caption("Official state-level data | Reported 1 April 2025")

st.info(
    "Source: Bureau of Energy Efficiency, Ministry of Power, "
    "published by the Ministry of Heavy Industries through PIB. "
    "These counts describe public charging stations in Tier 1, 2 and 3 "
    "cities as reported on 1 April 2025. They are not live counts."
)

with st.sidebar:
    st.header("Dashboard")
    page = st.radio(
        "Choose a view",
        [
            "Overview",
            "State Analysis",
            "Infrastructure Gaps",
            "Future Projection",
            "Data Table & Sources"
        ]
    )

    st.divider()
    st.write("ChargeWise India")
    st.caption("EV infrastructure planning prototype")

# Overview metrics
a, b, c, d = st.columns(4)
a.metric("Public charging stations", f"{df['Total'].sum():,}")
b.metric("States and UTs listed", len(df))
c.metric("Highest total", "Karnataka")
d.metric("Karnataka stations", f"{5880:,}")

if page == "Overview":
    st.header("National Infrastructure Overview")

    left, right = st.columns([1.4, 1])

    with left:
        fig = px.bar(
            df.sort_values("Total").tail(12),
            x="Total",
            y="State",
            orientation="h",
            color="Total",
            color_continuous_scale="Blues",
            title="12 largest reported state/UT totals"
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#0b1120",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        tier_totals = pd.DataFrame({
            "City category": ["Tier 1", "Tier 2", "Tier 3"],
            "Stations": [9702, 4625, 12040]
        })
        fig2 = px.pie(
            tier_totals,
            names="City category",
            values="Stations",
            hole=0.48,
            title="Reported stations by city tier"
        )
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120"
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("India Map")
    st.write(
        "The map provides geographic context. State totals are not "
        "individual station coordinates, so station markers are not shown."
    )
    m = folium.Map(
        location=[22.5, 79.0],
        zoom_start=4,
        tiles="CartoDB positron"
    )
    st_folium(m, height=400, use_container_width=True)

elif page == "State Analysis":
    st.header("State-wise Charging Infrastructure")

    selected = st.multiselect(
        "Select states",
        df["State"].tolist(),
        default=["Karnataka", "Maharashtra", "Uttar Pradesh",
                 "Tamil Nadu", "Kerala"]
    )

    filtered = df[df["State"].isin(selected)]

    fig = px.bar(
        filtered.sort_values("Total"),
        x="Total",
        y="State",
        orientation="h",
        color="Total",
        color_continuous_scale="Teal",
        title="Reported public charging stations by state/UT"
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1120",
        plot_bgcolor="#0b1120"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(filtered, use_container_width=True, hide_index=True)

elif page == "Infrastructure Gaps":
    st.header("Infrastructure Gap Screening")

    st.warning(
        "Low station counts alone do not prove an infrastructure gap. "
        "A proper gap model also needs EV registrations, population, "
        "traffic, road access, charger capacity, and geographic coverage."
    )

    st.subheader("Lowest reported totals")
    st.dataframe(
        df.sort_values("Total").head(10),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Planning considerations")
    st.markdown("""
    - Compare charger availability with EV registrations.
    - Measure distance to the nearest public charging facility.
    - Consider highways, traffic flows and travel corridors.
    - Account for fast/slow charging capacity and connector compatibility.
    - Validate candidate locations through field or official data.
    """)

elif page == "Future Projection":
    st.header("Future Demand Scenario Explorer")

    st.write(
        "This is an illustrative scenario, not an official forecast."
    )

    start = st.number_input(
        "Starting station count",
        min_value=1,
        value=26367,
        step=100
    )
    rate = st.slider("Assumed annual growth (%)", 0, 50, 15)
    years = st.slider("Projection period (years)", 1, 15, 5)

    proj = pd.DataFrame({"Year": range(years + 1)})
    proj["Illustrative count"] = (
        start * (1 + rate / 100) ** proj["Year"]
    ).round().astype(int)

    fig = px.line(
        proj,
        x="Year",
        y="Illustrative count",
        markers=True,
        title="Hypothetical infrastructure growth scenario"
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1120",
        plot_bgcolor="#0b1120"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(proj, use_container_width=True, hide_index=True)

    st.download_button(
        "Download projection CSV",
        proj.to_csv(index=False).encode("utf-8"),
        "chargewise_projection.csv",
        "text/csv"
    )

    st.caption(
        "The starting value is the BEE-reported 26,367 total from "
        "1 April 2025. Future values are mathematical scenarios based "
        "on your selected growth assumption."
    )

elif page == "Data Table & Sources":
    st.header("Data and Methodology")

    st.dataframe(
        df.sort_values("Total", ascending=False),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download state-wise dataset CSV",
        df.to_csv(index=False).encode("utf-8"),
        "chargewise_official_state_counts_apr2025.csv",
        "text/csv"
    )

    st.markdown("""
    **Primary source:** Bureau of Energy Efficiency data, published by
    the Ministry of Heavy Industries through the Press Information Bureau.

    **Reporting date:** 1 April 2025.

    **Coverage:** Public charging stations reported across Tier 1, Tier 2
    and Tier 3 cities.

    **Limitation:** This is aggregated state/UT data, not a list of
    individual station names, coordinates, connector types or operating
    status. It should not be interpreted as a live 2026 inventory.

    **Gap analysis limitation:** State totals alone cannot identify
    underserved districts or establish station adequacy.
    """)

    st.markdown(
        "[Open the official PIB data release]"
        "(https://www.pib.gov.in/PressReleasePage.aspx?PRID=2118894&lang=2&reg=48)"
    )

st.divider()
st.caption(
    "ChargeWise India | Public charging infrastructure analysis prototype"
)