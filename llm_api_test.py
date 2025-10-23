import pandas as pd
import numpy as np
import requests
import json
from faker import Faker
import shap
import matplotlib.pyplot as plt
import joblib
import warnings
warnings.filterwarnings('ignore')

# Initialize Faker
fake = Faker()

# Initialize data
data = pd.DataFrame()
filtered_data = pd.DataFrame()
selected_row = None
prediction_result = ""
llm_insights = ""
status_message = ""

# New customer form data
age = 30
housing = "rent"
credit_score = 650.0
deposits = 5
withdrawal = 3
purchases_partners = 10
purchases = 25
cc_taken = 0
cc_recommended = 0
cc_disliked = 0
cc_liked = 0
cc_application_begin = 0
app_downloaded = 1
web_user = 1
app_web_user = 1
ios_user = 1
android_user = 0
registered_phones = 1
payment_type = "credit_card"
waiting_4_loan = 0
cancelled_loan = 0
received_loan = 0
rejected_loan = 0
zodiac_sign = "leo"
left_for_two_month_plus = 0
left_for_one_month = 0
rewards_earned = 100
reward_rate = 0.02
is_referred = 0

# Filter variables
min_age = 18
max_age = 80
min_credit = 300
max_credit = 850
housing_filter = "all"

def load_sample_data():
    """Load sample data for demonstration"""
    global data, filtered_data
    
    # Create sample data
    np.random.seed(42)
    n_samples = 50
    
    sample_data = {
        "age": np.random.randint(18, 80, n_samples),
        "housing": np.random.choice(["own", "rent", "mortgage"], n_samples),
        "credit_score": np.random.normal(650, 100, n_samples).clip(300, 850),
        "deposits": np.random.poisson(5, n_samples),
        "withdrawal": np.random.poisson(3, n_samples),
        "purchases_partners": np.random.poisson(10, n_samples),
        "purchases": np.random.poisson(25, n_samples),
        "cc_taken": np.random.binomial(1, 0.3, n_samples),
        "cc_recommended": np.random.binomial(1, 0.4, n_samples),
        "cc_disliked": np.random.binomial(1, 0.2, n_samples),
        "cc_liked": np.random.binomial(1, 0.6, n_samples),
        "cc_application_begin": np.random.binomial(1, 0.3, n_samples),
        "app_downloaded": np.random.binomial(1, 0.7, n_samples),
        "web_user": np.random.binomial(1, 0.8, n_samples),
        "app_web_user": np.random.binomial(1, 0.5, n_samples),
        "ios_user": np.random.binomial(1, 0.4, n_samples),
        "android_user": np.random.binomial(1, 0.6, n_samples),
        "registered_phones": np.random.poisson(1, n_samples),
        "payment_type": np.random.choice(["credit_card", "debit_card", "bank_transfer"], n_samples),
        "waiting_4_loan": np.random.binomial(1, 0.1, n_samples),
        "cancelled_loan": np.random.binomial(1, 0.05, n_samples),
        "received_loan": np.random.binomial(1, 0.2, n_samples),
        "rejected_loan": np.random.binomial(1, 0.1, n_samples),
        "zodiac_sign": np.random.choice(["aries", "taurus", "gemini", "cancer", "leo", "virgo", 
                                       "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"], n_samples),
        "left_for_two_month_plus": np.random.binomial(1, 0.1, n_samples),
        "left_for_one_month": np.random.binomial(1, 0.15, n_samples),
        "rewards_earned": np.random.poisson(100, n_samples),
        "reward_rate": np.random.uniform(0.01, 0.05, n_samples),
        "is_referred": np.random.binomial(1, 0.3, n_samples)
    }
    
    data = pd.DataFrame(sample_data)
    add_personal_info_columns(data)
    filtered_data = data.copy()
    
    return data

def add_personal_info_columns(df):
    """Add personal information columns using Faker"""
    df['Name'] = [fake.first_name() for _ in range(len(df))]
    df['Surname'] = [fake.last_name() for _ in range(len(df))]
    df['email'] = [fake.email() for _ in range(len(df))]
    df['phone'] = [fake.phone_number() for _ in range(len(df))]
    df['address'] = [fake.address().replace('\n', ', ') for _ in range(len(df))]

def load_data(state):
    """Load sample data"""
    global data, filtered_data, status_message
    data = load_sample_data()
    filtered_data = data.copy()
    status_message = "Sample data loaded successfully!"
    print(status_message)
    # state.data = data
    # state.filtered_data = filtered_data
    # state.status_message = status_message

