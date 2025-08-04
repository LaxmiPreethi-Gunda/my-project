import streamlit as st
import matplotlib.pyplot as plt

# Title
st.title("📊 Classroom Power Consumption Estimator")

# User input for custom fan wattage
st.sidebar.header("⚙ Customize Your Fan")
custom_fan_wattage = st.sidebar.number_input("Enter your fan's wattage (W)", min_value=75, max_value=90, value=75)


# Appliance data
appliances = {
    "Fan": {"quantity": 6, "power_watts": custom_fan_wattage},
    "Tube Light": {"quantity": 7, "power_watts": 40},
    "Projector": {"quantity": 1, "power_watts": 300},
    "Laptop Charging Socket": {"quantity": 8, "power_watts": 65}
}

# Constants
usage_hours_per_day = 6
electricity_cost_per_unit = 6  # ₹ per unit (1 kWh)
days_per_month = 30

# Appliance Usage Summary
st.subheader("Appliance Usage Summary")
total_energy_kwh_per_day = 0
total_cost_per_day = 0

# For chart data
appliance_names = []
daily_energy_values = []

for appliance, info in appliances.items():
    quantity = info["quantity"]
    power_watts = info["power_watts"]
    energy_kwh = (quantity * power_watts * usage_hours_per_day) / 1000
    cost = energy_kwh * electricity_cost_per_unit

    total_energy_kwh_per_day += energy_kwh
    total_cost_per_day += cost

    appliance_names.append(appliance)
    daily_energy_values.append(energy_kwh)

    st.markdown(f"{appliance}: {quantity} × {power_watts}W × {usage_hours_per_day}h = {energy_kwh:.2f} kWh → ₹{cost:.2f}")

# Monthly calculations
total_energy_kwh_per_month = total_energy_kwh_per_day * days_per_month
total_cost_per_month = total_cost_per_day * days_per_month

# Total Summary
st.markdown("---")
st.success(f"🔋 Total Energy Consumed per Day: {total_energy_kwh_per_day:.2f} kWh")
st.success(f"💰 Total Cost per Day: ₹{total_cost_per_day:.2f}")
st.info(f"📅 Monthly Energy Consumption: {total_energy_kwh_per_month:.2f} kWh")
st.info(f"💸 Monthly Cost: ₹{total_cost_per_month:.2f}")

# 📈 Bar Chart: Daily Energy Consumption per Appliance
st.markdown("### 📉 Daily Energy Consumption by Appliance")

fig, ax = plt.subplots()
bars = ax.bar(appliance_names, daily_energy_values, color='skyblue')
ax.set_ylabel('Energy (kWh)')
ax.set_title('Daily Energy Consumption per Appliance')
ax.bar_label(bars, fmt='%.2f')
st.pyplot(fig)

# Detailed Custom Fan Calculation
st.markdown("### 🧮 Custom Fan Power Usage Analysis")

fan_power = custom_fan_wattage
fan_hours_per_day = 6

# Fan Calculations
fan_per_hour_kwh = (fan_power * 1) / 1000
fan_per_day_kwh = (fan_power * fan_hours_per_day) / 1000
fan_per_week_kwh = (fan_power * fan_hours_per_day * 7) / 1000
fan_per_month_kwh = (fan_power * fan_hours_per_day * days_per_month) / 1000

# Fan Costs
cost_per_hour = fan_per_hour_kwh * electricity_cost_per_unit
cost_per_day = fan_per_day_kwh * electricity_cost_per_unit
cost_per_week = fan_per_week_kwh * electricity_cost_per_unit
cost_per_month = fan_per_month_kwh * electricity_cost_per_unit

# Fan Display
st.info(f"🔌 Fan Wattage: {fan_power}W")
st.markdown(f"- Per Hour: {fan_per_hour_kwh:.3f} kWh → ₹{cost_per_hour:.2f}")
st.markdown(f"- Per Day (6h): {fan_per_day_kwh:.3f} kWh → ₹{cost_per_day:.2f}")
st.markdown(f"- Per Week (6h/day): {fan_per_week_kwh:.3f} kWh → ₹{cost_per_week:.2f}")
st.markdown(f"- Per Month (6h/day): {fan_per_month_kwh:.3f} kWh → ₹{cost_per_month:.2f}")