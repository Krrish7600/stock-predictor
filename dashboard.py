import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="AI Stock Dashboard", layout="wide")

# Sidebar Navigation
st.sidebar.title("🧠 AI Stock Predictor")
st.sidebar.markdown("## 📌 Navigation")
selected = st.sidebar.radio("Go to", ["Overview", "Trends", "Predictions", "Insights"])

# Header
st.title("📊 AI-Powered Stock Prediction Dashboard")
st.caption("Visualize historical investments, AI-predicted performance, and portfolio metrics.")

# --- Data Simulation (Replace with real-time API or model data) ---
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
invested = np.random.randint(13000, 20000, size=12)
predicted_growth = invested + np.random.randint(-2000, 3000, size=12)

df = pd.DataFrame({
    "Month": months,
    "Invested Amount": invested,
    "AI Predicted Value": predicted_growth
})

# Layout
col1, col2 = st.columns((2, 1))

# 📈 Line Chart - Investment vs AI Prediction
with col1:
    st.subheader("📈 Investment vs AI Prediction")
    fig = px.line(df, x="Month", y=["Invested Amount", "AI Predicted Value"], markers=True,
                  labels={"value": "Amount ($)", "variable": "Metric"})
    st.plotly_chart(fig, use_container_width=True)

# 📊 Pie Chart - Portfolio Distribution (Mock data)
with col2:
    st.subheader("📊 Portfolio Composition")
    pie_data = pd.DataFrame({
        'Stock': ['AAPL', 'GOOGL', 'TSLA', 'MSFT'],
        'Allocation': [35000, 25000, 20000, 30000]
    })
    pie = px.pie(pie_data, values='Allocation', names='Stock', hole=0.4)
    st.plotly_chart(pie, use_container_width=True)

# --- Divider ---
st.markdown("---")

# 📉 Daily Gains / Losses & Summary
col3, col4 = st.columns(2)

with col3:
    st.subheader("📉 Daily Gains / Losses")
    daily = pd.DataFrame({
        "Day": [f'Day {i}' for i in range(1, 11)],
        "Gains/Losses": np.random.randint(-500, 700, 10)
    })
    st.bar_chart(daily.set_index("Day"))

with col4:
    st.subheader("📋 Summary")
    st.write("##### Total Invested: `$92,600`")
    st.progress(85)
    st.write("##### Total Predicted Value: `$128,000`")
    st.progress(70)
    st.write("##### Accuracy (Last 30 days): 91.3% ✅")

# 🚀 Go to Predictor Page
if st.button("📍 Launch Stock Predictor"):
    st.switch_page("pages/predictor.py")
