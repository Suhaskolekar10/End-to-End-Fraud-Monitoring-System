import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

def generate_historical_data(num_records=50000):
    print(f"Generating {num_records} historical records...")
    data = []
    
    # Start date for history (e.g., 30 days ago)
    start_date = datetime.now() - timedelta(days=30)

    for i in range(num_records):
        # Move time forward slightly for each transaction
        tx_time = start_date + timedelta(seconds=i * (30*24*3600/num_records))
        
        user_id = random.randint(1000, 1200)
        
        # Logic for fraud: 2% chance of a "high-value" fraud attempt
        is_fraud = 1 if random.random() < 0.02 else 0
        
        if is_fraud:
            amount = round(random.uniform(2000, 15000), 2)
            category = "Electronics" if random.random() > 0.5 else "Travel"
        else:
            amount = round(random.uniform(5, 800), 2)
            category = random.choice(["Groceries", "Dining", "Pharmacy", "Entertainment"])

        data.append({
            "transaction_id": fake.uuid4(),
            "user_id": user_id,
            "amount": amount,
            "timestamp": tx_time.strftime("%Y-%m-%d %H:%M:%S"),
            "merchant_category": category,
            "location": fake.city(),
            "device_id": fake.ipv4(),
            "is_fraud": is_fraud
        })

    df = pd.DataFrame(data)
    # Save to our data/raw folder
    output_path = "data/raw/historical_transactions.csv"
    df.to_csv(output_path, index=False)
    print(f"Successfully saved historical data to {output_path}")

if __name__ == "__main__":
    generate_historical_data(50000)