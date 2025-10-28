#!/usr/bin/env python3
"""
Test script to verify UI changes work correctly
"""

import sys
import pandas as pd
import numpy as np

def test_rule_based_insights():
    """Test that rule-based insights work independently"""
    print("Testing rule-based insights...")
    
    # Import the function
    try:
        from streamlit_ui import get_rule_based_insights
        
        # Create test customer data
        customer_data = {
            'age': 35,
            'credit_score': 650,
            'deposits': 3,
            'purchases': 8,
            'app_downloaded': 0
        }
        
        # Create test prediction result
        prediction_result = {
            'churn_probability_XGB': 0.75,
            'risk_level_XGB': 'High'
        }
        
        # Test the function
        insights, error = get_rule_based_insights(customer_data, prediction_result)
        
        if insights and not error:
            print("✅ Rule-based insights working correctly")
            print(f"Sample insight: {insights[:100]}...")
            return True
        else:
            print(f"❌ Rule-based insights failed: {error}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing rule-based insights: {e}")
        return False

def test_health_check():
    """Test that health check works without LLM API"""
    print("Testing health check...")
    
    try:
        from streamlit_ui import check_llm_api_health
        
        health = check_llm_api_health()
        
        # Should always return a dict with required keys
        required_keys = ['gemini_direct_available', 'ollama_direct_available', 'transformers_available']
        
        if all(key in health for key in required_keys):
            print("✅ Health check working correctly")
            print(f"Gemini available: {health.get('gemini_direct_available', False)}")
            return True
        else:
            print("❌ Health check missing required keys")
            return False
            
    except Exception as e:
        print(f"❌ Error testing health check: {e}")
        return False

def test_feature_flags():
    """Test that feature flags are set correctly"""
    print("Testing feature flags...")
    
    try:
        from streamlit_ui import ENABLE_OLLAMA, ENABLE_TRANSFORMERS, ENABLE_GEMINI
        
        if not ENABLE_OLLAMA and not ENABLE_TRANSFORMERS and ENABLE_GEMINI:
            print("✅ Feature flags set correctly")
            print(f"Ollama: {ENABLE_OLLAMA}, Transformers: {ENABLE_TRANSFORMERS}, Gemini: {ENABLE_GEMINI}")
            return True
        else:
            print("❌ Feature flags not set correctly")
            print(f"Ollama: {ENABLE_OLLAMA}, Transformers: {ENABLE_TRANSFORMERS}, Gemini: {ENABLE_GEMINI}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing feature flags: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing UI changes...")
    print("=" * 50)
    
    tests = [
        test_feature_flags,
        test_rule_based_insights,
        test_health_check
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append(False)
            print()
    
    print("=" * 50)
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 All tests passed! ({passed}/{total})")
        return 0
    else:
        print(f"⚠️  Some tests failed ({passed}/{total})")
        return 1

if __name__ == "__main__":
    sys.exit(main())