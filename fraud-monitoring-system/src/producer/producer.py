import json
import time
import random
from datetime import datetime
from faker import Faker

fake = Faker()

def generate_transaction():
    """Generates a single synthetic transaction."""
    
    # Randomly decide if this transaction should look 'suspicious'
    is_suspicious = random.random() < 0.05  # 5% chance of being an outlier
    
    if is_suspicious:
        amount = round(random.uniform(5000, 20000), 2)  # High amount
    else:
        amount = round(random.uniform(10, 1000), 2)     # Normal amount

    transaction = {
        "transaction_id": fake.uuid4(),
        "user_id": random.randint(1000, 1100),         # Small pool of users to see patterns
        "amount": amount,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "merchant_category": random.choice(["Groceries", "Electronics", "Travel", "Dining", "Pharmacy"]),
        "location": fake.city(),
        "device_id": fake.ipv4(),
        "is_fraud_label": 1 if is_suspicious else 0    # We include this for training purposes
    }
    return transaction

def run_producer(interval=1):
    """Continuously generates and prints transactions."""
    print("--- Starting Transaction Stream (Ctrl+C to stop) ---")
    try:
        while True:
            tx = generate_transaction()
            print(json.dumps(tx, indent=2))
            
            ###----------------
            ### Kafka code here
            ###----------------
            
            time.sleep(interval) # Wait 1 second between transactions
    except KeyboardInterrupt:
        print("\nStream stopped.")

if __name__ == "__main__":
    run_producer()