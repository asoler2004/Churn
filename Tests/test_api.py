import requests
import json
import shap


# Test data - example customer
test_customer = {
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

def test_api():
    """Test the churn prediction API"""
    base_url = "http://localhost:8000"
    # base_url = "https://fastapi-example-production-8493.up.railway.app"
    
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

            print("*******************************")    
            print("Predicción de XGBoost")
            print("*******************************")
            print(f"Churn Probability: {result['churn_probability_XGB']:.4f}")
            print(f"Churn Prediction: {result['churn_prediction_XGB']}")
            print(f"Risk Level: {result['risk_level_XGB']}")
            print(f"Shap_values: {result['shap_values_XGB']}")
            print(f"Shap_base: {result['base_values_XGB']}")
            print("*******************************")
            print("Predicción de Random Forest")
            print("*******************************")
            print(f"Churn Probability: {result['churn_probability_RF']:.4f}")
            print(f"Churn Prediction: {result['churn_prediction_RF']}")
            print(f"Risk Level: {result['risk_level_RF']}")
            print(f"Shap_values: {result['shap_values_RF']}")
            print(f"Shap_base: {result['base_values_RF']}")

            print(f"customer data: {result['customerdata']}")
            print(f"processed data: {result['processeddata']}")
     
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
            # print(f"Categorical columns: {list(info['categorical_encodings'].keys())}")
        else:
            print(f"Error getting model info: {response.status_code}")
    except Exception as e:
        print(f"Error getting model info: {str(e)}")

if __name__ == "__main__":
    test_api()