import requests
import json

# Test data - example customer
test_customer = {
    "age": 35,
    "housing": "own",
    "credit_score": 350.5,
    "deposits": 1,
    "withdrawal": 1,
    "purchases_partners": 0,
    "purchases": 0,
    "cc_taken": 1,
    "cc_recommended": 0,
    "cc_disliked": 10,
    "cc_liked": 0,
    "cc_application_begin": 1,
    "app_downloaded": 0,
    "web_user": 0,
    "app_web_user": 0,
    "ios_user": 1,
    "android_user": 0,
    "registered_phones": 1,
    "payment_type": "credit_card",
    "waiting_4_loan": 0,
    "cancelled_loan": 0,
    "received_loan": 0,
    "rejected_loan": 1,
    "zodiac_sign": "pisces",
    "left_for_two_month_plus": 1,
    "left_for_one_month": 0,
    "rewards_earned": 0,
    "reward_rate": 0.0,
    "is_referred": 0
}

def test_api():
    """Test the churn prediction API"""
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print("Health Check:", response.json())
    except requests.exceptions.ConnectionError:
        print("Error: API server is not running. Please start it first with: python api.py")
        return
    
    # Test prediction endpoint
    try:
        response = requests.post(
            f"{base_url}/predict",
            json=test_customer,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\nPrediction Result:")
            print(f"Churn Probability: {result['churn_probability']:.4f}")
            print(f"Churn Prediction: {result['churn_prediction']}")
            print(f"Risk Level: {result['risk_level']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error making prediction: {str(e)}")
    
    # Test model info endpoint
    try:
        response = requests.get(f"{base_url}/model-info")
        if response.status_code == 200:
            info = response.json()
            print(f"\nModel Info:")
            print(f"Feature count: {len(info['feature_columns'])}")
            print(f"Categorical columns: {list(info['categorical_encodings'].keys())}")
        else:
            print(f"Error getting model info: {response.status_code}")
    except Exception as e:
        print(f"Error getting model info: {str(e)}")

if __name__ == "__main__":
    test_api()