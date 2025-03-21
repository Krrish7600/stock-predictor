from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from stock_data import fetch_stock_data
from prediction_engine import predict_stock_trend
from models import init_db, register_user, authenticate_user

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a secure key in production

# Initialize database
init_db()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = authenticate_user(email, password)
        if user:
            session['user_id'] = user[0]
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if register_user(email, password):
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        flash('Email already registered')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        ticker = request.form['ticker'].upper()
        data = fetch_stock_data(ticker)
        if data is not None:
            return redirect(url_for('prediction', ticker=ticker))
        flash('Invalid ticker or no data available')
    return render_template('search.html')

@app.route('/prediction/<ticker>')
def prediction(ticker):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    data = fetch_stock_data(ticker)
    if data is None:
        flash('No data available for this stock')
        return redirect(url_for('search'))
    prediction = predict_stock_trend(data)
    return render_template('prediction.html', ticker=ticker, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)