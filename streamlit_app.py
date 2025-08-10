import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
import os

# ===== CONFIG =====
# Change this to your local Google Drive folder path
# Example for Windows with Google Drive for Desktop:
GOOGLE_DRIVE_FOLDER = r"G:\My Drive\Zapier Watch"

st.title("Energy AI Dashboard")

# File uploader
uploaded = st.file_uploader("Upload Energy Data (CSV)", type=["csv"])

if uploaded:
    # Load data
    df = pd.read_csv(uploaded)

    # Ensure date is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    # Show basic chart
    st.subheader("Energy Output Over Time")
    st.line_chart(df['output_kwh'])

    # Run anomaly detection
    model = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly'] = model.fit_predict(df[['output_kwh']]) == -1
    anomalies = df[df['anomaly'] == True]

    # Show summary (mock for now)
    st.subheader("Weekly Summary")
    st.markdown("**Anomalies detected on June 5 and 9.**")

    # Plot anomalies on chart
    st.subheader("Energy Output with Anomalies")
    fig, ax = plt.subplots()
    ax.plot(df["date"], df["output_kwh"], label="Output")
    ax.scatter(anomalies["date"], anomalies["output_kwh"], color="red", label="Anomaly")
    ax.set_title("Energy Output with Anomalies")
    ax.legend()
    st.pyplot(fig)

    # Show anomalies table
    st.subheader("Anomaly Table")
    st.write(anomalies[["date", "output_kwh"]])

    # ===== Save anomalies to Google Drive folder =====
    if not os.path.exists(GOOGLE_DRIVE_FOLDER):
        os.makedirs(GOOGLE_DRIVE_FOLDER)

    alerts_path = os.path.join(GOOGLE_DRIVE_FOLDER, "alerts_today.csv")
    anomalies[["date", "output_kwh"]].to_csv(alerts_path, index=False)
    st.success(f"Alerts saved to Google Drive folder: {alerts_path}")

else:
    st.info("Please upload a CSV file to view results.")
