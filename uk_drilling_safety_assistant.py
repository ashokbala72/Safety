
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


def simulate_seismic():
    import numpy as np
    import random
    from datetime import datetime, timedelta
    now = datetime.now()
    timestamps = [now - timedelta(seconds=60*i) for i in range(30)]
    latitudes = np.random.uniform(57.0, 57.5, 30)
    longitudes = np.random.uniform(-1.5, -0.5, 30)
    amplitudes = np.random.uniform(0.2, 0.8, 30)
    risk_levels = random.choices(["🟢", "🟡", "🔴"], weights=[1, 3, 6], k=30)
    return pd.DataFrame({
        "Timestamp": timestamps,
        "Latitude": latitudes,
        "Longitude": longitudes,
        "Amplitude": amplitudes,
        "Fault Risk": risk_levels
    })



def simulate_drilling_view():
    import numpy as np
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=50, freq="min")
    return pd.DataFrame({
        "Timestamp": timestamps,
        "Torque": np.random.uniform(300, 500, size=len(timestamps)),
        "ROP": np.random.uniform(10, 20, size=len(timestamps))
    })

from datetime import datetime, timedelta

st.set_page_config(page_title="UK Oil & Gas Safety & Drilling Optimization Assistant", layout="wide")

# Generate mock time series data for drilling sensors
def simulate_sensor_data():
    base_time = datetime.now() - timedelta(hours=2)
    timestamps = [base_time + timedelta(seconds=30 * i) for i in range(240)]
    data = pd.DataFrame({
        "Timestamp": timestamps,
        "WOB (lbs)": np.random.normal(25000, 1500, len(timestamps)).clip(20000, 30000),
        "RPM (rev/min)": np.random.normal(120, 10, len(timestamps)).clip(80, 150),
        "Torque (ft-lbf)": np.random.normal(10000, 1200, len(timestamps)).clip(7000, 13000),
        "Mud Flow (gpm)": np.random.normal(480, 25, len(timestamps)).clip(400, 550),
        "Bit Depth (ft)": np.linspace(8500, 8800, len(timestamps))
    })
    return data

# Simulate lithology logs
def simulate_logs():
    depths = np.arange(8000, 10000, 0.5)
    logs = pd.DataFrame({
        "Depth (ft)": depths,
        "GR (API)": np.random.normal(75, 15, len(depths)),
        "RHOB (g/cc)": np.random.normal(2.5, 0.1, len(depths)),
        "NPHI (v/v)": np.random.normal(0.25, 0.05, len(depths)),
        "RT (ohm.m)": np.random.normal(20, 5, len(depths))
    })
    return logs

# Generate bit wear
def simulate_bit_wear():
    time = [datetime.now() - timedelta(minutes=60 - i) for i in range(60)]
    wear = np.cumsum(np.random.uniform(0.5, 1.5, len(time)))
    wear = (wear / max(wear)) * 100
    return pd.DataFrame({"Time": time, "Bit Wear (%)": wear})

# Layout
main_tab, app_tab = st.tabs(["📘 Overview", "🛠️ Main App"])

# Overview