def apply_filters(state):
    """Apply filters to the data"""
    global filtered_data
    if data.empty:
        return
    
    filtered_data = data.copy()
    
    # Apply filters
    filtered_data = filtered_data[
        (filtered_data['age'] >= state.min_age) & 
        (filtered_data['age'] <= state.max_age) &
        (filtered_data['credit_score'] >= state.min_credit) & 
        (filtered_data['credit_score'] <= state.max_credit)
    ]
    
    if state.housing_filter != "all":
        filtered_data = filtered_data[filtered_data['housing'] == state.housing_filter]
    
    state.filtered_data = filtered_data

def add_customer(state):
    """Add a new customer"""
    global data, filtered_data, status_message
    
    new_record = {
        "age": state.age,
        "housing": state.housing,
        "credit_score": state.credit_score,
        "deposits": state.deposits,
        "withdrawal": state.withdrawal,
        "purchases_partners": state.purchases_partners,
        "purchases": state.purchases,
        "cc_taken": state.cc_taken,
        "cc_recommended": state.cc_recommended,
        "cc_disliked": state.cc_disliked,
        "cc_liked": state.cc_liked,
        "cc_application_begin": state.cc_application_begin,
        "app_downloaded": state.app_downloaded,
        "web_user": state.web_user,
        "app_web_user": state.app_web_user,
        "ios_user": state.ios_user,
        "android_user": state.android_user,
        "registered_phones": state.registered_phones,
        "payment_type": state.payment_type,
        "waiting_4_loan": state.waiting_4_loan,
        "cancelled_loan": state.cancelled_loan,
        "received_loan": state.received_loan,
        "rejected_loan": state.rejected_loan,
        "zodiac_sign": state.zodiac_sign,
        "left_for_two_month_plus": state.left_for_two_month_plus,
        "left_for_one_month": state.left_for_one_month,
        "rewards_earned": state.rewards_earned,
        "reward_rate": state.reward_rate,
        "is_referred": state.is_referred,
        "Name": fake.first_name(),
        "Surname": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": fake.address().replace('\n', ', ')
    }
    
    data = pd.concat([data, pd.DataFrame([new_record])], ignore_index=True)
    apply_filters(state)
    status_message = "New customer added successfully!"
    state.data = data
    state.status_message = status_message

def predict_churn(customer):
    """Predict churn for selected customer"""
    # global prediction_result, status_message
    
    # if state.selected_row is None or len(state.filtered_data) == 0:
    #     status_message = "Please select a customer first"
    #     state.status_message = status_message
    #     return
    
    try:
        # Get selected customer data
        # customer = state.filtered_data.iloc[state.selected_row[0]]
        
        # Prepare data for API (exclude personal info)
        customer_data = {
    "purchases_partners": 190,
    "reward_rate": 74.0,
    "cc_recommended": 80,
    "web_user": 1,
    "received_loan": 1,
    "credit_score": 800.0,
    "age": 65,
    "deposits": 100,
    "withdrawal": 10,
    "is_referred": 1,
    "registered_phones": 1,
    "ios_user": 1,
    "waiting_4_loan": 0,
    "cancelled_loan": 0,
    "rejected_loan": 0,
    "left_for_two_month_plus": 0,
    "left_for_one_month": 0,
}

        #  {k: v for k, v in customer.items() if k not in ['Name', 'Surname', 'email', 'phone', 'address']}

        
        
        # Make API call
        response = requests.post(
            "http://localhost:8000/predict",
            json=customer_data,
            headers={"Content-Type": "application/json"}
        )
        """"      
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": fake.address().replace('\n', ', ')"""
        if response.status_code == 200:
            result = response.json()
            prediction_result = f"""
Customer: {fake.first_name()} {fake.last_name()}
Churn Probability: {result['churn_probability_XGB']:.2%}
Prediction: {'Will Churn' if result['churn_prediction_XGB'] else 'Will Stay'}
Risk Level: {result['risk_level_XGB']}
            """
            status_message = "Prediction completed successfully!"
            print(status_message)
            print(prediction_result)
            # state.prediction_result = prediction_result
            # state.status_message = status_message
            
            # Store for LLM insights
        #     state.api_result = result
        #     state.selected_customer_data = customer_data
        # else:
        #     status_message = f"API Error: {response.status_code}"
        #     state.status_message = status_message
            
    except requests.exceptions.ConnectionError:
        status_message = "Error: Churn prediction API not running. Start api.py first."
        print(status_message)
    except Exception as e:
        status_message = f"Error: {str(e)}"
        print(status_message)

