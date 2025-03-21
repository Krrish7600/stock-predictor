from sklearn.linear_model import LinearRegression
import numpy as np

def predict_stock_trend(data):
    # Prepare data for simple linear regression
    X = np.array(range(len(data))).reshape(-1, 1)  # Time index
    y = np.array(data)  # Stock prices
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next 5 days
    future_X = np.array(range(len(data), len(data) + 5)).reshape(-1, 1)
    prediction = model.predict(future_X)
    
    # Determine trend
    trend = "Up" if prediction[-1] > y[-1] else "Down"
    return {"trend": trend, "predictions": prediction.tolist()}