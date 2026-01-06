import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

def train_fraud_model():
    # 1. Load Data
    data_path = "data/processed/featured_transactions.csv"
    if not os.path.exists(data_path):
        print("Data not found! Run feature_engineering.py first.")
        return

    df = pd.read_csv(data_path)

    # 2. Select Features and Target
    # We drop columns that the model can't use directly (like IDs and raw timestamps)
    features = ['amount', 'hour_of_day', 'day_of_week', 'tx_count_24h', 
                'avg_spend_user', 'amount_deviation', 'merchant_cat_code']
    X = df[features]
    y = df['is_fraud']

    # 3. Split Data (80% Train, 20% Test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("Training XGBoost Model...")
    
    # 4. Initialize and Train XGBoost
    # 'scale_pos_weight' helps the model focus more on the rare 'Fraud' cases
    fraud_ratio = (y == 0).sum() / (y == 1).sum()
    
    model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        scale_pos_weight=fraud_ratio, # Crucial for imbalanced data
        use_label_encoder=False,
        eval_metric='logloss'
    )

    model.fit(X_train, y_train)

    # 5. Evaluate
    y_pred = model.predict(X_test)
    print("\n--- Model Evaluation ---")
    print(classification_report(y_test, y_pred))
    
    # 6. Save the Model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/fraud_model.pkl')
    # Save feature list to ensure API uses the same order later
    joblib.dump(features, 'models/feature_list.pkl')
    
    print(f"\nModel saved to models/fraud_model.pkl")

if __name__ == "__main__":
    train_fraud_model()