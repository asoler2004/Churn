# 🏦 Fintech Churn Prediction System

A comprehensive machine learning system for predicting customer churn with an interactive dashboard, real-time API, and AI-powered insights.

## 🌟 Features

### Core ML System
- XGBoost classifier for churn prediction
- FastAPI-based REST API for real-time predictions
- Flexible categorical encoding: LabelEncoder or OneHotEncoder
- Automatic preprocessing of categorical variables
- Model performance evaluation
- Risk level classification (Low/Medium/High)

### Interactive Dashboards
**Taipy Dashboard** (`churn_ui.py`)
- 📊 Data management with filtering and customer addition
- 🤖 Real-time churn prediction interface
- 💡 AI-powered customer retention insights
- 📈 SHAP explainability plots
- 🔍 Customer data exploration and analysis

**Streamlit Dashboard** (`streamlit_ui.py`)
- 🎨 Modern, responsive web interface
- 📊 Interactive data tables with AgGrid
- 📈 Advanced visualizations with Plotly
- 🎯 Customer profile radar charts
- 🔢 Risk gauge indicators
- 📱 Mobile-friendly design

### AI Insights Engine
- LLM-powered customer retention recommendations
- Personalized action items based on customer profile
- Risk-based intervention strategies
- Behavioral pattern analysis

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model
```bash
python train_model.py
```

**Encoding Options:**
- Edit `train_model.py` and set `use_onehot = True` for OneHotEncoder
- Set `use_onehot = False` for LabelEncoder (default)

### 3. Start All Services

**Option A: Taipy Dashboard (Default)**
```bash
python start_services.py
```

**Option B: Streamlit Dashboard**
```bash
python start_services.py --ui streamlit
```

**Option C: Streamlit Only**
```bash
python run_streamlit.py
```

This starts:
- 🤖 Churn Prediction API (port 8000)
- 💡 LLM Insights API (port 8001)  
- 📊 Dashboard (Taipy: port 5000, Streamlit: port 8501)

### 4. Access the Dashboard
- **Taipy**: `http://localhost:5000`
- **Streamlit**: `http://localhost:8501`

## 📋 Manual Setup (Alternative)

### Train the Model
```bash
python train_model.py
```

### Start Services Individually
```bash
# Terminal 1: Churn Prediction API
python api.py

# Terminal 2: LLM Insights API  
python llm_api.py

# Terminal 3: Taipy Dashboard
python churn_ui.py
```

## 🎮 Using the Dashboards

### Taipy Dashboard Features
1. **Data Management**: Load data, apply filters, add customers
2. **Churn Prediction**: Select customers, run predictions, view results
3. **AI Insights**: Generate LLM-powered retention recommendations

### Streamlit Dashboard Features
1. **📊 Customer Data Tab**
   - Interactive data table with sorting and filtering
   - Customer selection with checkboxes
   - Real-time summary statistics
   - Advanced filtering sidebar

2. **➕ Add Customer Tab**
   - Comprehensive customer form
   - All 30+ customer attributes
   - Automatic personal info generation
   - Form validation

3. **🤖 Predictions Tab**
   - Customer profile visualization
   - Real-time churn prediction
   - Risk level indicators with color coding
   - SHAP explainability plots
   - Progress bars and gauges

4. **💡 Insights Tab**
   - AI-powered retention strategies
   - Risk gauge visualization
   - Personalized recommendations
   - Action-oriented insights

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

## 📁 Project Structure

```
├── train_model.py          # XGBoost model training
├── api.py                  # Churn prediction API
├── llm_api.py             # LLM insights API
├── churn_ui.py            # Taipy dashboard
├── streamlit_ui.py        # Streamlit dashboard
├── test_api.py            # API testing script
├── start_services.py      # Service orchestration
├── run_streamlit.py       # Streamlit standalone runner
├── requirements.txt       # Dependencies
└── README.md             # Documentation
```

## 🗂️ Generated Files

- `churn_model.pkl` - Trained XGBoost model
- `encoders.pkl` - Fitted encoders (Label or OneHot)
- `model_metadata.json` - Feature columns and encoding metadata
- `shap_plot.png` - SHAP explainability plots (when generated)

## 🔧 API Endpoints

### Churn Prediction API (Port 8000)
- `POST /predict` - Predict churn for a customer
- `GET /health` - Health check
- `GET /model-info` - Model information

### LLM Insights API (Port 8001)
- `POST /generate-insights` - Generate retention recommendations
- `GET /health` - Health check

## 🎛️ Encoding Methods

**LabelEncoder (Default):**
- Converts categories to integers (0, 1, 2...)
- Compact representation
- Good for tree-based models like XGBoost

**OneHotEncoder:**
- Creates binary columns for each category
- No ordinal assumptions
- Better for capturing category relationships

## 🔍 Dashboard Features

### Data Management
- **CSV Loading**: Load customer data from files
- **Fake Data Generation**: Automatically add personal info columns
- **Real-time Filtering**: Filter by age, credit score, housing
- **Customer Addition**: Add new customers via form

### Prediction & Analysis
- **ML Predictions**: Real-time churn probability scoring
- **Risk Classification**: Low/Medium/High risk levels
- **SHAP Explanations**: Feature importance visualization
- **Customer Selection**: Click-to-select interface

### AI Insights
- **Retention Strategies**: Personalized recommendations
- **Action Items**: Specific intervention steps
- **Risk Analysis**: Behavioral pattern insights
- **Customer Profiling**: Comprehensive analysis

## 🚨 Troubleshooting

**Model Not Found Error:**
```bash
python train_model.py  # Train the model first
```

**API Connection Error:**
- Ensure all services are running
- Check ports 8000, 8001, 5000 are available
- Use `python start_services.py` for automatic startup

**Dashboard Not Loading:**
- Check Taipy installation: `pip install taipy`
- Verify port 5000 is available
- Check browser console for errors