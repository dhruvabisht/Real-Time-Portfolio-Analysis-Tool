import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from prophet import Prophet
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Load the data
df = pd.read_csv('data/historical_stocks.csv')
df['Date'] = pd.to_datetime(df['Date'])
df = df[df['Name'] == 'AAPL'].sort_values('Date')  # filter one stock for simplicity

# Feature Engineering
df['return'] = df['Close'].pct_change()
df['volatility'] = df['return'].rolling(window=10).std()
df['volume_change'] = df['Volume'].pct_change()
df.dropna(inplace=True)

# Risk Classification Labels: (0 = Low Risk, 1 = Medium, 2 = High)
risk_bins = pd.qcut(df['volatility'], q=3, labels=[0, 1, 2])
df['risk'] = risk_bins.astype(int)

# Features for classification and anomaly detection
features = ['return', 'volatility', 'volume_change']
X = df[features]

# ----------- RISK CLASSIFIER MODEL -----------
X_train, X_test, y_train, y_test = train_test_split(X, df['risk'], test_size=0.2, random_state=42)
scaler = StandardScaler().fit(X_train)
X_train_scaled = scaler.transform(X_train)

risk_model = RandomForestClassifier(n_estimators=100, random_state=42)
risk_model.fit(X_train_scaled, y_train)

# Save risk model & scaler
os.makedirs("models", exist_ok=True)
joblib.dump(risk_model, "models/risk_model.pkl")
joblib.dump(scaler, "models/scaler.pkl")

# ----------- ANOMALY DETECTION MODEL -----------
anomaly_model = IsolationForest(contamination=0.03, random_state=42)
anomaly_model.fit(X_train_scaled)

joblib.dump(anomaly_model, "models/anomaly_model.pkl")

# ----------- FORECASTING MODEL (Prophet) -----------
df_forecast = df[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})
forecast_model = Prophet()
forecast_model.fit(df_forecast)

forecast_model.save("models/forecast_model.json")  # Prophet has its own save method in v1.2+

print("✅ Models trained and saved successfully.")
