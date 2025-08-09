import pandas as pd
from sklearn.ensemble import IsolationForest

# === Step 1: Load Cleaned Dataset ===
df = pd.read_csv("cleaned_data.csv")
df['date'] = pd.to_datetime(df['date'])

# === Step 2: Feature Engineering ===
df['rolling_7d'] = df['output_kwh'].rolling(window=7, min_periods=1).mean()
df['weekday'] = df['date'].dt.weekday
df['lag_1'] = df['output_kwh'].shift(1)

# Remove NaN caused by lag
df.dropna(inplace=True)

# === Step 3: Train Isolation Forest Model ===
features = ['output_kwh', 'rolling_7d', 'weekday', 'lag_1']
model = IsolationForest(
    contamination=0.03,
    n_estimators=150,
    max_samples='auto',
    random_state=42
)
model.fit(df[features])

# === Step 4: Predict Anomalies ===
df['anomaly'] = model.predict(df[features]) == -1

# === Step 5: Save Predictions ===
predictions = df[['date', 'output_kwh', 'anomaly']]
predictions.to_csv("predictions.csv", index=False)

# === Step 6: Generate Summary ===
avg_kwh = df['output_kwh'].mean()
peak_kwh = df['output_kwh'].max()
anomaly_dates = df[df['anomaly']]['date'].dt.strftime("%b %d").tolist()

summary = (
    f"Summarize site performance: "
    f"Avg = {avg_kwh:.2f} kWh, "
    f"Anomalies = {', '.join(anomaly_dates)}, "
    f"Peak = {peak_kwh:.2f} kWh"
)

# === Step 7: Save Summary ===
with open("weekly_summary.txt", "w") as f:
    f.write(summary)

print("Pipeline complete. Files generated:")
print("- predictions.csv")
print("- weekly_summary.txt")
