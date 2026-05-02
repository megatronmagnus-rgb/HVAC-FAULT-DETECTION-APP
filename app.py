import streamlit as st
import numpy as np
import pandas as pd
import joblib
import os

# ---------- CONFIG ----------
st.set_page_config(page_title="HVAC Fault Detection", layout="centered")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- LOAD MODELS (FIXED NAME ONLY) ----------
model_path = os.path.join(BASE_DIR, "..", "model", "ac_fault_model.pkl")
encoder_path = os.path.join(BASE_DIR, "..", "model", "label_encoder.pkl")
features_path = os.path.join(BASE_DIR, "..", "model", "features.pkl")

model = joblib.load(model_path)
encoder = joblib.load(encoder_path)
features = joblib.load(features_path)

# ---------- UI ----------
st.title("HVAC Fault Detection System")
st.markdown("Enter sensor readings:")

col1, col2 = st.columns(2)

with col1:
    T1 = st.number_input("T1 (Compressor Inlet)", value=25.0)
    T2 = st.number_input("T2 (Compressor Outlet)", value=30.0)
    T3 = st.number_input("T3 (After Condenser)", value=0.0)
    T4 = st.number_input("T4 (After Expansion Valve)", value=0.0)
    T5 = st.number_input("T5 (Fresh Air Inlet)", value=0.0)

with col2:
    T6 = st.number_input("T6 (Evaporator Inlet Air)", value=0.0)
    T7 = st.number_input("T7 (Evaporator Outlet Air)", value=0.0)
    T8 = st.number_input("T8 (Chamber Temp)", value=25.0)
    Power = st.number_input("Compressor Power (kW)", value=2.0)

# ---------- ENGINEERED FEATURES ----------
temp_diff = T2 - T1
pressure_diff = T7 - T6
efficiency = temp_diff / (T1 + 1e-6)
thermal_load = temp_diff * Power

# ---------- INPUT DICTIONARY ----------
input_dict = {
    "T1": T1,
    "T2": T2,
    "T3": T3,
    "T4": T4,
    "T5": T5,
    "T6": T6,
    "T7": T7,
    "T8": T8,
    "Power": Power,
    "temp_diff": temp_diff,
    "efficiency": efficiency,
    "thermal_load": thermal_load,
    "pressure_diff": pressure_diff
}

# enforce training order
input_data = pd.DataFrame([input_dict])[features]

# ---------- PREDICTION ----------
if st.button("Predict Fault"):

    pred = model.predict(input_data)[0]
    fault_name = encoder.inverse_transform([pred])[0]

    confidence = model.predict_proba(input_data).max() * 100

    # ---------- INTERPRETATION ----------
    reasons = []

    if temp_diff > 8:
        reasons.append("High compressor temperature rise → compressor stress")

    if pressure_diff > 5:
        reasons.append("Airflow imbalance in evaporator system")

    if efficiency < 0.6:
        reasons.append("Low efficiency → system underperforming")

    if Power > 3 and temp_diff < 5:
        reasons.append("High power with low cooling → inefficiency")

    # ---------- OUTPUT ----------
    st.subheader("Result")

    st.success(f"Detected Fault: {fault_name}")
    st.info(f"Confidence: {round(confidence, 2)}%")

    st.subheader("Interpretation")

    if reasons:
        for r in reasons:
            st.write("•", r)
    else:
        st.write("System operating normally or within expected range")