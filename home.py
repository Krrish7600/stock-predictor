import streamlit as st

# 🎨 Set Page Configuration
st.set_page_config(page_title="Stock Prediction AI", layout="wide")

# 📌 Custom CSS for styling
st.markdown(
    """
    <style>
        .hero {
            text-align: center;
            margin-top: 80px;
            padding: 50px;
            background: linear-gradient(to right, #0d6efd, #5a67d8);
            color: white;
            border-radius: 10px;
        }
        .hero h1 {
            font-size: 48px;
        }
        .hero p {
            font-size: 20px;
            margin-bottom: 30px;
        }
        .btn-primary {
            background-color: white;
            color: #0d6efd;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }
        .btn-primary:hover {
            background-color: #e6e6e6;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 🚀 Hero Section
st.markdown(
    """
    <div class="hero">
        <h1>AI-Powered Stock Prediction</h1>
        <p>Get real-time & accurate stock price predictions using advanced AI & Machine Learning.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 👉 Start Predicting Button (Streamlit-native Navigation)
st.markdown("<br>", unsafe_allow_html=True)
centered_col = st.columns([1, 2, 1])[1]

with centered_col:
    if st.button("Start Predicting", key="start_button"):
        st.switch_page("pages\login.py")  # ✅ Navigate to login.py

# 📌 Features Section
st.write("## 🔥 Why Choose Stock Predictor?")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 📈 AI Predictions")
    st.write("Accurate future stock price forecasting with deep learning.")

with col2:
    st.markdown("### 💱 Multi-Currency Support")
    st.write("View stock prices in multiple currencies with real-time conversion.")

with col3:
    st.markdown("### ⚡ Real-Time Data")
    st.write("Get the latest stock price data directly from the market.")
