# drilling_safety_app_azure.py

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# -----------------------------
# Azure OpenAI Setup
# -----------------------------
load_dotenv()
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-raj")

client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

# -----------------------------
# Simulation Functions
# -----------------------------
def simulate_seismic():
    import random
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
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=50, freq="min")
    return pd.DataFrame({
        "Timestamp": timestamps,
        "Torque": np.random.uniform(300, 500, size=len(timestamps)),
        "ROP": np.random.uniform(10, 20, size=len(timestamps))
    })

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

def simulate_bit_wear():
    time = [datetime.now() - timedelta(minutes=60 - i) for i in range(60)]
    wear = np.cumsum(np.random.uniform(0.5, 1.5, len(time)))
    wear = (wear / max(wear)) * 100
    return pd.DataFrame({"Time": time, "Bit Wear (%)": wear})

# -----------------------------
# Layout
# -----------------------------
st.set_page_config(page_title="UK Oil & Gas Safety & Drilling Optimization Assistant", layout="wide")
main_tab, app_tab = st.tabs(["📘 Overview", "🛠️ Main App"])

# -----------------------------
# Overview Tab
# -----------------------------
with main_tab:
    st.title("📘 Overview: UK Oil & Gas Safety & Drilling Optimization Assistant")
    st.markdown("""
Welcome to the **UK Drilling Safety Assistant** – a GenAI-powered dashboard to monitor and enhance the safety of oil & gas drilling operations.

This prototype simulates conditions in a large-scale UK drilling operation and provides insights on safety risks and mitigation steps.

### 🧭 What Each Tab Does:
- 🎛️ Real-Time Drilling View – live torque & ROP + hazards
- 🪓 Bit Wear Monitoring – bit wear & risks
- 💡 Auto Parameter Tuning – safe operational tuning
- 🔥 Safety & Risk Prediction – hazards from performance metrics
- 📈 Logs & Lithology Viewer – lithology logs
- 🌍 Seismic Interpreter – seismic fault zones
- 📊 Performance Dashboard – KPIs & notes
- 📌 GenAI Recommendations – AI-driven safety steps
- 🧠 GenAI Forecast – aggregated hazards + AI analysis
- ❓ Ask a Query – interactive GenAI assistant

### 🔧 Making It Production Ready:
Integrate with SCADA, seismic APIs, weather APIs, and HSE systems.
""")


