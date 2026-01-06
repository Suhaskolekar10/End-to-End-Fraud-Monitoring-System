import sys
import os

sys.path.append(os.getcwd())

import time
import requests
import random
from src.producer.producer import generate_transaction

# URL of our FastAPI service
API_URL = "http://localhost:8000/predict"

def run_bridge():
    print("--- 🌉 Starting Real-Time Bridge (System End-to-End) ---")
    print(f"Connecting to API at {API_URL}...")
    
    try:
        while True:
            # 1. Generate a new raw transaction
            raw_tx = generate_transaction()
            
            # 2. Add some 'Mock State' (normally fetched from a DB/Redis)
            # In a real system, we'd lookup this user's 24h count and avg spend
            payload = {
                "user_id": raw_tx["user_id"],
                "amount": raw_tx["amount"],
                "hour_of_day": random.randint(0, 23),
                "day_of_week": random.randint(0, 6),
                "tx_count_24h": random.randint(1, 20) if raw_tx["amount"] > 1000 else random.randint(1, 5),
                "avg_spend_user": 50.0, # Mock average
                "merchant_cat_code": random.randint(0, 4)
            }
            
            # 3. Send to API for Scoring
            try:
                response = requests.post(API_URL, json=payload)
                result = response.json()
                
                # 4. Print results to console
                status_icon = "❌" if "REJECTED" in result['decision'] else "✅"
                print(f"{status_icon} User {payload['user_id']} | Amt: ${payload['amount']:<8} | Prob: {result['fraud_probability']:.4f} | {result['decision']}")
                
            except requests.exceptions.ConnectionError:
                print("Error: API is not running. Start src/api/app.py first!")
                break
            
            # Simulate real-world transaction gap
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nBridge stopped.")

if __name__ == "__main__":
    run_bridge()