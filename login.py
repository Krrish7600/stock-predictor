import streamlit as st
import sqlite3

# 🎨 Page config
st.set_page_config(page_title="Login - Stock Predictor", layout="wide")

# 🔐 Page Title
st.title("🔑 Login / Sign Up")

# 📂 Database Setup
def create_users_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            email TEXT,
            name TEXT,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_users_table()

# 🟣 Login Section
username = st.text_input("Enter your username")
password = st.text_input("Enter your password", type="password")

if st.button("Login"):
    if username and password:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        result = c.fetchone()
        conn.close()

        if result:
            st.success(f"✅ Welcome, {username}!")
            st.balloons()
            st.info("Redirecting to Dashboard...")
            st.switch_page("pages/dashboard.py")
        else:
            st.error("❌ Incorrect username or password.")
    else:
        st.warning("⚠️ Please enter both fields.")

# 🆕 Sign Up Section
with st.expander("🆕 New User? Click to Sign Up"):
    with st.form("signup_form"):
        st.subheader("Create a New Account")
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        new_username = st.text_input("Choose a Username")
        new_password = st.text_input("Create Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        submit = st.form_submit_button("Register")

        if submit:
            if not (name and email and phone and new_username and new_password and confirm_password):
                st.error("🚨 Please fill all fields.")
            elif new_password != confirm_password:
                st.error("❌ Passwords do not match.")
            else:
                conn = sqlite3.connect('users.db')
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE username=?", (new_username,))
                if c.fetchone():
                    st.warning("⚠️ Username already exists. Try a different one.")
                else:
                    c.execute("INSERT INTO users (username, password, email, name, phone) VALUES (?, ?, ?, ?, ?)",
                              (new_username, new_password, email, name, phone))
                    conn.commit()
                    conn.close()
                    st.success("🎉 Account created successfully!")
                    st.balloons()
                    st.info("Redirecting to Dashboard...")
                    st.switch_page("pages/dashboard.py")
