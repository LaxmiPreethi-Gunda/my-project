import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ------------------- CONFIG -------------------
st.set_page_config(page_title="Household Energy ML Dashboard", page_icon="⚡", layout="wide")
st.title("⚡ Household Energy ML Dashboard")

# Sidebar navigation
page = st.sidebar.radio("Navigate", ["🏠 Home", "📊 Insights & ML"])

# ------------------- FILE UPLOAD -------------------
uploaded_file = st.sidebar.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    # Read file
    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)

    # ------------------- HOME PAGE -------------------
    if page == "🏠 Home":
        st.subheader("Dataset Preview")
        st.dataframe(df.head(), use_container_width=True)

        st.write(f"*Rows:* {df.shape[0]} | *Columns:* {df.shape[1]}")
        st.write("### Summary Statistics")
        st.write(df.describe())

    # ------------------- INSIGHTS & ML PAGE -------------------
    else:
        st.subheader("Data Insights")
        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()

        if len(numeric_cols) < 2:
            st.error("Dataset must have at least 2 numeric columns for visualization and ML.")
        else:
            # Scatter Plot
            x_axis = st.selectbox("X-axis", numeric_cols, index=0)
            y_axis = st.selectbox("Y-axis", numeric_cols, index=1)
            fig1 = px.scatter(df, x=x_axis, y=y_axis, title=f"{x_axis} vs {y_axis}")
            st.plotly_chart(fig1, use_container_width=True)

            # ------------------- MACHINE LEARNING MODEL -------------------
            if "Monthly_Energy_Consumption_kWh" in df.columns:
                # Create a binary target: High consumption > mean
                mean_consumption = df["Monthly_Energy_Consumption_kWh"].mean()
                df["High_Consumption"] = (df["Monthly_Energy_Consumption_kWh"] > mean_consumption).astype(int)

                # Select features (exclude target & IDs)
                feature_cols = [col for col in numeric_cols if col not in ["Monthly_Energy_Consumption_kWh"]]
                X = df[feature_cols]
                y = df["High_Consumption"]

                # Train/test split
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model = RandomForestClassifier(n_estimators=100, random_state=42)
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                acc = accuracy_score(y_test, y_pred)
                st.success(f"ML Model Trained (RandomForest) | Accuracy: {acc:.2%}")

                # Predict for all rows
                df["Predicted_High_Consumption"] = model.predict(X)

                # Show updated dataset
                st.subheader("Predictions")
                st.dataframe(df[["Monthly_Energy_Consumption_kWh", "High_Consumption", "Predicted_High_Consumption"]].head(10), use_container_width=True)

                # Download predictions
                st.download_button(
                    label="Download Predictions",
                    data=df.to_csv(index=False),
                    file_name="energy_predictions.csv",
                    mime="text/csv"
                )
            else:
                st.warning("Column 'Monthly_Energy_Consumption_kWh' not found. Add it to use ML model.")

else:
    st.info("👆 Upload a CSV or Excel file from the sidebar to begin.")

# Footer
st.markdown("---")
st.markdown("Built with ❤ using *Streamlit + Plotly + Scikit-Learn*")