import pandas as pd
import numpy as np

def engineer_features(df):
    # 1. Convert timestamp to datetime and sort
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(['user_id', 'timestamp'])

    # 2. Time-based features
    df['hour_of_day'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek

    # 3. Transaction Velocity (Count of transactions in the last 24h)
    df = df.set_index('timestamp')
    
    df['tx_count_24h'] = df.groupby('user_id')['amount'].transform(
        lambda x: x.rolling(window='24h').count()
    )
    
    # 4. Average Spending Behavior
    df['avg_spend_user'] = df.groupby('user_id')['amount'].transform(
        lambda x: x.expanding().mean()
    )

    # 5. Amount Deviation
    df['amount_deviation'] = df['amount'] / (df['avg_spend_user'] + 1e-9)

    # 6. Label Encoding for Categorical Data
    df['merchant_cat_code'] = df['merchant_category'].astype('category').cat.codes

    # Reset index to bring timestamp back as a column
    return df.reset_index()

if __name__ == "__main__":
    raw_data_path = "data/raw/historical_transactions.csv"
    processed_data_path = "data/processed/featured_transactions.csv"
    
    try:
        df_raw = pd.read_csv(raw_data_path)
        df_featured = engineer_features(df_raw)
        
        df_featured.to_csv(processed_data_path, index=False)
        print(f"✅ Feature Engineering Complete! Saved to {processed_data_path}")
        print(df_featured[['user_id', 'amount', 'tx_count_24h', 'amount_deviation']].head())
    except Exception as e:
        print(f"❌ Error during feature engineering: {e}")