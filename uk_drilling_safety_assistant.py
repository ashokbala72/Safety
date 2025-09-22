import os
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import AzureOpenAI

# ========================
# Azure OpenAI Setup
# ========================
load_dotenv()
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

# ========================
# Data Simulations
# ========================
def simulate_seismic():
    now = datetime.now()
    timestamps = [now - timedelta(seconds=60*i) for i in range(30)]
    latitudes = np.random.uniform(57.0, 57.5, 30)
    longitudes = np.random.uniform(-1.5, -0.5, 30)
    amplitudes = np.random.uniform(0.2, 0.8, 30)
    import random
    risk_levels = random.choices(["🟢", "🟡", "🔴"], weights=[1, 3, 6], k=30)
    return pd.DataFrame({
        "Timestamp": timestamps,
        "Latitude": latitudes,
        "Longitude": longitudes,
        "Amplitude": amplitudes,
        "Fault Risk": risk_levels
    })

def simulate_drilling_view():
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=50, freq="min")
    return pd.DataFrame({
        "Timestamp": timestamps,
        "Torque": np.random.uniform(300, 500, size=len(timestamps)),
        "ROP": np.random.uniform(10, 20, size=len(timestamps))
    })

def simulate_sensor_data():
    base_time = datetime.now() - timedelta(hours=2)
    timestamps = [base_time + timedelta(seconds=30 * i) for i in range(240)]
    return pd.DataFrame({
        "Timestamp": timestamps,
        "WOB (lbs)": np.random.normal(25000, 1500, len(timestamps)).clip(20000, 30000),
        "RPM (rev/min)": np.random.normal(120, 10, len(timestamps)).clip(80, 150),
        "Torque (ft-lbf)": np.random.normal(10000, 1200, len(timestamps)).clip(7000, 13000),
        "Mud Flow (gpm)": np.random.normal(480, 25, len(timestamps)).clip(400, 550),
        "Bit Depth (ft)": np.linspace(8500, 8800, len(timestamps))
    })

def simulate_logs():
    depths = np.arange(8000, 10000, 0.5)
    return pd.DataFrame({
        "Depth (ft)": depths,
        "GR (API)": np.random.normal(75, 15, len(depths)),
        "RHOB (g/cc)": np.random.normal(2.5, 0.1, len(depths)),
        "NPHI (v/v)": np.random.normal(0.25, 0.05, len(depths)),
        "RT (ohm.m)": np.random.normal(20, 5, len(depths))
    })

def simulate_bit_wear():
    time = [datetime.now() - timedelta(minutes=60 - i) for i in range(60)]
    wear = np.cumsum(np.random.uniform(0.5, 1.5, len(time)))
    wear = (wear / max(wear)) * 100
    return pd.DataFrame({"Time": time, "Bit Wear (%)": wear})

# ========================
# GenAI helper
# ========================
def genai_summary(title, table_df):
    """Call Azure OpenAI to generate hazard summary."""
    try:
        with st.spinner(f"🔍 GenAI analyzing {title} hazards..."):
            prompt = f"""
            You are a drilling safety expert.
            Analyze the following hazards for {title}:

            {table_df.to_string(index=False)}

            Provide a short summary covering:
            - Main crew safety risks
            - Most likely incident
            - One immediate mitigation action
            """
            response = client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=300
            )
        st.success(response.choices[0].message.content)
    except Exception as e:
        st.error(f"GenAI error: {str(e)}")

# ========================
# Layout
# ========================
st.set_page_config(page_title="UK Oil & Gas Safety & Drilling Optimization Assistant", layout="wide")
main_tab, app_tab = st.tabs(["📘 Overview", "🛠️ Main App"])

# ========================
# Overview Tab
# ========================
with main_tab:
    st.title("📘 Overview: UK Oil & Gas Safety & Drilling Optimization Assistant")
    st.markdown("""
This assistant monitors simulated drilling data, predicts hazards, and generates **Azure OpenAI insights** for every tab.

Navigate to the **Main App** tab to explore live simulations.
""")

