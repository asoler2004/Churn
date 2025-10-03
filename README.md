# Fintech Churn Prediction System

A complete machine learning system for predicting customer churn using XGBoost, with a real-time API for inference.

## Features

- XGBoost classifier for churn prediction
- FastAPI-based REST API for real-time predictions
- Flexible categorical encoding: LabelEncoder or OneHotEncoder
- Automatic preprocessing of categorical variables
- Model performance evaluation
- Risk level classification (Low/Medium/High)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Prepare your data:
   - Place your CSV file in the project directory
   - Name it `churn_data.csv` or update the path in `train_model.py`

## Usage

### 1. Train the Model

```bash
python train_model.py
```

**Encoding Options:**
- Edit `train_model.py` and set `use_onehot = True` for OneHotEncoder
- Set `use_onehot = False` for LabelEncoder (default)

**OneHotEncoder vs LabelEncoder:**
- **LabelEncoder**: Assigns integer values (0, 1, 2...) to categories. More compact but implies ordinal relationship.
- **OneHotEncoder**: Creates binary columns for each category. No ordinal assumption but increases feature count.

This will:
- Load and preprocess your churn data
- Train an XGBoost classifier with your chosen encoding
- Evaluate model performance
- Save the trained model and metadata

### 2. Start the API Server

```bash
python api.py
```

The API will be available at `http://localhost:8000`

### 3. Test the API

```bash
python test_api.py
```

## API Endpoints

### POST /predict
Predict churn probability for a customer.

**Request body example:**
```json
{
  "age": 35,
  "housing": "own",
  "credit_score": 650.5,
  "deposits": 5,
  "withdrawal": 3,
  "purchases_partners": 10,
  "purchases": 25,
  "cc_taken": 1,
  "cc_recommended": 0,
  "cc_disliked": 0,
  "cc_liked": 1,
  "cc_application_begin": 1,
  "app_downloaded": 1,
  "web_user": 1,
  "app_web_user": 1,
  "ios_user": 1,
  "android_user": 0,
  "registered_phones": 1,
  "payment_type": "credit_card",
  "waiting_4_loan": 0,
  "cancelled_loan": 0,
  "received_loan": 1,
  "rejected_loan": 0,
  "zodiac_sign": "leo",
  "left_for_two_month_plus": 0,
  "left_for_one_month": 0,
  "rewards_earned": 150,
  "reward_rate": 0.02,
  "is_referred": 1
}
```

**Response:**
```json
{
  "churn_probability": 0.2345,
  "churn_prediction": 0,
  "risk_level": "Low"
}
```

### GET /health
Check API health status.

### GET /model-info
Get information about the loaded model.

## Data Requirements

Your CSV file should contain these columns:
- `user` (integer) - Row ID, will be excluded from features
- `churn` (integer) - Target variable (0/1)
- `age` (integer)
- `housing` (string)
- `credit_score` (float)
- `deposits` (integer)
- `withdrawal` (integer)
- `purchases_partners` (integer)
- `purchases` (integer)
- `cc_taken` (integer)
- `cc_recommended` (integer)
- `cc_disliked` (integer)
- `cc_liked` (integer)
- `cc_application_begin` (integer)
- `app_downloaded` (integer)
- `web_user` (integer)
- `app_web_user` (integer)
- `ios_user` (integer)
- `android_user` (integer)
- `registered_phones` (integer)
- `payment_type` (string)
- `waiting_4_loan` (integer)
- `cancelled_loan` (integer)
- `received_loan` (integer)
- `rejected_loan` (integer)
- `zodiac_sign` (string)
- `left_for_two_month_plus` (integer)
- `left_for_one_month` (integer)
- `rewards_earned` (integer)
- `reward_rate` (float)
- `is_referred` (integer)

## Files Generated

- `churn_model.pkl` - Trained XGBoost model
- `encoders.pkl` - Fitted encoders (Label or OneHot)
- `model_metadata.json` - Feature columns and encoding metadata

## Encoding Methods

**LabelEncoder (Default):**
- Converts categories to integers (0, 1, 2...)
- Compact representation
- May imply false ordinal relationships
- Good for tree-based models like XGBoost

**OneHotEncoder:**
- Creates binary columns for each category
- No ordinal assumptions
- Increases feature dimensionality
- Better for linear models, also works well with XGBoost

Choose based on your data characteristics and model performance.