def generate_insights(customer):
    """Generate LLM insights"""
    # global llm_insights, status_message
    
    # if not hasattr(state, 'api_result') or not hasattr(state, 'selected_customer_data'):
    #     status_message = "Please run prediction first"
    #     state.status_message = status_message
    #     return
    
    try:

           
    
        # Combine customer data with prediction results
        insight_data = {
            "purchases_partners": 190,
            "reward_rate": 74.0,
            "cc_recommended": 80,
            "web_user": 1,
            "received_loan": 1,
            "credit_score": 800.0,
            "age": 65,
            "deposits": 100,
            "withdrawal": 10,
            "is_referred": 1,
            "registered_phones": 1,
            "ios_user": 1,
            "waiting_4_loan": 0,
            "cancelled_loan": 0,
            "rejected_loan": 0,
            "left_for_two_month_plus": 0,
            "left_for_one_month": 0,
            "housing": 'O',
            "purchases": 10,
            "cc_taken": 0,
            "cc_disliked": 0,
            "cc_liked": 1,
            "cc_application_begin": 1,
            "app_downloaded": 1,
            "app_web_user": 1,
            "android_user": 0,
            "payment_type": "bi_weekly",
            # "zodiac_sign": "aries",
            "rewards_earned": 5,
            "churn_probability": 0.8,
            "churn_prediction": 1,
            "risk_level": "High",
            # "Name": fake.first_name(),
            # "Surname": fake.last_name(),
            # "email": fake.email(),
            # "phone": fake.phone_number(),
            # "address": fake.address().replace('\n', ', ')
        }
        # state.selected_customer_data.copy()
        # insight_data.update(state.api_result)
        
        # Make LLM API call
        response = requests.post(
            "http://localhost:8001/generate-insights",
            json=insight_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            llm_insights = result['recommendations']
            status_message = "Insights generated successfully!"
            print(status_message)
            print(llm_insights)
        else:
            status_message = f"LLM API Error: {response.status_code}"
            print(status_message)
            
    except requests.exceptions.ConnectionError:
        status_message = "Error: LLM API not running. Start llm_api.py first."
        
    except Exception as e:
        status_message = f"Error: {str(e)}"
        

# Define the UI layout
page = """
# 🏦 Fintech Churn Prediction Dashboard

## Status
<|{status_message}|text|>

---

## 📊 Data Management

### Load Data
<|Load Sample Data|button|on_action=load_data|>

### Data Filters
**Age Range:** <|{min_age}|number|> to <|{max_age}|number|> <|Apply Filters|button|on_action=apply_filters|>

**Credit Score Range:** <|{min_credit}|number|> to <|{max_credit}|number|>

**Housing Filter:** <|{housing_filter}|selector|lov=['all', 'own', 'rent', 'mortgage']|>

### Customer Data Table
<|{filtered_data}|table|selected={selected_row}|>

---

## ➕ Add New Customer

<|layout|columns=1 1 1|
**Age:** <|{age}|number|>
**Housing:** <|{housing}|selector|lov=['own', 'rent', 'mortgage']|>
**Credit Score:** <|{credit_score}|number|>

**Deposits:** <|{deposits}|number|>
**Withdrawals:** <|{withdrawal}|number|>
**Purchases:** <|{purchases}|number|>

**Payment Type:** <|{payment_type}|selector|lov=['credit_card', 'debit_card', 'bank_transfer']|>
**Zodiac Sign:** <|{zodiac_sign}|selector|lov=['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']|>
**Rewards Earned:** <|{rewards_earned}|number|>
|>

<|Add Customer|button|on_action=add_customer|>

---

## 🤖 Churn Prediction

<|Predict Churn|button|on_action=predict_churn|>

### Prediction Results
<|{prediction_result}|text|>

---

## 💡 Customer Insights

<|Generate LLM Insights|button|on_action=generate_insights|>

### AI-Generated Recommendations
<|{llm_insights}|text|>
"""

if __name__ == "__main__":
    # Initialize data
    example_customer = load_sample_data()
    predict_churn(example_customer)
    generate_insights(example_customer)
    
    # Create and run GUI
    # gui = Gui(page)
    # gui.run(debug=True, port=5000, title="Churn Prediction Dashboard")