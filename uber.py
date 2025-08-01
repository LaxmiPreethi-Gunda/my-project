import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import random

# Function to simulate GPS data for vehicles
def generate_vehicle_data(n=10):
    vehicles = []
    for i in range(n):
        lat = 12.9716 + random.uniform(-0.02, 0.02)  # Bengaluru base location
        lon = 77.5946 + random.uniform(-0.02, 0.02)
        vehicles.append({
            "Vehicle ID": f"UBER-{i+1}",
            "Latitude": round(lat, 6),
            "Longitude": round(lon, 6),
            "Speed (km/h)": round(random.uniform(20, 60), 2)
        })
    return pd.DataFrame(vehicles)

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🚗 Uber IoT Vehicle Tracking Dashboard")
st.markdown("Simulated real-time vehicle location + speed tracking")

# Generate and show vehicle data
df = generate_vehicle_data(15)

# Create Folium map
center = [df['Latitude'].mean(), df['Longitude'].mean()]
m = folium.Map(location=center, zoom_start=13)

# Add vehicle markers
for _, row in df.iterrows():
    popup = f"{row['Vehicle ID']}<br>Speed: {row['Speed (km/h)']} km/h"
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=popup,
        icon=folium.Icon(color="blue", icon="car", prefix="fa")
    ).add_to(m)

# Show map
st_folium(m, width=1000, height=500)

# Show vehicle data table
st.subheader("📋 Vehicle Data")
st.dataframe(df)