with main_tab:
    st.title("📘 Overview: UK Oil & Gas Safety & Drilling Optimization Assistant")
    st.markdown("""
Welcome to the **UK Drilling Safety Assistant** – a GenAI-powered dashboard to monitor and enhance the safety of oil & gas drilling operations.

This prototype simulates conditions in a large-scale UK drilling operation and provides insights on safety risks and mitigation steps.

### 🧭 What Each Tab Does (in Simple Terms):
- **🎛️ Real-Time Drilling View**: Shows live torque and rate-of-penetration trends, along with related drilling hazards.
- **🎯 Auto Parameter Tuning**: Monitors drill bit wear and suggests safer operational settings.
- **🔧 Bit Wear Monitoring**: Tracks bit wear and vibration data to prevent tool failure and injuries.
- **💰 Efficiency & Cost Tracker**: Highlights inefficiencies that could increase risk or cost.
- **📊 Performance Dashboard**: Visual summary of operations, speeds, depths, and alerts.
- **🔥 Safety & Risk Prediction**: Predicts major hazards like blowouts and overpressure zones using advanced logic.
- **🧠 GenAI Forecast**: Compiles all hazards and gives a safety overview across the entire operation.
- **❓ Ask a Query**: Chat with the assistant to ask safety-related questions interactively.

### 🧪 Simulated vs Real-Time Data:
- ✅ **Real-Time Feeds**:
  - **Seismic Data** (live simulation, replaceable with actual seismic feed)
  - **Weather Feed** (live simulation, link to weather API)
- 🧪 **Simulated Data**:
  - Drilling sensor data (Torque, ROP, Bit wear)
  - Safety predictions, hazard forecasts

> ℹ️ *No CSV uploads are required; all mock data is auto-generated.*

### 🔧 Making It Production Ready:
To deploy this app in a real-world drilling site, the following integrations are needed:

| System | Purpose |
|--------|---------|
| 🎛️ SCADA / Historian | Real-time drilling sensors (Torque, Vibration, ROP) |
| 🌍 Seismic API | Live seismic feed |
| ☁️ Weather API | Weather-based hazard detection |
| 🧠 GenAI Engine | GPT-4/GPT-3.5-based advisory |
| 💼 HSE System | Integration with compliance and audit tracking |
| 🔐 Identity System | Role-based access for field crew, supervisors, HSE auditors |

This assistant is designed to operate both **in the field** and **in remote command centers**.

Feel free to navigate to each tab and simulate safety hazards across real drilling workflows.
""")


