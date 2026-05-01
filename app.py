import streamlit as st
import numpy as np
import pickle
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# ---------- LOAD MODEL ----------
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# ---------- UI STYLE ----------
st.markdown("""
<style>
body {
    background-color: white;
}
.block-container {
    padding-top: 1rem;
}
h1 {
    text-align: center;
    color: #0b3d91;
}
.input-box {
    background-color: #e6f0ff;
    padding: 20px;
    border-radius: 12px;
}
.result-box {
    background-color: #f0f7ff;
    padding: 20px;
    border-radius: 12px;
    border-left: 6px solid #0b3d91;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("HVAC Fault Detection System")

# ---------- INPUT SECTION ----------
st.subheader("Enter System Parameters")

col1, col2 = st.columns(2)

with col1:
    inlet = st.number_input("Inlet Temp (°C)", value=24.0)
    outlet = st.number_input("Outlet Temp (°C)", value=16.0)
    coil = st.number_input("Cooling Coil Temp (°C)", value=10.0)
    ambient = st.number_input("Ambient Temp (°C)", value=30.0)

with col2:
    exhaust = st.number_input("Exhaust Temp (°C)", value=45.0)
    suction = st.number_input("Suction Temp (°C)", value=8.0)
    discharge = st.number_input("Discharge Temp (°C)", value=60.0)
    power = st.number_input("Compressor Power (kW)", value=1.2)

# ---------- ANALYZE BUTTON ----------
if st.button("Analyze System"):

    input_data = np.array([[inlet, outlet, coil, ambient,
                            exhaust, suction, discharge, power]])

    # ---------- MODEL PREDICTION ----------
    prediction = model.predict(input_data)[0]

    try:
        prob = model.predict_proba(input_data)[0][1]
    except:
        prob = 0.5  # fallback

    # ---------- HEALTH SCORE ----------
    health_score = int((1 - prob) * 100)

    # ---------- RESULT ----------
    st.subheader("System Result")

    colA, colB, colC = st.columns(3)

    with colA:
        if prediction == 0:
            st.success("Healthy")
        else:
            st.error("Fault Detected")

    with colB:
        st.metric("Fault Probability", f"{prob*100:.1f}%")

    with colC:
        st.metric("Health Score", f"{health_score}/100")

    # ---------- GRAPH ----------
    st.subheader("Temperature Profile")

    temps = [inlet, outlet, coil, ambient, exhaust, suction, discharge]
    labels = ["Inlet", "Outlet", "Coil", "Ambient", "Exhaust", "Suction", "Discharge"]

    fig, ax = plt.subplots()
    ax.plot(labels, temps, marker='o')
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("HVAC Temperature Distribution")

    st.pyplot(fig)

    # ---------- INTERPRETATION ----------
    st.subheader("System Interpretation")

    temp_diff = inlet - outlet

    if prediction == 0:
        reason = "System is operating within normal thermal and power ranges."
    else:
        if power > 1.5:
            reason = "High compressor load indicates possible mechanical stress or overcooling demand."
        elif temp_diff < 5:
            reason = "Low cooling difference suggests inefficient heat exchange."
        elif discharge > 70:
            reason = "High discharge temperature indicates overheating."
        else:
            reason = "General inefficiency detected in system performance."

    st.markdown(f"""
    <div class="result-box">
    <b>Analysis Summary:</b><br><br>
    • Cooling Difference: {temp_diff:.2f} °C<br>
    • Compressor Load: {power} kW<br>
    • Fault Probability: {prob*100:.1f}%<br><br>
    <b>Reason:</b><br>
    {reason}
    </div>
    """, unsafe_allow_html=True)

# ---------- FOOTER ----------
st.caption("Final Year Project | HVAC Fault Detection using Machine Learning")