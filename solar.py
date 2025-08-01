import streamlit as st
import pandas as pd
import random
from datetime import datetime
import matplotlib.pyplot as plt

# Simulate solar panel data
def generate_data():
    voltage = round(random.uniform(16.0, 22.0), 2)
    current = round(random.uniform(2.0, 5.0), 2)
    power = round(voltage * current, 2)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"Timestamp": timestamp, "Voltage (V)": voltage, "Current (A)": current, "Power (W)": power}

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Timestamp", "Voltage (V)", "Current (A)", "Power (W)"])

# Streamlit UI
st.title("🔆 Solar IoT Energy Monitoring Dashboard")
st.markdown("Simulated real-time solar panel readings.")

if st.button("Generate New Data"):
    new_data = generate_data()
    st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([new_data])], ignore_index=True)

# Show recent data
st.subheader("Latest Readings")
st.dataframe(st.session_state.data.tail(5))

# Plot power data
if not st.session_state.data.empty:
    st.subheader("📈 Power Output Over Time")
    fig, ax = plt.subplots(figsize=(10, 4))
    st.session_state.data["Timestamp"] = pd.to_datetime(st.session_state.data["Timestamp"])
    ax.plot(st.session_state.data["Timestamp"], st.session_state.data["Power (W)"], marker='o')
    ax.set_xlabel("Time")
    ax.set_ylabel("Power (W)")
    ax.set_title("Solar Power Output")
    ax.grid(True)
    st.pyplot(fig)