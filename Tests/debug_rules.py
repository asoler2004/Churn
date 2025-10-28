#!/usr/bin/env python3
"""
Debug script to test individual rules
"""

import requests
import json

def test_single_rule():
    """Test a single rule with debug output"""
    
    # Test Rule 1: Young + Low Credit + High Risk
    test_data = {
        "age": 25,
        "housing": "r",
        "credit_score": 450,
        "deposits": 2,
        "withdrawal": 5,
        "purchases_partners": 1,
        "purchases": 8,
        "cc_taken": 0,
        "cc_recommended": 1,
        "cc_disliked": 0,
        "cc_liked": 0,
        "cc_application_begin": 0,
        "app_downloaded": 0,
        "web_user": 1,
        "app_web_user": 0,
        "ios_user": 0,
        "android_user": 0,
        "registered_phones": 1,
        "payment_type": "monthly",
        "waiting_4_loan": 0,
        "cancelled_loan": 0,
        "received_loan": 0,
        "rejected_loan": 0,
        "left_for_two_month_plus": 0,
        "left_for_one_month": 0,
        "rewards_earned": 25,
        "reward_rate": 0.02,
        "is_referred": 0,
        "churn_probability": 0.75,
        "churn_prediction": 1,
        "risk_level": "High"
    }
    
    print("🧪 Testing Rule 1: Young + Low Credit + High Risk")
    print(f"Age: {test_data['age']}")
    print(f"Credit Score: {test_data['credit_score']}")
    print(f"Risk Level: {test_data['risk_level']}")
    print(f"Should trigger: age < 30 AND credit_score < 600 AND risk_level in ['Medium', 'High']")
    print(f"Conditions: {test_data['age'] < 30} AND {test_data['credit_score'] < 600} AND {test_data['risk_level'] in ['Medium', 'High']}")
    
    try:
        response = requests.post(
            "http://localhost:8001/generate-insights",
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            insights = result['recommendations']
            
            print(f"\n📄 Full Response:")
            print(insights)
            
            # Check for specific keywords
            keywords = ["educación financiera", "score crediticio", "jóvenes"]
            for keyword in keywords:
                if keyword.lower() in insights.lower():
                    print(f"✅ Found: {keyword}")
                else:
                    print(f"❌ Missing: {keyword}")
                    
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_single_rule()