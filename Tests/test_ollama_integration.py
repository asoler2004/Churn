#!/usr/bin/env python3
"""
Test script for Ollama integration with the fintech churn prediction system.
This script tests the Ollama API integration and enhanced customer profiling.
"""

import requests
import json
from typing import Dict, Any

def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print("✅ Ollama is running!")
            print(f"Available models: {[model['name'] for model in models]}")
            return True, models
        else:
            print(f"❌ Ollama responded with status {response.status_code}")
            return False, []
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Make sure it's running on localhost:11434")
        return False, []
    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")
        return False, []

def test_llm_api_health():
    """Test the LLM API health endpoint"""
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            health = response.json()
            print("✅ LLM API is running!")
            print(f"Health status: {json.dumps(health, indent=2)}")
            return True, health
        else:
            print(f"❌ LLM API responded with status {response.status_code}")
            return False, {}
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to LLM API. Make sure it's running on localhost:8001")
        return False, {}
    except Exception as e:
        print(f"❌ Error connecting to LLM API: {e}")
        return False, {}

def create_test_customer_data():
    """Create sample customer data for testing"""
    return {
        "age": 35,
        "housing": "r",
        "credit_score": 720.0,
        "deposits": 8,
        "withdrawal": 4,
        "purchases_partners": 15,
        "purchases": 32,
        "cc_taken": 1,
        "cc_recommended": 1,
        "cc_disliked": 0,
        "cc_liked": 1,
        "cc_application_begin": 1,
        "app_downloaded": 1,
        "web_user": 1,
        "app_web_user": 1,
        "ios_user": 0,
        "android_user": 1,
        "registered_phones": 2,
        "payment_type": "monthly",
        "waiting_4_loan": 0,
        "cancelled_loan": 0,
        "received_loan": 1,
        "rejected_loan": 0,
        "left_for_two_month_plus": 0,
        "left_for_one_month": 0,
        "rewards_earned": 450,
        "reward_rate": 0.025,
        "is_referred": 1,
        "churn_probability": 0.25,
        "churn_prediction": 0,
        "risk_level": "Medium"
    }

def test_rule_based_insights():
    """Test rule-based insights generation"""
    print("\n🧪 Testing Rule-based Insights...")
    
    customer_data = create_test_customer_data()
    customer_data.update({
        "use_transformers": False,
        "use_ollama": False
    })
    
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
            print(f"Recommendations length: {len(result['recommendations'])} chars")
            print(f"Key insights length: {len(result['key_insights'])} chars")
            return True, result
        else:
            print(f"❌ Failed with status {response.status_code}: {response.text}")
            return False, {}
            
    except Exception as e:
        print(f"❌ Error testing rule-based insights: {e}")
        return False, {}

def test_ollama_models_endpoint():
    """Test the Ollama models endpoint"""
    print("\n🔍 Testing Ollama Models Endpoint...")
    
    try:
        response = requests.get("http://localhost:8001/ollama/models", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Ollama models endpoint working!")
            print(f"Available: {result['available']}")
            print(f"Models found: {result['model_count']}")
            print(f"Models: {result['models']}")
            print(f"Recommended models: {result['recommended_models']}")
            return True, result
        else:
            print(f"❌ Failed with status {response.status_code}: {response.text}")
            return False, {}
            
    except Exception as e:
        print(f"❌ Error testing models endpoint: {e}")
        return False, {}

def test_ollama_insights(model_name="llama3.2"):
    """Test Ollama insights generation"""
    print(f"\n🦙 Testing Ollama Insights with {model_name}...")
    
    customer_data = create_test_customer_data()
    customer_data.update({
        "use_transformers": False,
        "use_ollama": True,
        "ollama_model": model_name
    })
    
    try:
        response = requests.post(
            "http://localhost:8001/generate-insights",
            json=customer_data,
            headers={"Content-Type": "application/json"},
            timeout=120  # Longer timeout for Ollama
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Ollama insights generated successfully!")
            print(f"Recommendations length: {len(result['recommendations'])} chars")
            print(f"Key insights length: {len(result['key_insights'])} chars")
            
            # Show a preview of the insights
            if result.get('debug_raw_response'):
                preview = result['debug_raw_response'][:200] + "..." if len(result['debug_raw_response']) > 200 else result['debug_raw_response']
                print(f"Preview: {preview}")
            
            return True, result
        else:
            print(f"❌ Failed with status {response.status_code}: {response.text}")
            return False, {}
            
    except Exception as e:
        print(f"❌ Error testing Ollama insights: {e}")
        return False, {}

def test_transformers_insights():
    """Test Transformers insights generation"""
    print("\n🤖 Testing Transformers Insights...")
    
    customer_data = create_test_customer_data()
    customer_data.update({
        "use_transformers": True,
        "use_ollama": False
    })
    
    try:
        response = requests.post(
            "http://localhost:8001/generate-insights",
            json=customer_data,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Transformers insights generated successfully!")
            print(f"Recommendations length: {len(result['recommendations'])} chars")
            print(f"Key insights length: {len(result['key_insights'])} chars")
            return True, result
        else:
            print(f"❌ Failed with status {response.status_code}: {response.text}")
            return False, {}
            
    except Exception as e:
        print(f"❌ Error testing Transformers insights: {e}")
        return False, {}

def main():
    """Run all tests"""
    print("🚀 Starting Ollama Integration Tests")
    print("=" * 50)
    
    # Test Ollama connection
    ollama_running, models = test_ollama_connection()
    
    # Test LLM API health
    api_running, health = test_llm_api_health()
    
    if not api_running:
        print("\n❌ Cannot proceed without LLM API. Please start it with: python llm_api.py")
        return
    
    # Test rule-based insights (should always work)
    rule_success, rule_result = test_rule_based_insights()
    
    # Test Transformers if available
    if health.get('transformers_available', False):
        transformers_success, transformers_result = test_transformers_insights()
    else:
        print("\n⚠️ Transformers not available, skipping test")
        transformers_success = False
    
    # Test Ollama models endpoint
    models_endpoint_success, models_info = test_ollama_models_endpoint()
    
    # Test Ollama if available
    if ollama_running and health.get('ollama_available', False):
        # Test with the first available model
        if models:
            model_to_test = models[0]['name']
            ollama_success, ollama_result = test_ollama_insights(model_to_test)
        else:
            print("\n⚠️ No Ollama models available")
            ollama_success = False
    else:
        print("\n⚠️ Ollama not available, skipping test")
        ollama_success = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"Rule-based insights: {'✅ PASS' if rule_success else '❌ FAIL'}")
    print(f"Transformers insights: {'✅ PASS' if transformers_success else '❌ FAIL/SKIP'}")
    print(f"Ollama models endpoint: {'✅ PASS' if models_endpoint_success else '❌ FAIL/SKIP'}")
    print(f"Ollama insights: {'✅ PASS' if ollama_success else '❌ FAIL/SKIP'}")
    
    if ollama_success:
        print("\n🎉 Ollama integration is working perfectly!")
        print("You can now use Ollama for enhanced AI insights in the Streamlit app.")
        if models_info and models_info.get('models'):
            print(f"Available models: {', '.join(models_info['models'][:3])}{'...' if len(models_info['models']) > 3 else ''}")
    elif ollama_running:
        print("\n⚠️ Ollama is running but integration needs debugging.")
    else:
        print("\n💡 To use Ollama:")
        print("1. Install Ollama: https://ollama.ai/")
        print("2. Run: ollama pull llama3.2")
        print("3. Start Ollama service")
        print("4. Re-run this test")

if __name__ == "__main__":
    main()