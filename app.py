import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# ---------- CLEAN WHITE UI ----------
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
    color: #1f2d3d;
}

.section-title {
    font-size: 18px;
    font-weight: 600;
    color: #1f2d3d;
    margin-bottom: 8px;
}

.card {
    background: #ffffff;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #e6e6e6;
    margin-bottom: 10px;
}

.interpret-box {
    background: #ffffff;
    color: #1f2d3d;
    padding: 18px;
    border-radius: 10px;
    border-left: 4px solid #2a7de1;
    font-size: 15px;
    line-height: 1.6;
}

.stButton>button {
    background-color: #2a7de1;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("HVAC Fault Detection System")

# ---------- INPUT ----------
st.subheader("System Inputs")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Air Side")
    T1 = st.number_input("Inlet Temp (°C)", value=26.0)
    T2 = st.number_input("Outlet Temp (°C)", value=16.0)

with col2:
    st.markdown("#### Refrigeration")
    T3 = st.number_input("Evaporator Temp (°C)", value=10.0)
    T4 = st.number_input("Condenser Temp (°C)", value=45.0)
    T7 = st.number_input("Ambient Temp (°C)", value=35.0)

with col3:
    st.markdown("#### Compressor")
    T5 = st.number_input("Suction Temp (°C)", value=8.0)
    T6 = st.number_input("Discharge Temp (°C)", value=60.0)
    power = st.number_input("Power (kW)", value=1.5)

# ---------- BUTTON ----------
if st.button("Analyze System"):

    delta_T = T1 - T2
    cond_eff = T4 - T7
    comp_stress = T6 - T5

    # Prediction
    if power > 4:
        prediction = "Compressor Fault"
    elif delta_T < 5:
        prediction = "Evaporator Fault"
    elif cond_eff > 15:
        prediction = "Condenser Fault"
    elif comp_stress > 50:
        prediction = "Refrigerant Issue"
    else:
        prediction = "Normal"

    # ---------- RESULTS ----------
    st.subheader("System Summary")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Cooling ΔT", f"{delta_T:.2f} °C")
    c2.metric("Cond ΔT", f"{cond_eff:.2f} °C")
    c3.metric("Comp Stress", f"{comp_stress:.2f}")
    c4.metric("Prediction", prediction)

    # ---------- HEALTH ----------
    health = max(0, 100 - (power*10 + abs(delta_T-10)*5))

    st.subheader("System Health")
    st.progress(int(health))
    st.write(f"Health Score: {health:.2f}%")

    # ---------- HEALTH REASON ----------
    st.subheader("Health Explanation")

    if health > 80:
        st.write("• System operating near optimal conditions")
    if delta_T < 5:
        st.write("• Low cooling performance reduced score")
    if power > 4:
        st.write("• High compressor load reduced efficiency")
    if cond_eff > 15:
        st.write("• Poor heat rejection affected system")
    if comp_stress > 50:
        st.write("• Compressor stress is too high")

    # ---------- INTERPRETATION ----------
    st.subheader("System Interpretation")

    if prediction == "Normal":
        text = """
System is operating within normal limits.
Cooling performance and compressor load are balanced.
Heat exchange is efficient across system components.
No fault condition detected.
"""

    elif prediction == "Compressor Fault":
        text = """
Compressor is consuming excessive power indicating overload.
Possible mechanical wear or pressure imbalance.
Continuous use may damage compressor.
Inspection is recommended.
"""

    elif prediction == "Evaporator Fault":
        text = """
Cooling difference is too low indicating weak heat absorption.
Possible refrigerant shortage or airflow issue.
Cooling efficiency is reduced.
Evaporator needs inspection.
"""

    elif prediction == "Condenser Fault":
        text = """
Condenser temperature is high compared to ambient.
Heat rejection is inefficient.
Likely due to dirty coils or airflow restriction.
Cleaning is required.
"""

    else:
        text = """
Compressor temperature variation is too high.
Indicates refrigerant imbalance.
System performance is unstable.
Refrigerant check is needed.
"""

    st.markdown(f'<div class="interpret-box">{text}</div>', unsafe_allow_html=True)