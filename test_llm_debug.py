#!/usr/bin/env python3
"""
Debug test for LLM API to identify the issue
"""

import requests
import json

def test_llm_api_debug():
    """Debug the LLM API issue"""
    print("🔍 Debugging LLM API Issue")
    print("=" * 40)
    
    # Sample data that should work
    test_data = {
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
    
    print("📤 Sending test request...")
    print(f"📊 Data fields: {len(test_data)}")
    
    try:
        response = requests.post(
            "http://localhost:8001/generate-insights",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(f"📝 Recommendations length: {len(result.get('recommendations', ''))}")
            print(f"🔍 First 200 chars: {result.get('recommendations', '')[:200]}...")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            
            # Try to parse error details
            try:
                error_data = response.json()
                print(f"🔍 Error detail: {error_data.get('detail', 'No detail')}")
            except:
                print("🔍 Could not parse error JSON")
        
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: LLM API not running")
        print("   Start with: python llm_api.py")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")

def test_minimal_data():
    """Test with minimal required data"""
    print("\\n🧪 Testing Minimal Data")
    print("=" * 30)
    
    minimal_data = {
        "age": 30,
        "housing": "rent",
        "credit_score": 650.0,
        "deposits": 5,
        "withdrawal": 3,
        "purchases_partners": 10,
        "purchases": 25,
        "cc_taken": 0,
        "cc_recommended": 0,
        "cc_disliked": 0,
        "cc_liked": 0,
        "cc_application_begin": 0,
        "app_downloaded": 0,
        "web_user": 0,
        "app_web_user": 0,
        "ios_user": 0,
        "android_user": 0,
        "registered_phones": 1,
        "payment_type": "credit_card",
        "waiting_4_loan": 0,
        "cancelled_loan": 0,
        "received_loan": 0,
        "rejected_loan": 0,
        "left_for_two_month_plus": 0,
        "left_for_one_month": 0,
        "rewards_earned": 100,
        "reward_rate": 0.02,
        "is_referred": 0,
        "churn_probability": 0.15,
        "churn_prediction": 0,
        "risk_level": "Low"
    }
    
    try:
        response = requests.post(
            "http://localhost:8001/generate-insights",
            json=minimal_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"📥 Response status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Minimal data test passed!")
        else:
            print(f"❌ Minimal data test failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_llm_api_debug()
    test_minimal_data()