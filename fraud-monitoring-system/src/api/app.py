import joblib
import pandas as pd
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

# --- 1. SETUP LOGGING (The Alerting Engine) ---
logging.basicConfig(
    filename='alerts.log',
    level=logging.INFO,
    format='%(asctime)s - ALERT - %(message)s'
)

def trigger_alert(transaction_data, fraud_probability):
    """Logs suspicious activity to a file and console."""
    alert_msg = (
        f"SUSPICIOUS ACTIVITY: User {transaction_data.get('user_id')} | "
        f"Amount: ${transaction_data.get('amount')} | "
        f"Prob: {fraud_probability:.2f}"
    )
    logging.info(alert_msg)
    print(f"\n[!] ALERT: {alert_msg}")

# --- 2. LOAD MODEL & ASSETS ---
try:
    model = joblib.load('models/fraud_model.pkl')
    features_names = joblib.load('models/feature_list.pkl')
    print("Model and Features loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}. Did you run train_model.py?")

# --- 3. API INITIALIZATION ---
app = FastAPI(title="End-to-End Fraud Monitoring System")

class Transaction(BaseModel):
    user_id: int
    amount: float
    hour_of_day: int
    day_of_week: int
    tx_count_24h: int
    avg_spend_user: float
    merchant_cat_code: int

@app.get("/")
def health_check():
    return {"status": "online", "model_version": "1.0.0"}

@app.post("/predict")
def predict_fraud(tx: Transaction):
    # Convert incoming request to DataFrame
    tx_dict = tx.dict()
    input_df = pd.DataFrame([tx_dict])
    
    # Feature Engineering (Must match training logic)
    # We add a small epsilon (1e-9) to avoid division by zero
    input_df['amount_deviation'] = input_df['amount'] / (input_df['avg_spend_user'] + 1e-9)
    
    # Reorder columns to match the model's expected input
    input_df = input_df[features_names]
    
    # Get Probability
    # [0][1] gives the probability of class 1 (Fraud)
    probability = float(model.predict_proba(input_df)[0][1])
    
    # --- 4. THRESHOLDING & ALERTING LOGIC ---
    decision = "APPROVED"
    
    if probability > 0.8:
        decision = "REJECTED (High Risk)"
        trigger_alert(tx_dict, probability)
    elif probability > 0.5:
        decision = "FLAGGED (Manual Review)"
        trigger_alert(tx_dict, probability)

    return {
        "user_id": tx.user_id,
        "fraud_probability": round(probability, 4),
        "decision": decision,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    # Run the server
    uvicorn.run(app, host="0.0.0.0", port=8000)