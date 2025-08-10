import os
import pandas as pd
import streamlit as st
from datetime import datetime

# Your Zapier folder path
GOOGLE_DRIVE_FOLDER = r"G:\My Drive\Zapier Watch"

# Ensure the folder exists
os.makedirs(GOOGLE_DRIVE_FOLDER, exist_ok=True)

st.title("Energy Data Anomaly Detection")

uploaded_file = st.file_uploader("Upload Energy Data CSV", type=["csv"])

if uploaded_file is not None:
    # Read uploaded CSV
    df = pd.read_csv(uploaded_file)
    st.write("Data preview:")
    st.dataframe(df.head())

    # Example anomaly detection logic (replace with your own)
    # For demonstration, we'll create a dummy anomalies dataframe:
    # Let's say anomalies if output_kwh > 1000 (you can adjust)
    if "output_kwh" in df.columns and "date" in df.columns:
        anomalies = df[df["output_kwh"] > 1000][["date", "output_kwh"]]
    else:
        st.error("CSV missing required columns: 'date' and 'output_kwh'")
        anomalies = pd.DataFrame()

    # Save alerts
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    alerts_filename = f"alerts_{timestamp}.csv"
    alerts_path = os.path.join(GOOGLE_DRIVE_FOLDER, alerts_filename)

    if anomalies.empty:
        df_to_save = pd.DataFrame({"message": ["No anomalies found"]})
    else:
        df_to_save = anomalies

    df_to_save.to_csv(alerts_path, index=False)
    st.success(f"Alerts saved to Google Drive folder: {alerts_path}")

else:
    st.info("Please upload a CSV file to detect anomalies.")