# ========================
# Main App Tabs
# ========================
with app_tab:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "🎛️ Real-Time Drilling View", "🪓 Bit Wear Monitoring", "💡 Auto Parameter Tuning",
        "🔥 Safety & Risk Prediction", "📈 Logs & Lithology Viewer", "🌍 Seismic Interpreter",
        "📊 Performance Dashboard", "📌 GenAI Recommendations", "🧠 GenAI Forecast", "❓ Ask a Query"
    ])

    # Tab1
    with tab1:
        st.subheader("🎛️ Real-Time Drilling View")
        drilling_df = simulate_drilling_view()
        st.dataframe(drilling_df)
        hazards = pd.DataFrame({
            "Issue": ["Torque/ROP Drift", "High Vibration"],
            "Operational Hazard": ["Poor hole cleaning", "Fatigue of BHA"],
            "Employee Safety Risk": ["Pipe trip injury", "Tool detachment"],
            "Severity": ["🟡", "🔴"],
            "Mitigation Step": ["Optimize hole cleaning", "Install vibration dampeners"]
        })
        st.dataframe(hazards)
        genai_summary("Real-Time Drilling View", hazards)

    # Tab2
    with tab2:
        st.subheader("🪓 Bit Wear Monitoring")
        wear_df = simulate_bit_wear()
        st.dataframe(wear_df)
        hazards = pd.DataFrame({
            "Issue": ["High Bit Wear", "Overpull Events"],
            "Operational Hazard": ["Bit failure", "Tripping snapback"],
            "Employee Safety Risk": ["Flying metal", "Whiplash injuries"],
            "Severity": ["🔴", "🟡"],
            "Mitigation Step": ["Replace bit before 85% wear", "Use controlled tripping speeds"]
        })
        st.dataframe(hazards)
        genai_summary("Bit Wear Monitoring", hazards)

    # Tab3
    with tab3:
        st.subheader("💡 Auto Parameter Tuning")
        drilling_df = simulate_drilling_view()
        st.dataframe(drilling_df)
        hazards = pd.DataFrame({
            "Issue": ["Torque/ROP Drift", "High Vibration"],
            "Operational Hazard": ["Poor hole cleaning", "Fatigue of BHA"],
            "Employee Safety Risk": ["Pipe trip injury", "Tool detachment"],
            "Severity": ["🟡", "🔴"],
            "Mitigation Step": ["Optimize hole cleaning", "Install vibration dampeners"]
        })
        st.dataframe(hazards)
        genai_summary("Auto Parameter Tuning", hazards)

    # Tab4
    with tab4:
        st.subheader("🔥 Safety & Risk Prediction")
        perf_data = pd.DataFrame({
            "Metric": ["Drilling Speed", "Fuel Usage", "Downtime Hours"],
            "Value": [np.random.uniform(15, 25), np.random.uniform(1000, 2000), np.random.randint(2, 6)],
            "Unit": ["m/hr", "L/day", "hours"]
        })
        st.dataframe(perf_data)
        hazards = pd.DataFrame({
            "Issue": ["Excessive Downtime"],
            "Operational Hazard": ["Missed production target"],
            "Employee Safety Risk": ["Fatigue-induced accidents"],
            "Severity": ["🟡"],
            "Mitigation Step": ["Shift rotation monitoring"]
        })
        st.dataframe(hazards)
        genai_summary("Safety & Risk Prediction", hazards)

    # Tab5
    with tab5:
        st.subheader("📈 Logs & Lithology Viewer")
        logs_df = simulate_logs()
        st.dataframe(logs_df)
        hazards = pd.DataFrame({
            "Issue": ["Abnormal GR/NPHI Logs", "Shale Instability"],
            "Operational Hazard": ["Formation collapse", "Swelling shale"],
            "Employee Safety Risk": ["Trapped tools", "Rig instability"],
            "Severity": ["🔴", "🟡"],
            "Mitigation Step": ["Set casing early", "Use mud stabilizers"]
        })
        st.dataframe(hazards)
        genai_summary("Logs & Lithology Viewer", hazards)

    # Tab6
    with tab6:
        st.subheader("🌍 Seismic Interpreter")
        seismic_df = simulate_seismic()
        st.dataframe(seismic_df)
        hazards = pd.DataFrame({
            "Issue": ["Seismic Fault Zone", "Pressure Contrast Zones"],
            "Operational Hazard": ["Casing collapse", "Formation instability"],
            "Employee Safety Risk": ["Explosion risk", "Evacuation hazard"],
            "Severity": ["🔴", "🔴"],
            "Mitigation Step": ["Adjust mud weight", "Install pressure sensors"]
        })
        st.dataframe(hazards)
        genai_summary("Seismic Interpreter", hazards)

    # Tab7
    with tab7:
        st.subheader("📊 Performance Dashboard")
        perf_df = pd.DataFrame({
            "KPI": ["ROP Variance (%)", "NPT (%)", "Drilling Stability Index"],
            "Value": [12.5, 6.7, 0.78]
        })
        st.dataframe(perf_df)
        hazards = pd.DataFrame({
            "Issue": ["High ROP Variance"],
            "Operational Hazard": ["Hole cleaning issues"],
            "Employee Safety Risk": ["Stuck pipe hazard"],
            "Severity": ["🟡"],
            "Mitigation Step": ["Optimize drilling parameters"]
        })
        st.dataframe(hazards)
        genai_summary("Performance Dashboard", hazards)

    # Tab8
    with tab8:
        st.subheader("📌 GenAI Recommendations")
        hazards = pd.DataFrame({
            "Focus": ["Production Optimization", "Water Management", "Pressure Maintenance"],
            "Recent Metric": ["ROP variance ↑", "High WC%", "Pressure drop"],
        })
        st.dataframe(hazards)
        genai_summary("Operational Recommendations", hazards)

    # Tab9
    with tab9:
        st.subheader("🧠 GenAI Forecast")
        forecast_df = pd.DataFrame({
            "Issue": ["High Bit Wear", "Shale Instability", "Seismic Fault Zone"],
            "Severity": ["🔴", "🟡", "🔴"]
        })
        st.dataframe(forecast_df)
        genai_summary("System-wide Forecast", forecast_df)

    # Tab10
    with tab10:
    st.subheader("❓ Ask a Query")
    st.markdown("Type your question and let the GenAI assistant help:")
    query = st.text_input("Enter your question:")

    if query:
        # Aggregate hazards from all tabs
        hazards = []
        for df in [drilling_view_table, bit_wear_table, logs_table, seismic_table, perf_table, hazard_table, forecast_table]:
            if 'Issue' in df.columns:
                for _, row in df.iterrows():
                    hazards.append(f"- {row['Issue']} (Severity: {row['Severity']}) | "
                                   f"Hazard: {row['Operational Hazard']} | "
                                   f"Safety Risk: {row['Employee Safety Risk']}")

        hazard_summary = "\n".join(hazards[:30])  # limit to 30 hazards for token safety

        # Build prompt
        prompt = f"""
You are a drilling safety assistant. Below is the list of identified hazards during operations:

{hazard_summary}

User Question: {query}

Answer clearly:
1. Are workers safe overall? (Safe / Unsafe)
2. Justify based on severity distribution (🔴 vs 🟡 vs 🟢).
3. Provide 3 safety recommendations.
"""

        with st.spinner("Analyzing hazards with GenAI..."):
            try:
                response = client.chat.completions.create(
                    model=DEPLOYMENT_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=800
                )
                answer = response.choices[0].message.content.strip()
                st.markdown("### 🧠 GenAI Safety Assessment")
                st.markdown(answer)
            except Exception as e:
                st.error(f"⚠️ Error fetching GenAI answer: {e}")

