import logging
from datetime import datetime

# Setup logging to an alert file
logging.basicConfig(
    filename='alerts.log',
    level=logging.INFO,
    format='%(asctime)s - ALERT - %(message)s'
)

def trigger_alert(transaction_data, fraud_probability):
    """
    This function handles the 'Outbound' alert.
    In a real world, this would call a Telegram/Slack API or Twilio for SMS.
    """
    alert_msg = (
        f"SUSPICIOUS ACTIVITY DETECTED\n"
        f"User ID: {transaction_data.get('user_id')}\n"
        f"Amount: ${transaction_data.get('amount')}\n"
        f"Fraud Probability: {fraud_probability * 100:.2f}%\n"
        f"Action: Account Temporarily Flagged\n"
        f"------------------------------------"
    )
    
    # 1. Log to file for the Dashboard
    logging.info(alert_msg)
    
    # 2. Print to Console
    print("\n" + "!"*30)
    print(alert_msg)
    print("!"*30 + "\n")

    # TODO: Add your Telegram/Email logic here later