# -----------------------------
# Main App Tabs
# -----------------------------
with app_tab:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "🎛️ Real-Time Drilling View", "🪓 Bit Wear Monitoring", "💡 Auto Parameter Tuning",
        "🔥 Safety & Risk Prediction", "📈 Logs & Lithology Viewer", "🌍 Seismic Interpreter",
        "📊 Performance Dashboard", "📌 GenAI Recommendations", "🧠 GenAI Forecast", "❓ Ask a Query"
    ])

    # -----------------------------
    # Tab 1: Real-Time Drilling View
    # -----------------------------
    with tab1:
        st.subheader("🎛️ Real-Time Drilling View")
        drilling_df = simulate_drilling_view()
        st.dataframe(drilling_df)
        fig = px.line(drilling_df, x="Timestamp", y=["Torque", "ROP"])
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🛑 Hazards")
        st.dataframe(pd.DataFrame({
            "Issue": ["Torque/ROP Drift", "High Vibration"],
            "Operational Hazard": ["Poor hole cleaning, stuck pipe", "Fatigue of BHA, component failure"],
            "Employee Safety Risk": ["Unexpected pipe trip, injury risk", "Tool detachment, flying debris"],
            "Severity": ["🟡", "🔴"],
            "Mitigation Step": [
                "Optimize cleaning schedule, monitor cuttings",
                "Use vibration dampeners, monitor downhole sensors"
            ]
        }))

    # -----------------------------
    # Tab 2: Bit Wear Monitoring
    # -----------------------------
    with tab2:
        st.subheader("🪓 Bit Wear Monitoring")
        wear_df = simulate_bit_wear()
        st.dataframe(wear_df)
        fig = px.line(wear_df, x="Time", y="Bit Wear (%)")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🛑 Hazards")
        st.dataframe(pd.DataFrame({
            "Issue": ["High Bit Wear", "Overpull Events"],
            "Operational Hazard": ["Bit failure during drilling", "Tripping snapback or pipe over-tension"],
            "Employee Safety Risk": ["Flying metal, hand/facial injury", "Whiplash or dropped objects"],
            "Severity": ["🔴", "🟡"],
            "Mitigation Step": [
                "Replace bit before 85% wear, monitor wear sensors",
                "Use controlled tripping speeds, monitor pipe tension"
            ]
        }))

    # -----------------------------
    # Tab 3: Auto Parameter Tuning
    # -----------------------------
    with tab3:
        st.subheader("💡 Auto Parameter Tuning")
        drilling_df = simulate_drilling_view()
        st.dataframe(drilling_df)
        fig = px.line(drilling_df, x="Timestamp", y=["Torque", "ROP"])
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 🛑 Hazards")
        st.dataframe(pd.DataFrame({
            "Issue": ["Torque/ROP Drift", "High Vibration"],
            "Operational Hazard": ["Poor hole cleaning, stuck pipe", "Fatigue of BHA, component failure"],
            "Employee Safety Risk": ["Unexpected pipe trip, injury risk", "Tool detachment, flying debris"],
            "Severity": ["🟡", "🔴"],
            "Mitigation Step": [
                "Optimize cleaning schedule, monitor cuttings",
                "Use vibration dampeners, monitor downhole sensors"
            ]
        }))

    # -----------------------------
    # Tab 4: Safety & Risk Prediction
    # -----------------------------
    with tab4:
        st.subheader("🔥 Safety & Risk Prediction")
        perf_data = pd.DataFrame({
            "Metric": ["Drilling Speed", "Fuel Usage", "Downtime Hours"],
            "Value": [np.random.uniform(15, 25), np.random.uniform(1000, 2000), np.random.randint(2, 6)],
            "Unit": ["m/hr", "L/day", "hours"]
        })
        st.dataframe(perf_data)
        st.plotly_chart(px.bar(perf_data, x="Metric", y="Value", color="Metric"))

    # -----------------------------
    # Tab 5: Logs & Lithology Viewer
    # -----------------------------
    with tab5:
        st.subheader("📈 Logs & Lithology Viewer")
        logs_df = simulate_logs()
        st.dataframe(logs_df)
        st.line_chart(logs_df.set_index("Depth (ft)"))

    # -----------------------------
    # Tab 6: Seismic Interpreter
    # -----------------------------
    with tab6:
        st.subheader("🌍 Seismic Interpreter")
        seismic_df = simulate_seismic()
        st.dataframe(seismic_df)
        st.plotly_chart(px.scatter(seismic_df, x="Longitude", y="Latitude",
                                   color="Fault Risk", size="Amplitude"))

    # -----------------------------
    # Tab 7: Performance Dashboard
    # -----------------------------
    with tab7:
        st.subheader("📊 Performance Dashboard")
        perf_df = pd.DataFrame({
            "KPI": ["ROP Variance (%)", "NPT (%)", "Drilling Stability Index"],
            "Value": [12.5, 6.7, 0.78]
        })
        st.dataframe(perf_df)
        st.plotly_chart(px.bar(perf_df, x="KPI", y="Value"))

    # -----------------------------
    # Tab 8: GenAI Recommendations
    # -----------------------------
    with tab8:
        st.subheader("📌 GenAI Recommendations")
        try:
            prompt = """
            You are a drilling safety advisor. Based on hazards like torque drift, high bit wear,
            abnormal logs, and seismic risks, provide 3 targeted safety recommendations.
            Each must include: ✅ Action, 🔍 Why, 📈 Expected Impact.
            """
            response = client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=800
            )
            st.info(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Azure OpenAI error: {str(e)}")

    # -----------------------------
    # Tab 9: GenAI Forecast
    # -----------------------------
    with tab9:
        st.subheader("🧠 GenAI Forecast")
        try:
            prompt = """
            Aggregate all operational risks (bit wear, torque drift, seismic faults, downtime).
            Provide a forecast across the next drilling phase, highlighting:
            - Top 3 most severe risks
            - Safety implications for crew
            - Recommended mitigations
            """
            response = client.chat.completions.create(
                model=DEPLOYMENT_NAME,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=800
            )
            st.info(response.choices[0].message.content)
        except Exception as e:
            st.error(f"Azure OpenAI error: {str(e)}")

    # -----------------------------
    # Tab 10: Ask a Query
    # -----------------------------
    with tab10:
        st.subheader("❓ Ask a Query")
        query = st.text_input("Enter your question:")
        if query:
            try:
                context = """
                You are a UK drilling safety assistant. Use simulated drilling, seismic,
                and hazard data to answer user questions clearly and technically.
                """
                prompt = f"{context}\n\nUser Question: {query}"
                response = client.chat.completions.create(
                    model=DEPLOYMENT_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.4,
                    max_tokens=800
                )
                st.success(response.choices[0].message.content)
            except Exception as e:
                st.error(f"Azure OpenAI error: {str(e)}")
