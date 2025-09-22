# uk_drilling_safety_assistant.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os, random
from datetime import datetime, timedelta
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
# Simulation Helpers
# -----------------------------
def simulate_seismic():
    now = datetime.now()
    timestamps = [now - timedelta(seconds=60*i) for i in range(30)]
    return pd.DataFrame({
        "Timestamp": timestamps,
        "Latitude": np.random.uniform(57.0, 57.5, 30),
        "Longitude": np.random.uniform(-1.5, -0.5, 30),
        "Amplitude": np.random.uniform(0.2, 0.8, 30),
        "Fault Risk": random.choices(["🟢", "🟡", "🔴"], weights=[1, 3, 6], k=30)
    })

def simulate_drilling_view():
    timestamps = pd.date_range(end=pd.Timestamp.now(), periods=50, freq="min")
    return pd.DataFrame({
        "Timestamp": timestamps,
        "Torque": np.random.uniform(300, 500, len(timestamps)),
        "ROP": np.random.uniform(10, 20, len(timestamps))
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

# -----------------------------
# Streamlit Layout
# -----------------------------
st.set_page_config(page_title="UK Oil & Gas Safety & Drilling Optimization Assistant", layout="wide")
main_tab, app_tab = st.tabs(["📘 Overview", "🛠️ Main App"])

with main_tab:
    st.title("📘 Overview: UK Oil & Gas Safety & Drilling Optimization Assistant")
    st.markdown("""
This assistant monitors drilling operations, forecasts risks, and provides GenAI-driven safety recommendations.  
Navigate through each tab for live simulations and hazard advisories.
""")

with app_tab:
    tabs = st.tabs([
        "🎛️ Real-Time Drilling View",
        "🪓 Bit Wear Monitoring",
        "💡 Auto Parameter Tuning",
        "🔥 Safety & Risk Prediction",
        "📈 Logs & Lithology Viewer",
        "🌍 Seismic Interpreter",
        "📊 Performance Dashboard",
        "📌 GenAI Recommendations",
        "🧠 GenAI Forecast",
        "❓ Ask a Query"
    ])

    # --------------------------------
    # Tab 1: Real-Time Drilling View
    # --------------------------------
    with tabs[0]:
        st.subheader("🎛️ Real-Time Drilling View")
        drilling_df = simulate_drilling_view()
        st.line_chart(drilling_df.set_index("Timestamp")[["Torque", "ROP"]])

        hazards = [
            {"Issue": "Torque/ROP Drift", "Severity": "🟡", "Risk": "Poor hole cleaning, stuck pipe"},
            {"Issue": "High Vibration", "Severity": "🔴", "Risk": "Fatigue of BHA, component failure"},
        ]
        st.session_state["drilling_hazards"] = hazards
        st.dataframe(pd.DataFrame(hazards))

    # --------------------------------
    # Tab 2: Bit Wear Monitoring
    # --------------------------------
    with tabs[1]:
        st.subheader("🪓 Bit Wear Monitoring")
        wear_df = simulate_bit_wear()
        st.line_chart(wear_df.set_index("Time"))

        hazards = [
            {"Issue": "High Bit Wear", "Severity": "🔴", "Risk": "Bit failure during drilling"},
            {"Issue": "Overpull Events", "Severity": "🟡", "Risk": "Pipe over-tension"}
        ]
        st.session_state["bit_hazards"] = hazards
        st.dataframe(pd.DataFrame(hazards))

    # --------------------------------
    # Tab 3: Auto Parameter Tuning
    # --------------------------------
    with tabs[2]:
        st.subheader("💡 Auto Parameter Tuning")
        drilling_df = simulate_drilling_view()
        st.line_chart(drilling_df.set_index("Timestamp")[["Torque", "ROP"]])

        hazards = [
            {"Issue": "Incorrect RPM", "Severity": "🟡", "Risk": "Potential BHA stress"},
            {"Issue": "Torque Instability", "Severity": "🔴", "Risk": "Unexpected stalls"}
        ]
        st.session_state["tuning_hazards"] = hazards
        st.dataframe(pd.DataFrame(hazards))

    # --------------------------------
    # Tab 4: Safety & Risk Prediction
    # --------------------------------
    with tabs[3]:
        st.subheader("🔥 Safety & Risk Prediction")
        perf_data = pd.DataFrame({
            "Metric": ["Drilling Speed", "Fuel Usage", "Downtime Hours"],
            "Value": [np.random.uniform(15, 25), np.random.uniform(1000, 2000), np.random.randint(2, 6)],
            "Unit": ["m/hr", "L/day", "hours"]
        })
        st.dataframe(perf_data)

        hazards = [
            {"Issue": "Excessive Downtime", "Severity": "🟡", "Risk": "Crew fatigue, accident potential"}
        ]
        st.session_state["safety_hazards"] = hazards
        st.dataframe(pd.DataFrame(hazards))

    # --------------------------------
    # Tab 5: Logs & Lithology Viewer
    # --------------------------------
    with tabs[4]:
        st.subheader("📈 Logs & Lithology Viewer")
        logs_df = simulate_logs()
        st.line_chart(logs_df.set_index("Depth (ft)")[["GR (API)", "NPHI (v/v)"]])

        hazards = [
            {"Issue": "Abnormal GR/NPHI Logs", "Severity": "🔴", "Risk": "Formation collapse risk"},
            {"Issue": "Shale Instability", "Severity": "🟡", "Risk": "Sloughing or swelling"}
        ]
        st.session_state["log_hazards"] = hazards
        st.dataframe(pd.DataFrame(hazards))

    # --------------------------------
    # Tab 6: Seismic Interpreter
    # --------------------------------
    with tabs[5]:
        st.subheader("🌍 Seismic Interpreter")
        seismic_df = simulate_seismic()
        st.scatter_chart(seismic_df, x="Longitude", y="Latitude", color="Fault Risk")

        hazards = [
            {"Issue": "Seismic Fault Zone", "Severity": "🔴", "Risk": "Formation influx risk"},
            {"Issue": "Pressure Contrast Zone", "Severity": "🔴", "Risk": "Kick / blowout risk"}
        ]
        st.session_state["seismic_hazards"] = hazards
        st.dataframe(pd.DataFrame(hazards))

    # --------------------------------
    # Tab 7: Performance Dashboard
    # --------------------------------
    with tabs[6]:
        st.subheader("📊 Performance Dashboard")
        perf_df = pd.DataFrame({
            "KPI": ["ROP Variance (%)", "NPT (%)", "Drilling Stability Index"],
            "Value": [12.5, 6.7, 0.78]
        })
        st.bar_chart(perf_df.set_index("KPI"))

        hazards = [
            {"Issue": "ROP Variance High", "Severity": "🟡", "Risk": "Potential stuck pipe"},
        ]
        st.session_state["perf_hazards"] = hazards
        st.dataframe(pd.DataFrame(hazards))

    # --------------------------------
    # Tab 8: 📌 GenAI Recommendations
    # --------------------------------
    with tabs[7]:
        st.subheader("📌 GenAI Recommendations")
        all_hazards = sum([st.session_state.get(k, []) for k in st.session_state.keys() if "hazards" in k], [])
        if not all_hazards:
            st.warning("⚠️ No hazards collected yet.")
        else:
            hazard_text = "\n".join([f"- {h['Issue']} ({h['Severity']}) → {h['Risk']}" for h in all_hazards])
            prompt = f"""
You are a drilling safety advisor. Given these identified hazards:

{hazard_text}

Provide 3 concrete safety recommendations:
- ✅ Action
- 🔍 Why
- 📈 Expected Impact
"""
            with st.spinner("Generating recommendations..."):
                try:
                    resp = client.chat.completions.create(
                        model=DEPLOYMENT_NAME,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=600
                    )
                    st.success(resp.choices[0].message.content.strip())
                except Exception as e:
                    st.error(f"GenAI failed: {e}")

    # --------------------------------
    # Tab 9: 🧠 GenAI Forecast
    # --------------------------------
    with tabs[8]:
        st.subheader("🧠 GenAI Forecast")
        all_hazards = sum([st.session_state.get(k, []) for k in st.session_state.keys() if "hazards" in k], [])
        hazard_text = "\n".join([f"- {h['Issue']} ({h['Severity']}) → {h['Risk']}" for h in all_hazards]) or "No hazards logged."
        prompt = f"""
You are a drilling safety forecaster. Based on hazards:

{hazard_text}

Summarize overall worker safety and highlight the top 3 risks to focus on in the next 12 hours.
"""
        with st.spinner("Forecasting..."):
            try:
                resp = client.chat.completions.create(
                    model=DEPLOYMENT_NAME,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500
                )
                st.info(resp.choices[0].message.content.strip())
            except Exception as e:
                st.error(f"GenAI failed: {e}")

    # --------------------------------
    # Tab 10: ❓ Ask a Query
    # --------------------------------
    with tabs[9]:
        st.subheader("❓ Ask a Query")
        q = st.text_input("Enter your question:")
        if q:
            all_hazards = sum([st.session_state.get(k, []) for k in st.session_state.keys() if "hazards" in k], [])
            hazard_text = "\n".join([f"- {h['Issue']} ({h['Severity']}) → {h['Risk']}" for h in all_hazards]) or "No hazards identified."
            prompt = f"""
User question: "{q}"

Here are current hazards:
{hazard_text}

Answer the question with reference to these hazards and overall worker safety.
"""
            with st.spinner("Thinking..."):
                try:
                    resp = client.chat.completions.create(
                        model=DEPLOYMENT_NAME,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=500
                    )
                    st.info(resp.choices[0].message.content.strip())
                except Exception as e:
                    st.error(f"GenAI failed: {e}")
