import os
import random
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import datetime, timedelta
from openai import AzureOpenAI
from dotenv import load_dotenv

# ==============================
# Azure OpenAI Setup
# ==============================
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-raj")

# ==============================
# Session State Setup
# ==============================
if "all_hazards" not in st.session_state:
    st.session_state.all_hazards = []

# ==============================
# Data Simulation Helpers
# ==============================
def simulate_seismic():
    now = datetime.now()
    timestamps = [now - timedelta(seconds=60 * i) for i in range(30)]
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

# ==============================
# Streamlit Layout
# ==============================
st.set_page_config(page_title="UK Oil & Gas Safety & Drilling Optimization Assistant", layout="wide")
main_tab, app_tab = st.tabs(["📘 Overview", "🛠️ Main App"])

# ==============================
# Overview Tab
# ==============================
with main_tab:
    st.title("📘 Overview: UK Oil & Gas Safety & Drilling Optimization Assistant")
    st.markdown("""
Welcome to the **UK Drilling Safety Assistant** – a GenAI-powered dashboard to monitor and enhance the safety of oil & gas drilling operations.

This prototype simulates conditions in a large-scale UK drilling operation and provides insights on safety risks and mitigation steps.

Navigate the tabs to explore live hazards and ask GenAI about worker safety.
    """)

