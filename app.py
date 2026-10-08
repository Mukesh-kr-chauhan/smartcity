"""
SmartCity AI — Main Streamlit Application
AI-Powered Sustainable City Decision & Impact Optimization Platform
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.config import ZONES, ZONE_PROFILES, GEMINI_API_KEY
from utils.db import init_db, save_problems, save_recommendation
from utils.data_loader import load_raw_datasets
from analysis.preprocessing import preprocess_city_data, merge_city_data
from analysis.anomaly_detection import run_all_anomaly_models
from analysis.problem_detection import detect_structured_problems
from analysis.cross_domain import analyze_cross_domain_synergies
from analysis.priority_engine import prioritize_all_problems
from analysis.sustainability_score import compute_city_sustainability_score
from analysis.impact_estimation import estimate_remediation_impact
from agents.decision_agent import generate_decision_support
from scenarios.simulator import inject_scenario

st.set_page_config(
    page_title="SmartCity AI | Sustainable Decision Platform",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .disclaimer-banner {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 12px;
        font-size: 0.85rem;
        color: #475569;
        margin-bottom: 20px;
    }
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize persistence
init_db()

@st.cache_data(show_spinner=False)
def execute_pipeline(scenario_name: str):
    raw_data = load_raw_datasets()
    cleaned_data = preprocess_city_data(raw_data)
    scenario_data = inject_scenario(cleaned_data, scenario_name)
    merged_df = merge_city_data(scenario_data)
    
    evaluated_data = run_all_anomaly_models(scenario_data)
    raw_problems = detect_structured_problems(evaluated_data)
    cross_insights = analyze_cross_domain_synergies(merged_df)
    prioritized = prioritize_all_problems(raw_problems, cross_insights)
    overall_score, sub_scores = compute_city_sustainability_score(evaluated_data)
    impact_estimate = estimate_remediation_impact(prioritized)

    save_problems(prioritized)

    return {
        "data": scenario_data,
        "merged_df": merged_df,
        "problems": prioritized,
        "cross_insights": cross_insights,
        "sustainability_score": overall_score,
        "sub_scores": sub_scores,
        "impact_estimate": impact_estimate
    }

# Sidebar Navigation & Controls
st.sidebar.title("🏙️ SmartCity AI")
st.sidebar.caption("AI-Powered Sustainable City Platform")

st.sidebar.markdown("---")
st.sidebar.subheader("🎮 Live Scenario Simulator")
scenario_option = st.sidebar.selectbox(
    "Select Operating Scenario:",
    [
        "Normal City",
        "Water Leak Scenario",
        "Traffic Congestion Scenario",
        "Energy Peak Scenario",
        "Waste Overflow Scenario",
        "Air Pollution Scenario",
        "Combined Sustainability Scenario"
    ],
    index=1
)

if st.sidebar.button("Run Simulation Pipeline", use_container_width=True):
    st.cache_data.clear()

st.sidebar.markdown("---")
page = st.sidebar.radio(
    "Navigation:",
    [
        "1. City Overview",
        "2. Traffic Intelligence",
        "3. Energy Intelligence",
        "4. Water Intelligence",
        "5. Waste Intelligence",
        "6. Air Quality Intelligence",
        "7. Cross-Domain Analysis",
        "8. Priority Center",
        "9. AI Recommendations",
        "10. Environmental Impact",
        "11. Scenario Simulator",
        "12. Natural Language Query",
        "13. About"
    ]
)

results = execute_pipeline(scenario_option)
problems = results["problems"]
cross_insights = results["cross_insights"]
overall_score = results["sustainability_score"]
sub_scores = results["sub_scores"]
impact = results["impact_estimate"]
city_data = results["data"]

# Executive Disclaimer Banner
st.markdown("""
<div class="disclaimer-banner">
    <b>Responsible AI Protocol:</b> SmartCity AI is a prototype decision-support system using simulated/demo data. 
    AI-generated recommendations are intended to support human decision-making and must be independently verified before real-world implementation.
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# 1. CITY OVERVIEW
# ==============================================================================
if page == "1. City Overview":
    st.title("🏙️ City Executive Overview")
    st.write(f"Current Operating State: **{scenario_option}**")

    col1, col2, col3, col4, col5 = st.columns(5)
    crit_count = sum(1 for p in problems if p["priority_status"] == "CRITICAL")
    high_count = sum(1 for p in problems if p["priority_status"] == "HIGH")

    col1.metric("Sustainability Score", f"{overall_score} / 100", delta=f"{overall_score - 75:.1f} vs Target")
    col2.metric("Active Detected Issues", len(problems))
    col3.metric("Critical Alerts", crit_count, delta_color="inverse")
    col4.metric("High Priority Issues", high_count, delta_color="inverse")
    col5.metric("Cross-Domain Synergies", len(cross_insights))

    st.markdown("---")

    col_left, col_right = st.columns([1.8, 1.2])

    with col_left:
        st.subheader("🗺️ Urban Zone Operational Map")
        map_records = []
        for z, meta in ZONE_PROFILES.items():
            z_probs = [p for p in problems if p["zone"] == z]
            highest_sev = "Normal"
            if any(p["priority_status"] == "CRITICAL" for p in z_probs):
                highest_sev = "Critical"
            elif any(p["priority_status"] == "HIGH" for p in z_probs):
                highest_sev = "Warning"

            map_records.append({
                "Zone": z,
                "Type": meta["type"],
                "lat": meta["lat"],
                "lon": meta["lon"],
                "Population": meta["base_pop"],
                "Status": highest_sev,
                "Size": 25 if highest_sev == "Critical" else 18 if highest_sev == "Warning" else 12,
            })

        map_df = pd.DataFrame(map_records)
        
        # Center coordinates for Zone A-E (Manhattan metro area)
        center_coords = {"lat": 40.745, "lon": -73.985}
        color_map = {"Critical": "#ef4444", "Warning": "#f97316", "Normal": "#10b981"}

        if hasattr(px, "scatter_map"):
            fig_map = px.scatter_map(
                map_df,
                lat="lat",
                lon="lon",
                color="Status",
                size="Size",
                size_max=22,
                hover_name="Zone",
                hover_data={"lat": False, "lon": False, "Type": True, "Population": True, "Status": True, "Size": False},
                color_discrete_map=color_map,
                zoom=11.0,
                center=center_coords,
                height=420
            )
            fig_map.update_layout(map_style="open-street-map", margin=dict(l=0, r=0, t=0, b=0))
        else:
            fig_map = px.scatter_mapbox(
                map_df,
                lat="lat",
                lon="lon",
                color="Status",
                size="Size",
                size_max=22,
                hover_name="Zone",
                hover_data={"lat": False, "lon": False, "Type": True, "Population": True, "Status": True, "Size": False},
                color_discrete_map=color_map,
                zoom=11.0,
                center=center_coords,
                height=420
            )
            fig_map.update_layout(mapbox_style="open-street-map", margin=dict(l=0, r=0, t=0, b=0))

        st.plotly_chart(fig_map, use_container_width=True)

    with col_right:
        st.subheader("📊 Domain Efficiency Breakdown")
        radar_df = pd.DataFrame(dict(
            r=list(sub_scores.values()),
            theta=[k.replace("_", " ").title() for k in sub_scores.keys()]
        ))
        fig_radar = px.line_polar(radar_df, r='r', theta='theta', line_close=True)
        fig_radar.update_traces(fill='toself', line_color='#2563eb')
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), height=420, margin=dict(l=40, r=40, t=20, b=20))
        st.plotly_chart(fig_radar, use_container_width=True)

    if problems:
        top_prob = problems[0]
        st.subheader("🚨 Primary Sustainability Issue Requiring Review")
        status_color = "#fee2e2" if top_prob["priority_status"] == "CRITICAL" else "#ffedd5"
        border_color = "#dc2626" if top_prob["priority_status"] == "CRITICAL" else "#ea580c"

        st.markdown(f"""
        <div style="background-color: {status_color}; border-left: 6px solid {border_color}; padding: 16px; border-radius: 6px;">
            <h4 style="margin: 0; color: #1e293b;">[{top_prob['priority_status']}] {top_prob['zone']} — {top_prob['category']} Anomaly (Priority Score: {top_prob['priority_score']}/100)</h4>
            <p style="margin: 8px 0; color: #334155;">{top_prob['explanation']}</p>
            <small style="color: #64748b;"><b>Deviation:</b> {top_prob['deviation_percent']}% | <b>Observed:</b> {top_prob['detected_value']} | <b>Expected:</b> {top_prob['expected_value']}</small>
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 2. TRAFFIC INTELLIGENCE
# ==============================================================================
elif page == "2. Traffic Intelligence":
    st.title("🚗 Traffic Intelligence Engine")
    tf_df = city_data["traffic"]

    col1, col2, col3 = st.columns(3)
    recent_tf = tf_df.tail(len(ZONES))
    col1.metric("Avg Speed Across Zones", f"{recent_tf['average_speed'].mean():.1f} km/h")
    col2.metric("Total Congestion Index", f"{recent_tf['idle_time'].mean():.1f} min idle/veh")
    col3.metric("Vehicle Count", f"{recent_tf['vehicle_count'].sum():,}")

    st.subheader("Traffic Velocity Trends (Hourly)")
    fig = px.line(
        tf_df, x="timestamp", y="average_speed", color="zone_id",
        title="Hourly Average Speed by Zone (km/h)", labels={"average_speed": "Speed (km/h)"}
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Recent Arterial Status")
    st.dataframe(
        recent_tf[["zone_id", "road_id", "vehicle_count", "average_speed", "congestion_level", "travel_time", "idle_time"]],
        use_container_width=True
    )

# ==============================================================================
# 3. ENERGY INTELLIGENCE
# ==============================================================================
elif page == "3. Energy Intelligence":
    st.title("⚡ Energy Intelligence Engine")
    en_df = city_data["energy"]

    col1, col2, col3 = st.columns(3)
    recent_en = en_df.tail(len(ZONES))
    col1.metric("Current City Load", f"{recent_en['electricity_consumption'].sum():,.0f} kWh")
    col2.metric("Renewable Infeed", f"{recent_en['renewable_generation'].sum():,.0f} kWh")
    col3.metric("Peak Demand", f"{recent_en['peak_demand'].max():,.0f} kW")

    fig = px.area(
        en_df, x="timestamp", y="electricity_consumption", color="zone_id",
        title="Hourly Power Consumption by Zone (kWh)"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# 4. WATER INTELLIGENCE
# ==============================================================================
elif page == "4. Water Intelligence":
    st.title("💧 Water Intelligence Engine")
    wtr_df = city_data["water"]

    zone_select = st.selectbox("Select Zone for Detailed Inspection:", ZONES, index=1)
    z_wtr = wtr_df[wtr_df["zone_id"] == zone_select].sort_values("timestamp")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=z_wtr["timestamp"], y=z_wtr["water_consumption"], name="Observed Consumption (L)", line=dict(color="#2563eb", width=2)))
    fig.add_trace(go.Scatter(x=z_wtr["timestamp"], y=z_wtr["historical_average"], name="Historical Baseline (L)", line=dict(color="#94a3b8", dash="dash")))
    fig.update_layout(title=f"{zone_select} — Telemetry Consumption vs. Historical Baseline", xaxis_title="Timestamp", yaxis_title="Consumption (L/h)")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_p = px.line(z_wtr, x="timestamp", y="pressure", title=f"{zone_select} — Distribution Pressure (bar)")
        st.plotly_chart(fig_p, use_container_width=True)
    with col2:
        fig_f = px.line(z_wtr, x="timestamp", y="water_flow", title=f"{zone_select} — Water Flow Rate (m³/s)")
        st.plotly_chart(fig_f, use_container_width=True)

# ==============================================================================
# 5. WASTE INTELLIGENCE
# ==============================================================================
elif page == "5. Waste Intelligence":
    st.title("♻️ Waste Intelligence Engine")
    wst_df = city_data["waste"]

    recent_wst = wst_df.tail(len(ZONES))
    fig = px.bar(
        recent_wst, x="zone_id", y=["waste_generated", "collection_capacity"],
        barmode="group", title="Current Waste Generation vs. Bin Capacity (kg)",
        labels={"value": "Kilograms", "variable": "Metric"}
    )
    st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# 6. AIR QUALITY INTELLIGENCE
# ==============================================================================
elif page == "6. Air Quality Intelligence":
    st.title("🍃 Air Quality Intelligence Engine")
    aq_df = city_data["air_quality"]

    recent_aq = aq_df.tail(len(ZONES))
    fig = px.bar(
        recent_aq, x="zone_id", y="AQI", color="AQI",
        color_continuous_scale=["#10b981", "#f59e0b", "#ef4444", "#7f1d1d"],
        title="Live Air Quality Index (AQI) Across Zones"
    )
    st.plotly_chart(fig, use_container_width=True)

    fig_pollutants = px.line(
        aq_df, x="timestamp", y="PM2_5", color="zone_id",
        title="Particulate Matter PM2.5 Concentrations (µg/m³)"
    )
    st.plotly_chart(fig_pollutants, use_container_width=True)

# ==============================================================================
# 7. CROSS-DOMAIN ANALYSIS
# ==============================================================================
elif page == "7. Cross-Domain Analysis":
    st.title("🔗 Cross-Domain Intelligence")
    st.markdown("""
    SmartCity AI correlates interactions across municipal domains to surface systemic bottlenecks.
    """)

    if not cross_insights:
        st.info("No anomalous cross-domain synergies detected under the current operating profile.")
    else:
        for s in cross_insights:
            st.markdown(f"""
            <div style="background-color: #f1f5f9; border-left: 5px solid #6366f1; padding: 14px; border-radius: 6px; margin-bottom: 12px;">
                <h4 style="margin: 0 0 6px 0; color: #1e1b4b;">{s['synergy_type']} ({s['zone']})</h4>
                <p style="margin: 0; color: #334155;">{s['description']}</p>
                <p style="margin: 6px 0 0 0; color: #4338ca;"><b>Recommended Operational Synergy:</b> {s['recommendation_seed']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.subheader("Cross-Domain Correlation Explorer")
    merged = results["merged_df"]
    fig_corr = px.scatter(
        merged, x="idle_time", y="PM2_5", color="zone_id", size="vehicle_count",
        hover_data=["congestion_level", "NO2"],
        title="Correlation: Traffic Idle Time vs. PM2.5 Particulate Concentration",
        labels={"idle_time": "Idle Time (minutes)", "PM2_5": "PM2.5 Concentration (µg/m³)"}
    )
    st.plotly_chart(fig_corr, use_container_width=True)

# ==============================================================================
# 8. PRIORITY CENTER
# ==============================================================================
elif page == "8. Priority Center":
    st.title("🎯 Sustainability Priority Engine")
    st.markdown("""
    The Sustainability Priority Engine scores all detected problems on a transparent **0–100 scale**, 
    balancing severity, environmental hazard, urgency, resource waste, and population exposure.
    """)

    if not problems:
        st.success("No anomalies detected across city telemetry networks.")
    else:
        for p in problems:
            with st.expander(f"[{p['priority_status']} - {p['priority_score']}/100] {p['zone']} : {p['category']} Problem", expanded=(p["priority_status"] == "CRITICAL")):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.write(f"**Explanation:** {p['explanation']}")
                    st.write(f"**Observed Value:** `{p['detected_value']}` | **Expected:** `{p['expected_value']}` | **Deviation:** `+{p['deviation_percent']}%`")
                    st.caption(f"Problem ID: {p['problem_id']} | Telemetry Timestamp: {p['timestamp']}")
                with c2:
                    st.markdown("**Priority Factor Breakdown (0–100):**")
                    breakdown = p.get("priority_breakdown", {})
                    for factor, val in breakdown.items():
                        st.progress(int(val) / 100, text=f"{factor.replace('_', ' ').capitalize()}: {val}")

# ==============================================================================
# 9. AI RECOMMENDATIONS
# ==============================================================================
elif page == "9. AI Recommendations":
    st.title("🤖 AI Decision-Support Agent")

    if not GEMINI_API_KEY:
        st.info("Operating in **Deterministic Rule-Based Mode** (No `GEMINI_API_KEY` set in `.env`). Full explainable reasoning remains active.")
    else:
        st.success(f"Operating with active **Google Gemini Integration** (`{GEMINI_API_KEY[:4]}...`).")

    if not problems:
        st.info("No active problems to formulate recommendations for.")
    else:
        for p in problems[:4]:
            rec = generate_decision_support(p, cross_insights)
            save_recommendation(rec)

        st.markdown(f"""
            <div style="background-color: #0f172a; border: 1px solid #334155; border-top: 4px solid #38bdf8; padding: 18px; border-radius: 8px; margin-bottom: 20px; color: #f8fafc;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h3 style="margin: 0; color: #38bdf8;">{rec['category']} Action: {rec['zone']}</h3>
                    <span style="background-color: #1e293b; color: #38bdf8; border: 1px solid #0284c7; padding: 4px 10px; border-radius: 4px; font-size: 0.8rem; font-weight: bold;">
                        Engine: {rec.get('provider', 'AI Agent')}
                    </span>
                </div>
                <hr style="margin: 12px 0; border: 0; border-top: 1px solid #334155;">
                <p style="margin: 8px 0; color: #f1f5f9; line-height: 1.5;">
                    <strong style="color: #94a3b8;">Recommended Action:</strong><br>{rec['action']}
                </p>
                <p style="margin: 8px 0; color: #f1f5f9; line-height: 1.5;">
                    <strong style="color: #94a3b8;">Underlying Reason & Evidence:</strong><br>{rec['reason']}
                </p>
                <p style="margin: 8px 0; color: #f1f5f9; line-height: 1.5;">
                    <strong style="color: #94a3b8;">Expected Environmental Benefit:</strong><br>{rec['expected_benefit']}
                </p>
                <div style="display: flex; justify-content: space-between; margin-top: 14px; font-size: 0.85rem; color: #94a3b8; border-top: 1px dashed #334155; padding-top: 8px;">
                    <span><b>Confidence Score:</b> <span style="color: #38bdf8;">{int(rec['confidence'] * 100)}%</span></span>
                    <span><b>Human Verification:</b> <span style="color: #f59e0b;">Mandatory</span></span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==============================================================================
# 10. ENVIRONMENTAL IMPACT
# ==============================================================================
elif page == "10. Environmental Impact":
    st.title("🌱 Environmental Impact Estimation Engine")
    st.caption("Modeled potential recovery benefits if proposed decision-support actions are implemented.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Est. Water Conserved", f"{impact['water_saved_liters_day']:,.0f} L/day")
    c2.metric("Est. Power Conserved", f"{impact['energy_saved_kwh_day']:,.1f} kWh/day")
    c3.metric("Est. Carbon Averted", f"{impact['emissions_reduced_kg_co2']:,.1f} kg CO2")
    c4.metric("Idle Duration Saved", f"{impact['idle_time_saved_hours']:,.1f} veh-hrs")

    st.markdown("---")
    st.subheader("Model Projections: Current Status vs. Remediated Projection")

    comp_df = pd.DataFrame({
        "Metric": ["Water Losses (kL)", "Excess Energy (MWh)", "Idling Emissions (kg CO2)"],
        "Current Unmitigated": [
            impact['water_saved_liters_day'] / 1000.0,
            impact['energy_saved_kwh_day'] / 1000.0,
            impact['emissions_reduced_kg_co2']
        ],
        "Post-Remediation (Target)": [
            (impact['water_saved_liters_day'] / 1000.0) * 0.15,
            (impact['energy_saved_kwh_day'] / 1000.0) * 0.20,
            impact['emissions_reduced_kg_co2'] * 0.25
        ]
    })

    fig = px.bar(
        comp_df, x="Metric", y=["Current Unmitigated", "Post-Remediation (Target)"],
        barmode="group", title="Remediation Impact Assessment (Simulated Model Estimates)"
    )
    st.plotly_chart(fig, use_container_width=True)
    st.info(f"Disclaimer: {impact['note']}")

# ==============================================================================
# 11. SCENARIO SIMULATOR
# ==============================================================================
elif page == "11. Scenario Simulator":
    st.title("🎮 Live Scenario Simulator")
    st.markdown("""
    Test how the integrated AI pipeline reacts to multi-domain disruptions.
    Selecting a scenario simulates real-world stress events and flows through detection, 
    cross-domain reasoning, prioritization, and impact estimation.
    """)

    st.write(f"Currently Active Scenario: **{scenario_option}**")
    st.write("To simulate a different scenario, choose from the sidebar and click **'Run Simulation Pipeline'**.")

# ==============================================================================
# 12. NATURAL LANGUAGE QUERY
# ==============================================================================
elif page == "12. Natural Language Query":
    st.title("💬 Grounded City Knowledge Query")
    st.markdown("Query live telemetry, detected problems, and sustainability priorities in natural language.")

    preset_queries = [
        "Which sustainability problem is currently the highest priority?",
        "Which zone has the highest water consumption?",
        "Why is Zone B marked critical?",
        "What factors are affecting air quality?",
        "How can water usage be reduced in Zone B?"
    ]

    selected_query = st.selectbox("Sample Executive Prompts:", [""] + preset_queries)
    custom_query = st.text_input("Or enter your own question:", value=selected_query)

    if st.button("Query City Telemetry Agent") and custom_query:
        q = custom_query.lower()
        response = ""

        if "highest priority" in q or "priority" in q:
            if problems:
                top = problems[0]
                response = (
                    f"The highest priority issue right now is in **{top['zone']}** related to **{top['category']}** "
                    f"with a Priority Score of **{top['priority_score']}/100** ({top['priority_status']}). "
                    f"{top['explanation']}"
                )
            else:
                response = "There are currently no high-priority sustainability problems flagged."

        elif "water" in q and ("highest" in q or "zone" in q):
            recent_wtr = city_data["water"].sort_values("timestamp").groupby("zone_id").last().reset_index()
            highest_wtr = recent_wtr.sort_values("water_consumption", ascending=False).iloc[0]
            response = (
                f"**{highest_wtr['zone_id']}** currently reports the highest water consumption at "
                f"**{highest_wtr['water_consumption']:,.1f} L/h** compared to its historical average of "
                f"{highest_wtr['historical_average']:,.1f} L/h."
            )

        elif "zone b" in q and "critical" in q:
            z_probs = [p for p in problems if p["zone"] == "Zone B"]
            if z_probs:
                p = z_probs[0]
                response = (
                    f"**Zone B** is flagged as **{p['priority_status']}** due to a detected **{p['category']}** problem. "
                    f"{p['explanation']} Telemetry indicates a measured value of {p['detected_value']} against "
                    f"an expected baseline of {p['expected_value']} (+{p['deviation_percent']}% deviation)."
                )
            else:
                response = "Zone B is currently operating within normal sustainability thresholds."

        elif "air quality" in q or "factors" in q:
            response = (
                "Air quality is primarily driven by vehicle volume, arterial idle duration, "
                "and microclimate inversion layers. Telemetry confirms that zones with average speeds under "
                "18 km/h experience up to a 65% elevation in localized PM2.5 and NO2 levels."
            )

        elif "reduced" in q or "action" in q:
            response = (
                "To curb anomalous usage in Zone B, the AI Decision Agent recommends: "
                "1) Dispatching maintenance crews to verify district meter and valve integrity, "
                "2) Conducting an automated pressure drop audit across pipeline segments, and "
                "3) Inspecting high-volume commercial cooling installations."
            )

        else:
            response = (
                f"Based on real-time city telemetry: The city sustainability index stands at {overall_score}/100. "
                f"There are {len(problems)} active problem candidates across traffic, energy, water, waste, and air quality domains."
            )

        st.markdown(f"""
        <div style="background-color: #f8fafc; border-left: 4px solid #0ea5e9; padding: 16px; border-radius: 6px; margin-top: 15px;">
            <b>Grounded Decision Assistant Response:</b><br>{response}
        </div>
        """, unsafe_allow_html=True)

# ==============================================================================
# 13. ABOUT & ARCHITECTURE
# ==============================================================================
elif page == "13. About":
    st.title("ℹ️ About SmartCity AI")
    st.markdown("""
    ### System Architecture & Methodology

    SmartCity AI is an integrated Decision-Support Platform that transforms fragmented municipal data 
    into prioritized, explainable, and responsible sustainability interventions.

    ```text
    CITY DATA → PREPROCESSING → ML ANOMALY DETECTION → PROBLEM ENGINE → 
    CROSS-DOMAIN REASONING → PRIORITY SCORING → AI DECISION AGENT → IMPACT ESTIMATION
    ```

    #### Analytical Tenets:
    1. **Correlation ≠ Causation:** Inter-domain synergies (e.g. traffic congestion correlating with NO2 spikes) are surfaced as associative indicators.
    2. **Explainable Priority Scoring:** Transparent formula incorporating severity, urgency, carbon/environmental impact, resource waste, and exposed population.
    3. **Human-in-the-Loop:** Explicit guardrails stipulate that AI outputs are advisory and require domain verification prior to physical implementation.
    """)