import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

st.set_page_config(page_title="Energy AI Dashboard", layout="wide")

st.title("⚡ Energy Monitoring Dashboard")

# Sidebar for file upload
uploaded = st.sidebar.file_uploader("Upload your energy CSV", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)

    # Ensure date is datetime format
    if 'date' not in df.columns or 'output_kwh' not in df.columns:
        st.error("CSV must include 'date' and 'output_kwh' columns.")
    else:
        df['date'] = pd.to_datetime(df['date'])

        st.subheader("📈 Energy Output Chart")
        st.line_chart(df.set_index('date')['output_kwh'])

        # Run anomaly detection
        model = IsolationForest(contamination=0.05)
        df['anomaly'] = model.fit_predict(df[['output_kwh']]) == -1
        anomalies = df[df['anomaly'] == True]

        # Display summary (mock or real)
        st.subheader("📝 Weekly Summary")
        summary_text = "Anomalies detected on June 5 and 9."  # Replace with GPT summary if available
        st.markdown(f"**Summary:** {summary_text}")

        # Show anomaly chart
        st.subheader("🚨 Anomaly Visualization")
        fig, ax = plt.subplots()
        ax.plot(df["date"], df["output_kwh"], label="Output (kWh)")
        ax.scatter(anomalies["date"], anomalies["output_kwh"], color="red", label="Anomaly")
        ax.set_title("Energy Output with Anomalies")
        ax.legend()
        st.pyplot(fig)

        # Show alert table
        st.subheader("📋 Anomaly Alerts Table")
        st.dataframe(anomalies[["date", "output_kwh"]])

        # Export CSV for Zapier
        csv_name = "alerts_today.csv"
        anomalies[["date", "output_kwh"]].to_csv(csv_name, index=False)
        st.success(f"Anomaly data saved to {csv_name}. Ready for Zapier automation.")
        st.download_button("⬇ Download Alerts CSV", data=open(csv_name, "rb"), file_name=csv_name)

else:
    st.info("Please upload a CSV file with 'date' and 'output_kwh' columns.")
