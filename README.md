# Real-Time Fraud Monitoring System 🛡️

A comprehensive, end-to-end financial surveillance system that detects fraudulent transactions in real-time using Machine Learning. This project covers the entire pipeline from synthetic data generation and feature engineering to model deployment and containerization.

## 🚀 Features

* **Synthetic Data Generation:** Custom engine producing 50,000+ realistic transaction records with embedded fraud patterns.
* **Behavioral Feature Engineering:** Advanced logic to calculate **Transaction Velocity** (24h counts) and **Spending Deviation** on the fly.
* **ML Engine:** High-performance **XGBoost** classifier handling imbalanced datasets (fraud vs. legitimate).
* **Real-Time API:** **FastAPI** service serving predictions in milliseconds with automated thresholding.
* **Containerized Architecture:** Fully deployable via **Docker** and **Docker Compose**.
* **Automated Alerting:** Real-time logging of high-risk activities into an `alerts.log` for immediate response.

---

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **ML Framework:** XGBoost, Scikit-Learn
* **API Framework:** FastAPI, Uvicorn
* **Data Processing:** Pandas, NumPy
* **Deployment:** Docker, Docker Compose
* **Testing:** Requests, Curl

---

## 📂 Project Structure

```text
├── src/
│   ├── api/           # FastAPI Scoring Service & Alerting
│   ├── processor/     # Feature Engineering & Model Training scripts
│   ├── producer/      # Historical and Live data generators
│   └── bridge.py      # Simulation script connecting Producer to API
├── models/            # Serialized XGBoost models and feature lists
├── data/              # Raw and processed datasets (CSV)
├── Dockerfile         # Container configuration
└── docker-compose.yml # Multi-container orchestration

```

---

## 🏁 Getting Started

### 1. Prerequisites

* Python 3.9+ installed
* Docker & Docker Compose (Optional, but recommended)

### 2. Local Setup & Training

```bash
# Clone the repository
git clone https://github.com/your-username/fraud-monitoring-system.git
cd fraud-monitoring-system

# Install dependencies
pip install -r requirements.txt

# Step 1: Generate historical data
python src/producer/generate_history.py

# Step 2: Run feature engineering
python src/processor/feature_engineering.py

# Step 3: Train the model
python src/processor/train_model.py

```

### 3. Run the Real-Time System (Manual)

Open two terminals:

* **Terminal 1 (API):** `python src/api/app.py`
* **Terminal 2 (Bridge):** `PYTHONPATH=. python src/bridge.py`

### 4. Run with Docker (Recommended)

```bash
docker-compose up --build

```

---

## 📊 How it Works

1. **Velocity Check:** The system tracks how many times a user has spent money in the last 24 hours.
2. **Deviation Analysis:** If a transaction amount is significantly higher than the user's historical average, the `amount_deviation` score triggers a risk flag.
3. **ML Inference:** The XGBoost model analyzes these features against learned fraud patterns (e.g., high spending at 3:00 AM in unusual categories).
4. **Action:** The API returns a decision: **APPROVED**, **FLAGGED**, or **REJECTED**.

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.

---