with app_tab:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "🎛️ Real-Time Drilling View", "🪓 Bit Wear Monitoring", "💡 Auto Parameter Tuning",
        "🔥 Safety & Risk Prediction", "📈 Logs & Lithology Viewer", "🌍 Seismic Interpreter",
        "📊 Performance Dashboard", "📌 GenAI Recommendations", "🧠 GenAI Forecast", "❓ Ask a Query"
    ])

    
    
    with tab1:
        st.subheader("🎛️ Real-Time Drilling View")
        drilling_df = simulate_drilling_view()
        st.dataframe(drilling_df)
        fig = px.line(drilling_df, x="Timestamp", y=["Torque", "ROP"], title="Torque and ROP Trends")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🛑 Hazards")
        drilling_view_table = pd.DataFrame({
            "Issue": ["Torque/ROP Drift", "High Vibration"],
            "Operational Hazard": ["Poor hole cleaning, stuck pipe", "Fatigue of BHA, component failure"],
            "Employee Safety Risk": ["Unexpected pipe trip, injury risk", "Tool detachment, flying debris"],
            "Severity": ["🟡", "🔴"],
            "Mitigation Step": [
                "Optimize cleaning schedule, monitor cuttings",
                "Use vibration dampeners, monitor downhole sensors"
            ]
        })
        st.dataframe(drilling_view_table, use_container_width=True)

    with tab2:
        st.subheader("🪓 Bit Wear Monitoring")
        wear_df = simulate_bit_wear()
        st.dataframe(wear_df)
        fig = px.line(wear_df, x="Time", y="Bit Wear (%)", title="Bit Wear Progression")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🛑 Hazards")
        bit_wear_table = pd.DataFrame({
            "Issue": ["High Bit Wear", "Overpull Events"],
            "Operational Hazard": ["Bit failure during drilling", "Tripping snapback or pipe over-tension"],
            "Employee Safety Risk": ["Flying metal, hand/facial injury", "Whiplash or dropped objects"],
            "Severity": ["🔴", "🟡"],
            "Mitigation Step": [
                "Replace bit before 85% wear, monitor wear sensors",
                "Use controlled tripping speeds, monitor pipe tension"
            ]
        })
        st.dataframe(bit_wear_table, use_container_width=True)
    
    
    
    
    
    with tab3:
        st.subheader("💡 Auto Parameter Tuning")
        drilling_df = simulate_drilling_view()
        st.dataframe(drilling_df)
        fig = px.line(drilling_df, x="Timestamp", y=["Torque", "ROP"], title="Torque and ROP Trends")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🛑 Hazards")
        drilling_view_table = pd.DataFrame({
            "Issue": ["Torque/ROP Drift", "High Vibration"],
            "Operational Hazard": ["Poor hole cleaning, stuck pipe", "Fatigue of BHA, component failure"],
            "Employee Safety Risk": ["Unexpected pipe trip, injury risk", "Tool detachment, flying debris"],
            "Severity": ["🟡", "🔴"],
            "Mitigation Step": [
                "Optimize cleaning schedule, monitor cuttings",
                "Use vibration dampeners, monitor downhole sensors"
            ]
        })
        st.dataframe(drilling_view_table, use_container_width=True)

    with tab4:
        st.subheader("🔥 Safety & Risk Prediction")
        perf_data = pd.DataFrame({
            "Metric": ["Drilling Speed", "Fuel Usage", "Downtime Hours"],
            "Value": [np.random.uniform(15, 25), np.random.uniform(1000, 2000), np.random.randint(2, 6)],
            "Unit": ["m/hr", "L/day", "hours"]
        })
        st.dataframe(perf_data, use_container_width=True)
        fig = px.bar(perf_data, x="Metric", y="Value", color="Metric", title="Performance Metrics")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🛑 Hazards")
        perf_table = pd.DataFrame({
            "Issue": ["Excessive Downtime"],
            "Operational Hazard": ["Missed production target, crew overwork"],
            "Employee Safety Risk": ["Fatigue-induced accidents"],
            "Severity": ["🟡"],
            "Mitigation Step": ["Shift rotation & real-time performance monitoring"]
        })
        st.dataframe(perf_table, use_container_width=True)

    with tab5:
        st.subheader("📈 Logs & Lithology Viewer")
        logs_df = simulate_logs()
        st.dataframe(logs_df)
        st.line_chart(logs_df.set_index("Depth (ft)"))

        st.markdown("### 🛑 Hazards")
        logs_table = pd.DataFrame({
            "Issue": ["Abnormal GR/NPHI Logs", "Shale Instability"],
            "Operational Hazard": ["Formation collapse or lost circulation", "Sloughing or swelling shale"],
            "Employee Safety Risk": ["Confined space hazard, trapped tools", "Rig instability or personnel fall-in"],
            "Severity": ["🔴", "🟡"],
            "Mitigation Step": [
                "Set casing early, monitor logs closely",
                "Use appropriate mud weight and stabilizers"
            ]
        })
        st.dataframe(logs_table, use_container_width=True)
    
    
    with tab6:
        st.subheader("🌍 Seismic Interpreter")
        seismic_df = simulate_seismic()
        st.dataframe(seismic_df)
        fig = px.scatter(seismic_df, x="Longitude", y="Latitude", color="Fault Risk", size="Amplitude", title="Seismic Fault Zones")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🛑 Hazards")
        seismic_table = pd.DataFrame({
            "Issue": ["Seismic Fault Zone", "Pressure Contrast Zones"],
            "Operational Hazard": ["Casing collapse, formation influx", "Formation instability, kick risk"],
            "Employee Safety Risk": ["Explosion, toxic gas exposure", "Evacuation hazard, rig shutdown"],
            "Severity": ["🔴", "🔴"],
            "Mitigation Step": [
                "Adjust mud weight, run seismic pre-checks",
                "Install pressure sensors, monitor influx rates"
            ]
        })
        st.dataframe(seismic_table, use_container_width=True)
    
    with tab7:
        st.subheader("📊 Performance Dashboard")
        perf_df = pd.DataFrame({
            "KPI": ["ROP Variance (%)", "NPT (%)", "Drilling Stability Index"],
            "Value": [12.5, 6.7, 0.78]
        })
        st.dataframe(perf_df)
        fig = px.bar(perf_df, x="KPI", y="Value", title="Performance Metrics")
        st.plotly_chart(fig, use_container_width=True)
        st.info("GenAI Safety Note: High ROP variance may indicate hole cleaning issues – potential stuck pipe or tool ejection hazard for operators.")

    
    with tab8:
        st.subheader("🔥 Safety & Risk Prediction")
        safety_df = pd.DataFrame({
            "Area": ["Rig Floor", "Drill Pipe", "Mud Circulation"],
            "Predicted Risk Level": ["🔴", "🟡", "🟡"],
            "Last Incident": ["Slip & fall", "Thread galling", "Loss circulation"],
            "Mitigation Action": [
                "Install anti-slip mats and alerts",
                "Ensure pipe dope consistency & torque control",
                "Monitor flow rates, adjust LCM"
            ]
        })
        st.dataframe(safety_df, use_container_width=True)

        st.markdown("### 🛑 Hazards")
        hazard_table = pd.DataFrame({
            "Issue": ["Floor Slips", "Mechanical Thread Failures"],
            "Operational Hazard": ["Crew injury on wet floor", "Tool seizure or damaged strings"],
            "Employee Safety Risk": ["Bone fractures, downtime", "Unexpected tripping & falling equipment"],
            "Severity": ["🔴", "🟡"],
            "Mitigation Step": [
                "Anti-slip flooring, real-time moisture alerts",
                "Inspect threads, apply calibrated torque"
            ]
        })
        st.dataframe(hazard_table, use_container_width=True)

    
    with tab9:
        st.subheader("🧠 GenAI Forecast")
        st.markdown("This tab aggregates predicted operational risks across drilling operations.")

        forecast_table = pd.DataFrame({
            "Issue": [
                "High Bit Wear", "Overpull Events", "Abnormal GR/NPHI Logs", "Shale Instability",
                "Torque/ROP Drift", "High Vibration", "Seismic Fault Zone", "Pressure Contrast Zones",
                "Excessive Downtime", "Floor Slips", "Mechanical Thread Failures"
            ],
            "Operational Hazard": [
                "Bit failure during drilling", "Tripping snapback or pipe over-tension",
                "Formation collapse or lost circulation", "Sloughing or swelling shale",
                "Poor hole cleaning, stuck pipe", "Fatigue of BHA, component failure",
                "Casing collapse, formation influx", "Formation instability, kick risk",
                "Missed production target, crew overwork", "Crew injury on wet floor", "Tool seizure or damaged strings"
            ],
            "Employee Safety Risk": [
                "Flying metal, hand/facial injury", "Whiplash or dropped objects",
                "Confined space hazard, trapped tools", "Rig instability or personnel fall-in",
                "Unexpected pipe trip, injury risk", "Tool detachment, flying debris",
                "Explosion, toxic gas exposure", "Evacuation hazard, rig shutdown",
                "Fatigue-induced accidents", "Bone fractures, downtime", "Unexpected tripping & falling equipment"
            ],
            "Severity": [
                "🔴", "🟡", "🔴", "🟡", "🟡", "🔴", "🔴", "🔴", "🟡", "🔴", "🟡"
            ],
            "Mitigation Step": [
                "Replace bit before 85% wear, monitor wear sensors",
                "Use controlled tripping speeds, monitor pipe tension",
                "Set casing early, monitor logs closely",
                "Use appropriate mud weight and stabilizers",
                "Optimize cleaning schedule, monitor cuttings",
                "Use vibration dampeners, monitor downhole sensors",
                "Adjust mud weight, run seismic pre-checks",
                "Install pressure sensors, monitor influx rates",
                "Shift rotation & real-time performance monitoring",
                "Anti-slip flooring, real-time moisture alerts",
                "Inspect threads, apply calibrated torque"
            ]
        })
        st.dataframe(forecast_table, use_container_width=True)

    
    
    
    
    
    
    with tab10:
        st.subheader("❓ Ask a Query")
        st.markdown("Type your question and let the GenAI assistant help:")
        query = st.text_input("Enter your question:")
        if query:
            st.markdown("🧠 GenAI Response:")
            if "safe" in query.lower():
                safety_summary = """
Based on current operational data:

- 🛠️ Real-Time Drilling View shows hazards like Torque/ROP Drift (🟡) and High Vibration (🔴)
- 🔧 Auto Parameter Tuning reports High Bit Wear (🔴)
- 🔥 Safety & Risk Prediction highlights Blowout risk (🔴) and Overpressure zones (🟡)

While most risks are being mitigated, the presence of multiple 🔴 high-severity hazards suggests that employee safety is at **elevated risk**.

✅ Recommended Actions:
• Reinforce rig crew briefing
• Monitor vibration and pressure sensors
• Schedule preventative checks immediately
"""
                st.info(safety_summary)
            else:
                st.info(f"""This is a simulated GenAI answer to your question: '{query}'

• Please ensure operations comply with HSE standards.""")
