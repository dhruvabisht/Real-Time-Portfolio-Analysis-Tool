import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from prophet import Prophet
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

# ----------- LOAD HISTORICAL STOCK DATA -----------
df_all = pd.read_csv('data/historical_stocks.csv')
df_all['Date'] = pd.to_datetime(df_all['Date'], errors='coerce')
stock_names = df_all['Name'].unique()

# Create model directory
os.makedirs("models", exist_ok=True)

for stock_name in stock_names:
    df = df_all[df_all['Name'] == stock_name].sort_values('Date')

    if df.shape[0] < 20:
        print(f"⏭️ Skipping {stock_name} — not enough data.")
        continue

    # Feature Engineering
    df['return'] = df['Close'].pct_change()
    df['volatility'] = df['return'].rolling(window=10).std()
    df['volume_change'] = df['Volume'].pct_change()
    df.dropna(inplace=True)

    if df['volatility'].nunique() < 3:
        print(f"⏭️ Skipping {stock_name} — insufficient volatility variety.")
        continue

    try:
        # Risk Classification
        risk_bins = pd.qcut(df['volatility'], q=3, labels=[0, 1, 2])
        df['risk'] = risk_bins.astype(int)

        # Features
        features = ['return', 'volatility', 'volume_change']
        X = df[features]
        y = df['risk']

        # Split and scale
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler().fit(X_train)
        X_train_scaled = scaler.transform(X_train)

        # Risk Model
        risk_model = RandomForestClassifier(n_estimators=100, random_state=42)
        risk_model.fit(X_train_scaled, y_train)
        joblib.dump(risk_model, f"models/risk_model_{stock_name}.pkl")
        joblib.dump(scaler, f"models/scaler_{stock_name}.pkl")

        # Anomaly Detection Model
        anomaly_model = IsolationForest(contamination=0.03, random_state=42)
        anomaly_model.fit(X_train_scaled)
        joblib.dump(anomaly_model, f"models/anomaly_model_{stock_name}.pkl")

        # Forecasting Model (Prophet)
        df_forecast = df[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
        forecast_model = Prophet()
        forecast_model.fit(df_forecast)
        forecast_model.save(f"models/forecast_model_{stock_name}.json")

        print(f"✅ Models trained and saved for {stock_name}")

    except Exception as e:
        print(f"❌ Failed for {stock_name}: {e}")
