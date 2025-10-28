#!/usr/bin/env python3
"""
Test script for the new transformers-based insights functionality
"""

import requests
import json

def test_llm_api_health():
    """Test the LLM API health endpoint"""
    print("🔍 Testing LLM API Health...")
    
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print("✅ LLM API is healthy!")
            print(f"   Status: {health_data.get('status')}")
            print(f"   Transformers Available: {health_data.get('transformers_available')}")
            print(f"   Rule-based Available: {health_data.get('rule_based_available')}")
            return health_data
        else:
            print(f"❌ LLM API returned status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Failed to connect to LLM API: {e}")
        return None

def test_rule_based_insights():
    """Test rule-based insights generation"""
    print("\n📊 Testing Rule-based Insights...")
    
    # Sample customer data
    customer_data = {
        "age": 35,
        "housing": "own",
        "credit_score": 720.0,
        "deposits": 8,
        "withdrawal": 4,
        "purchases_partners": 15,
        "purchases": 30,
        "cc_taken": 1,
        "cc_recommended": 1,
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
        "left_for_two_month_plus": 0,
        "left_for_one_month": 0,
        "rewards_earned": 250,
        "reward_rate": 0.03,
        "is_referred": 1,
        "churn_probability": 0.25,
        "churn_prediction": 0,
        "risk_level": "Medium",
        "use_transformers": False
    }
    
    try:
        response = requests.post(
            "http://localhost:8001/generate-insights",
            json=customer_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Rule-based insights generated successfully!")
            print("\n📋 Generated Insights:")
            print("-" * 50)
            print(result['recommendations'][:500] + "..." if len(result['recommendations']) > 500 else result['recommendations'])
            return True
        else:
            print(f"❌ Failed to generate rule-based insights: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing rule-based insights: {e}")
        return False

def test_transformers_insights():
    """Test transformers-based insights generation"""
    print("\n🤖 Testing Transformers-based Insights...")
    
    # Sample customer data
    customer_data = {
        "age": 28,
        "housing": "rent",
        "credit_score": 650.0,
        "deposits": 3,
        "withdrawal": 5,
        "purchases_partners": 8,
        "purchases": 12,
        "cc_taken": 0,
        "cc_recommended": 1,
        "cc_disliked": 1,
        "cc_liked": 0,
        "cc_application_begin": 0,
        "app_downloaded": 0,
        "web_user": 1,
        "app_web_user": 0,
        "ios_user": 0,
        "android_user": 1,
        "registered_phones": 1,
        "payment_type": "debit_card",
        "waiting_4_loan": 1,
        "cancelled_loan": 0,
        "received_loan": 0,
        "rejected_loan": 1,
        "left_for_two_month_plus": 1,
        "left_for_one_month": 0,
        "rewards_earned": 50,
        "reward_rate": 0.01,
        "is_referred": 0,
        "churn_probability": 0.75,
        "churn_prediction": 1,
        "risk_level": "High",
        "use_transformers": True
    }
    
    try:
        response = requests.post(
            "http://localhost:8001/generate-insights",
            json=customer_data,
            headers={"Content-Type": "application/json"},
            timeout=60  # Longer timeout for transformers
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Transformers insights generated successfully!")
            print("\n🧠 Generated AI Insights:")
            print("-" * 50)
            print(result['recommendations'][:500] + "..." if len(result['recommendations']) > 500 else result['recommendations'])
            return True
        else:
            print(f"❌ Failed to generate transformers insights: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing transformers insights: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Testing Transformers Insights Implementation")
    print("=" * 60)
    
    # Test API health
    health = test_llm_api_health()
    if not health:
        print("\n❌ Cannot proceed with tests - LLM API is not available")
        print("💡 Make sure to start the LLM API with: python llm_api.py")
        return
    
    # Test rule-based insights
    rule_success = test_rule_based_insights()
    
    # Test transformers insights if available
    if health.get('transformers_available'):
        transformers_success = test_transformers_insights()
    else:
        print("\n⚠️ Transformers not available - skipping transformers test")
        print("   This is normal if the model failed to load")
        transformers_success = None
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    print(f"   API Health: {'✅ Pass' if health else '❌ Fail'}")
    print(f"   Rule-based Insights: {'✅ Pass' if rule_success else '❌ Fail'}")
    if transformers_success is not None:
        print(f"   Transformers Insights: {'✅ Pass' if transformers_success else '❌ Fail'}")
    else:
        print(f"   Transformers Insights: ⚠️ Skipped (not available)")
    
    if rule_success:
        print("\n🎉 Basic functionality is working!")
        if transformers_success:
            print("🤖 Advanced AI functionality is also working!")
        else:
            print("💡 Advanced AI is not available, but rule-based insights work fine.")
    else:
        print("\n❌ Basic functionality has issues - check the LLM API")

if __name__ == "__main__":
    main()