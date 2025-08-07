import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random

# Streamlit Page Setup
st.set_page_config(page_title="Telangana Clothes Demand & Supply", layout="wide")
st.title("📊 Telangana Clothes Demand & Supply Dashboard")

# Step 1: Simulate Dataset
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
regions = ['Hyderabad', 'Warangal', 'Karimnagar', 'Nizamabad', 'Khammam']
categories = ['Men', 'Women', 'Kids']

data = []
for month in months:
    for region in regions:
        for category in categories:
            demand = random.randint(500, 2000)
            supply = random.randint(400, 2200)
            data.append([month, region, category, demand, supply])

df = pd.DataFrame(data, columns=['Month', 'Region', 'Category', 'Demand', 'Supply'])
df['Gap'] = df['Demand'] - df['Supply']

# Step 2: Aggregations
monthly = df.groupby('Month')[['Demand', 'Supply']].sum().reindex(months)
monthly_gap = df.groupby('Month')['Gap'].sum().reindex(months)
category_share = df.groupby('Category')['Demand'].sum()

# Sidebar Filters
st.sidebar.header("🔍 Filters")
selected_category = st.sidebar.multiselect("Select Category", categories, default=categories)
selected_region = st.sidebar.multiselect("Select Region", regions, default=regions)

# Filtered Data
filtered_df = df[df['Category'].isin(selected_category) & df['Region'].isin(selected_region)]

# Step 3: Dataset Display
st.subheader("📋 Full Dataset (Filtered)")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# Step 4: Regional Summary Table
st.subheader("📍 Region-wise Summary")
region_summary = filtered_df.groupby('Region')[['Demand', 'Supply', 'Gap']].sum().sort_values(by='Demand', ascending=False)
st.dataframe(region_summary, use_container_width=True)

# Step 5: Charts
st.subheader("📦 Monthly Total Demand vs Supply")
fig1, ax1 = plt.subplots(figsize=(10,5))
monthly.plot(kind='bar', ax=ax1)
ax1.set_ylabel("Units")
ax1.set_title("Monthly Total Demand vs Supply")
st.pyplot(fig1)

st.subheader("📈 Monthly Demand by Category")
fig2, ax2 = plt.subplots(figsize=(10,5))
sns.lineplot(data=filtered_df, x='Month', y='Demand', hue='Category', estimator='sum', ax=ax2)
ax2.set_title("Monthly Demand by Category")
st.pyplot(fig2)

st.subheader("🌐 Heatmap of Demand per Region per Month")
heatmap_data = df.pivot_table(index='Region', columns='Month', values='Demand', aggfunc='sum')
fig3, ax3 = plt.subplots(figsize=(8,5))
sns.heatmap(heatmap_data, cmap='Blues', annot=True, fmt=".0f", ax=ax3)
st.pyplot(fig3)

st.subheader("🧵 Demand Share by Category")
fig4, ax4 = plt.subplots()
category_share.plot.pie(autopct='%1.1f%%', startangle=90, ax=ax4)
ax4.set_ylabel('')
ax4.set_title("Demand Share by Category")
st.pyplot(fig4)

st.subheader("⚖ Demand-Supply Gap by Month")
fig5, ax5 = plt.subplots(figsize=(10,4))
monthly_gap.plot(kind='line', marker='o', ax=ax5)
ax5.set_title("Monthly Demand-Supply Gap")
ax5.set_ylabel("Gap (Units)")
st.pyplot(fig5)

st.subheader("📦 Supply Distribution by Region")
fig6, ax6 = plt.subplots(figsize=(10,5))
sns.boxplot(data=df, x='Region', y='Supply', ax=ax6)
ax6.set_title("Supply Distribution by Region")
st.pyplot(fig6)

# Step 6: Insights
st.subheader("📌 Insights")
peak_month = monthly['Demand'].idxmax()
top_region = df.groupby('Region')['Supply'].sum().idxmax()
worst_gap_month = monthly_gap.idxmax()

st.markdown(f"✅ Peak Demand Month: {peak_month}")
st.markdown(f"🏭 Region with Highest Supply: {top_region}")
st.markdown(f"⚠ Month with Highest Demand-Supply Gap: {worst_gap_month}")