# ==============================
# Main App Tabs
# ==============================
with app_tab:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
        "🎛️ Real-Time Drilling View", "🪓 Bit Wear Monitoring", "💡 Auto Parameter Tuning",
        "🔥 Safety & Risk Prediction", "📈 Logs & Lithology Viewer", "🌍 Seismic Interpreter",
        "📊 Performance Dashboard", "📌 GenAI Recommendations", "🧠 GenAI Forecast", "❓ Ask a Query"
    ])

    # ------------------------------
    # Tab 1 - Drilling View
    # ------------------------------
    with tab1:
        st.subheader("🎛️ Real-Time Drilling View")
        drilling_df = simulate_drilling_view()
        st.dataframe(drilling_df)
        fig = px.line(drilling_df, x="Timestamp", y=["Torque", "ROP"], title="Torque and ROP Trends")
        st.plotly_chart(fig, use_container_width=True)

        drilling_view_table = pd.DataFrame({
            "Issue": ["Torque/ROP Drift", "High Vibration"],
            "Operational Hazard": ["Poor hole cleaning, stuck pipe", "Fatigue of BHA, component failure"],
            "Employee Safety Risk": ["Unexpected pipe trip, injury risk", "Tool detachment, flying debris"],
            "Severity": ["🟡", "🔴"],
            "Mitigation Step": ["Optimize cleaning schedule", "Use vibration dampeners"]
        })
        st.dataframe(drilling_view_table, use_container_width=True)

        for _, row in drilling_view_table.iterrows():
            st.session_state.all_hazards.append(f"{row['Issue']} ({row['Severity']}) - {row['Operational Hazard']}")

    # ------------------------------
    # Tab 2 - Bit Wear
    # ------------------------------
    with tab2:
        st.subheader("🪓 Bit Wear Monitoring")
        wear_df = simulate_bit_wear()
        st.line_chart(wear_df.set_index("Time"))
        bit_wear_table = pd.DataFrame({
            "Issue": ["High Bit Wear", "Overpull Events"],
            "Operational Hazard": ["Bit failure", "Pipe over-tension"],
            "Employee Safety Risk": ["Flying debris", "Whiplash injuries"],
            "Severity": ["🔴", "🟡"],
            "Mitigation Step": ["Replace bit early", "Controlled tripping speeds"]
        })
        st.dataframe(bit_wear_table, use_container_width=True)

        for _, row in bit_wear_table.iterrows():
            st.session_state.all_hazards.append(f"{row['Issue']} ({row['Severity']}) - {row['Operational Hazard']}")

    # ------------------------------
    # Tab 3 - Auto Parameter Tuning
    # ------------------------------
    with tab3:
        st.subheader("💡 Auto Parameter Tuning")
        drilling_df = simulate_drilling_view()
        st.line_chart(drilling_df.set_index("Timestamp"))
        tuning_table = pd.DataFrame({
            "Issue": ["Torque/ROP Drift", "High Vibration"],
            "Operational Hazard": ["Poor hole cleaning", "Component fatigue"],
            "Employee Safety Risk": ["Stuck pipe", "Flying debris"],
            "Severity": ["🟡", "🔴"],
            "Mitigation Step": ["Optimize cleaning schedule", "Dampeners"]
        })
        st.dataframe(tuning_table, use_container_width=True)

        for _, row in tuning_table.iterrows():
            st.session_state.all_hazards.append(f"{row['Issue']} ({row['Severity']}) - {row['Operational Hazard']}")

    # ------------------------------
    # Tab 4 - Safety Prediction
    # ------------------------------
    with tab4:
        st.subheader("🔥 Safety & Risk Prediction")
        risk_table = pd.DataFrame({
            "Issue": ["Excessive Downtime"],
            "Operational Hazard": ["Crew fatigue"],
            "Employee Safety Risk": ["Accidents from exhaustion"],
            "Severity": ["🟡"],
            "Mitigation Step": ["Shift rotation"]
        })
        st.dataframe(risk_table)

        for _, row in risk_table.iterrows():
            st.session_state.all_hazards.append(f"{row['Issue']} ({row['Severity']}) - {row['Operational Hazard']}")

    # ------------------------------
    # Tab 5 - Logs Viewer
    # ------------------------------
    with tab5:
        st.subheader("📈 Logs & Lithology Viewer")
        logs_df = simulate_logs()
        st.line_chart(logs_df.set_index("Depth (ft)"))
        logs_table = pd.DataFrame({
            "Issue": ["Shale Instability"],
            "Operational Hazard": ["Formation collapse"],
            "Employee Safety Risk": ["Rig instability"],
            "Severity": ["🔴"],
            "Mitigation Step": ["Stabilizers"]
        })
        st.dataframe(logs_table)

        for _, row in logs_table.iterrows():
            st.session_state.all_hazards.append(f"{row['Issue']} ({row['Severity']}) - {row['Operational Hazard']}")

    # ------------------------------
    # Tab 6 - Seismic
    # ------------------------------
    with tab6:
        st.subheader("🌍 Seismic Interpreter")
        seismic_df = simulate_seismic()
        st.scatter_chart(seismic_df, x="Longitude", y="Latitude", color="Fault Risk")
        seismic_table = pd.DataFrame({
            "Issue": ["Seismic Fault Zone"],
            "Operational Hazard": ["Casing collapse"],
            "Employee Safety Risk": ["Explosion"],
            "Severity": ["🔴"],
            "Mitigation Step": ["Pre-check seismic"]
        })
        st.dataframe(seismic_table)

        for _, row in seismic_table.iterrows():
            st.session_state.all_hazards.append(f"{row['Issue']} ({row['Severity']}) - {row['Operational Hazard']}")

    # ------------------------------
    # Tab 7 - Dashboard
    # ------------------------------
    with tab7:
        st.subheader("📊 Performance Dashboard")
        perf_table = pd.DataFrame({
            "Issue": ["ROP Variance"],
            "Operational Hazard": ["Hole cleaning issues"],
            "Employee Safety Risk": ["Stuck pipe risk"],
            "Severity": ["🟡"],
            "Mitigation Step": ["Monitor ROP"]
        })
        st.dataframe(perf_table)

        for _, row in perf_table.iterrows():
            st.session_state.all_hazards.append(f"{row['Issue']} ({row['Severity']}) - {row['Operational Hazard']}")

    # ------------------------------
    # Tab 8 - Recommendations
    # ------------------------------
    with tab8:
        st.subheader("📌 GenAI Recommendations")
        st.info("This tab will show recommendations in future versions.")

    # ------------------------------
    # Tab 9 - Forecast
    # ------------------------------
    with tab9:
        st.subheader("🧠 GenAI Forecast")
        st.info("This tab aggregates hazards (see Ask a Query).")

    # ------------------------------
    # Tab 10 - Ask a Query
    # ------------------------------
    with tab10:
        st.subheader("❓ Ask a Query")
        query = st.text_input("Enter your question:")

        if query:
            hazard_summary = "\n".join(st.session_state.all_hazards[:50])

            prompt = f"""
You are a drilling safety assistant. Hazards detected so far:

{hazard_summary}

User Question: {query}

Answer clearly:
- Is worker safety acceptable overall? (Safe / Unsafe)
- Justify based on hazard severities.
- Provide 3 concrete safety recommendations.
"""
            with st.spinner("Analyzing with Azure OpenAI..."):
                try:
                    response = client.chat.completions.create(
                        model=DEPLOYMENT_NAME,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3,
                        max_tokens=700,
                    )
                    st.markdown("### 🧠 GenAI Safety Assessment")
                    st.success(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"GenAI error: {e}")
