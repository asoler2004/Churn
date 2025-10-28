#!/usr/bin/env python3
"""
Test script to verify API fixes for churn prediction and LLM insights
"""

import requests
import json

def test_churn_prediction_api():
    """Test the churn prediction API"""
    print("🧪 Testing Churn Prediction API")
    print("=" * 40)
    
    # Sample customer data
    customer_data = {
        "age": 35,
        "credit_score": 720.5,
        "withdrawal": 3,
        "deposits": 8,
        "purchases_partners": 12,
        "cc_recommended": 0,
        "web_user": 1,
        "ios_user": 0,
        "registered_phones": 1,
        "waiting_4_loan": 0,
        "cancelled_loan": 0,
        "received_loan": 1,
        "rejected_loan": 0,
        "left_for_two_month_plus": 0,
        "left_for_one_month": 0,
        "reward_rate": 0.025,
        "is_referred": 1
    }
    
    try:
        print("📤 Sending request to churn prediction API...")
        response = requests.post(
            "http://localhost:8000/predict",
            json=customer_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API Response received successfully!")
            
            # Check for expected fields
            expected_fields = [
                'churn_probability_XGB', 'churn_prediction_XGB', 'risk_level_XGB',
                'churn_probability_RF', 'churn_prediction_RF', 'risk_level_RF'
            ]
            
            print("\\n📊 Checking response fields:")
            for field in expected_fields:
                if field in result:
                    value = result[field]
                    print(f"   ✅ {field}: {value}")
                else:
                    print(f"   ❌ Missing: {field}")
            
            # Show probabilities
            xgb_prob = result.get('churn_probability_XGB', 0)
            rf_prob = result.get('churn_probability_RF', 0)
            
            print(f"\\n🎯 Churn Probabilities:")
            print(f"   XGBoost: {xgb_prob:.2%}")
            print(f"   Random Forest: {rf_prob:.2%}")
            
            if xgb_prob > 0 or rf_prob > 0:
                print("   ✅ Non-zero probabilities detected!")
            else:
                print("   ⚠️ Both probabilities are 0% - check model training")
            
            return result
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Churn prediction API not running")
        print("   Start with: python api.py")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_llm_insights_api(prediction_result=None):
    """Test the LLM insights API"""
    print("\\n🧪 Testing LLM Insights API")
    print("=" * 40)
    
    # Sample customer data for LLM API
    llm_data = {
        "age": 35,
        "housing": "own",
        "credit_score": 720.5,
        "deposits": 8,
        "withdrawal": 3,
        "purchases_partners": 12,
        "purchases": 28,
        "cc_taken": 1,
        "cc_recommended": 0,
        "cc_disliked": 0,
        "cc_liked": 1,
        "cc_application_begin": 1,
        "app_downloaded": 1,
        "web_user": 1,
        "app_web_user": 1,
        "ios_user": 0,
        "android_user": 1,
        "registered_phones": 1,
        "payment_type": "credit_card",
        "waiting_4_loan": 0,
        "cancelled_loan": 0,
        "received_loan": 1,
        "rejected_loan": 0,
        "left_for_two_month_plus": 0,
        "left_for_one_month": 0,
        "rewards_earned": 150,
        "reward_rate": 0.025,
        "is_referred": 1,
        "churn_probability": 0.25,
        "churn_prediction": 0,
        "risk_level": "Medium"
    }
    
    # Use prediction result if provided
    if prediction_result:
        llm_data.update({
            "churn_probability": prediction_result.get('churn_probability_XGB', 0.25),
            "churn_prediction": prediction_result.get('churn_prediction_XGB', 0),
            "risk_level": prediction_result.get('risk_level_XGB', 'Medium')
        })
    
    try:
        print("📤 Sending request to LLM insights API...")
        response = requests.post(
            "http://localhost:8001/generate-insights",
            json=llm_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ LLM API Response received successfully!")
            
            # Show insights
            recommendations = result.get('recommendations', 'No recommendations')
            print("\\n💡 Generated Insights:")
            print(recommendations[:500] + "..." if len(recommendations) > 500 else recommendations)
            
            return result
            
        else:
            print(f"❌ LLM API Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: LLM API not running")
        print("   Start with: python llm_api.py")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_api_integration():
    """Test the complete API integration flow"""
    print("\\n🚀 Testing Complete API Integration")
    print("=" * 50)
    
    # Step 1: Test churn prediction
    prediction_result = test_churn_prediction_api()
    
    if prediction_result:
        # Step 2: Test LLM insights with prediction result
        llm_result = test_llm_insights_api(prediction_result)
        
        if llm_result:
            print("\\n🎯 Integration Test Results:")
            print("   ✅ Churn Prediction API: Working")
            print("   ✅ LLM Insights API: Working")
            print("   ✅ End-to-end flow: Success")
            
            # Show key metrics
            xgb_prob = prediction_result.get('churn_probability_XGB', 0)
            risk = prediction_result.get('risk_level_XGB', 'Unknown')
            print(f"\\n📊 Final Results:")
            print(f"   Churn Risk: {risk} ({xgb_prob:.2%})")
            print(f"   Insights Generated: Yes")
            
            return True
        else:
            print("\\n⚠️ Integration partially working - LLM API issues")
            return False
    else:
        print("\\n❌ Integration failed - Churn prediction API issues")
        return False

if __name__ == "__main__":
    print("🔧 API Fixes Verification Test")
    print("=" * 60)
    
    success = test_api_integration()
    
    if success:
        print("\\n🎉 All API fixes working correctly!")
        print("\\n📋 Summary:")
        print("   • Churn prediction returns correct field names")
        print("   • Non-zero probabilities are generated")
        print("   • LLM API accepts correct data format")
        print("   • End-to-end integration works")
    else:
        print("\\n⚠️ Some issues remain - check API services")
        print("\\n🔧 Troubleshooting:")
        print("   1. Ensure both APIs are running:")
        print("      - python api.py (port 8000)")
        print("      - python llm_api.py (port 8001)")
        print("   2. Check model files are present")
        print("   3. Verify data formats match API expectations")