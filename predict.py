import streamlit as st
import pandas as pd
import numpy as np
import requests
import os
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objects as go
import tensorflow as tf
from tensorflow.keras.models import load_model

# 🔑 Polygon.io API Key
POLYGON_API_KEY = "4QR67o7Kj_fmup6I9nxg4fmFPOsgx4DP"

def show():
    st.title("🔮 Stock Price Prediction")

    st.sidebar.header("📊 Stock Prediction")
    stock_symbol = st.sidebar.text_input("Enter Stock Symbol:", "AAPL")
    currency = st.sidebar.selectbox("Select Currency", ["USD", "EUR", "GBP"], index=0)
    prediction_period = st.sidebar.selectbox("Select Prediction Period", ["1 Day", "7 Days", "1 Month", "6 Months"], index=0)

    period_mapping = {
        "1 Day": 1,
        "7 Days": 7,
        "1 Month": 30,
        "6 Months": 180
    }
    future_steps = period_mapping[prediction_period]

    if st.sidebar.button("Predict Stock Price"):
        df = get_stock_data(stock_symbol, days=365, currency=currency)

        if df is not None:
            df = add_moving_averages(df)
            df = calculate_market_structure(df)

            st.subheader(f"📌 Latest Stock Data for {stock_symbol} in {currency}")
            st.dataframe(df.tail(10))

            plot_stock_data(df)

            st.subheader(f"🔮 Predicted Prices for Next {prediction_period}")
            pred_df = predict_stock(df, future_steps)
            st.dataframe(pred_df)

            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(
                x=pred_df["Time"],
                y=pred_df["Predicted Price"],
                mode="lines",
                name="Predicted Price",
                line=dict(color="red", dash="dot")
            ))
            st.plotly_chart(fig_pred, use_container_width=True)

@st.cache_data(ttl=60)
def get_stock_data(symbol, days=90, currency="USD"):
    end_date = datetime.utcnow().strftime("%Y-%m-%d")
    start_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?apiKey={POLYGON_API_KEY}"
    
    response = requests.get(url)
    data = response.json()

    if "results" not in data:
        st.error("❌ Error fetching stock data. Try again.")
        return None

    df = pd.DataFrame(data["results"])
    df["Time"] = pd.to_datetime(df["t"], unit="ms")
    df.set_index("Time", inplace=True)
    df.rename(columns={"c": "Close"}, inplace=True)

    return df[["Close"]].dropna()

def add_moving_averages(df, short_window=10, long_window=50):
    df["SMA"] = df["Close"].rolling(window=short_window).mean()
    df["EMA"] = df["Close"].ewm(span=long_window, adjust=False).mean()
    return df

def calculate_market_structure(df):
    df["Support"] = df["Close"].rolling(window=20).min()
    df["Resistance"] = df["Close"].rolling(window=20).max()
    df["Swing_High"] = df["Close"][(df["Close"].shift(3) < df["Close"]) & (df["Close"].shift(-3) < df["Close"])]
    df["Swing_Low"] = df["Close"][(df["Close"].shift(3) > df["Close"]) & (df["Close"].shift(-3) > df["Close"])]
    df["Trend"] = "Sideways"
    df.loc[df["SMA"] > df["EMA"], "Trend"] = "Uptrend"
    df.loc[df["SMA"] < df["EMA"], "Trend"] = "Downtrend"
    df["ATR"] = df["Close"].rolling(window=14).apply(lambda x: np.ptp(x), raw=True)
    return df

def train_lstm(df):
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df["Close"].values.reshape(-1, 1))

    seq_length = 20
    X_train, y_train = [], []
    for i in range(seq_length, len(scaled_data) - 1):
        X_train.append(scaled_data[i - seq_length:i])
        y_train.append(scaled_data[i, 0])

    X_train, y_train = np.array(X_train), np.array(y_train)

    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(64, return_sequences=True, input_shape=(X_train.shape[1], 1)),
        tf.keras.layers.LSTM(64, return_sequences=False),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer="adam", loss="mean_squared_error")
    model.fit(X_train, y_train, epochs=15, batch_size=16, verbose=0)

    if not os.path.exists("models"):
        os.makedirs("models")
    model.save("models/stock_lstm_model.h5")
    np.save("models/scaler.npy", scaler)

    return scaler

def predict_stock(df, future_steps):
    model_path = "models/stock_lstm_model.h5"
    scaler_path = "models/scaler.npy"

    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        st.warning("⚠️ Model training required. Training now...")
        scaler = train_lstm(df)
        model = load_model(model_path)
    else:
        model = load_model(model_path)
        scaler = np.load(scaler_path, allow_pickle=True).item()

    scaled_data = scaler.transform(df["Close"].values.reshape(-1, 1))
    last_sequence = scaled_data[-20:].reshape(1, 20, 1)

    future_prices = []
    for _ in range(future_steps):
        predicted = model.predict(last_sequence, verbose=0)[0][0]
        future_prices.append(predicted)
        last_sequence = np.append(last_sequence[:, 1:, :], [[[predicted]]], axis=1)

    future_prices = scaler.inverse_transform(np.array(future_prices).reshape(-1, 1))[:, 0]
    future_dates = [df.index[-1] + timedelta(days=i) for i in range(1, future_steps + 1)]

    return pd.DataFrame({"Time": future_dates, "Predicted Price": future_prices})

def plot_stock_data(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], mode="lines", name="Actual Price", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=df.index, y=df["SMA"], mode="lines", name="SMA (10)", line=dict(color="orange")))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA"], mode="lines", name="EMA (50)", line=dict(color="purple")))
    fig.add_trace(go.Scatter(x=df.index, y=df["Support"], mode="lines", name="Support Level", line=dict(color="green", dash="dot")))
    fig.add_trace(go.Scatter(x=df.index, y=df["Resistance"], mode="lines", name="Resistance Level", line=dict(color="red", dash="dot")))
    st.plotly_chart(fig, use_container_width=True)
