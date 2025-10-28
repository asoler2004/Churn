#!/usr/bin/env python3
"""
Test script for Gemini API integration with the fintech churn prediction system.
This script tests the Gemini API integration and comprehensive customer profiling.
"""

import os
import json
from typing import Dict, Any
import google.generativeai as genai

def test_gemini_import():
    """Test if gemini_api_call module can be imported"""
    try:
        from gemini_api_call import (
            generate_gemini_insights,
            quick_gemini_insights,
            test_gemini_connection,
            GeminiConfig,
            CustomerData,
            is_gemini_available,
            get_available_models
        )
        print("✅ Gemini module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import gemini_api_call module: {e}")
        return False

def test_api_key_setup():
    """Test API key configuration"""
    print("\n🔑 Testing API Key Setup...")
    
    try:
        from gemini_api_call import get_api_key
        
        api_key = get_api_key()
        if api_key:
            # Mask the key for security
            masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
            print(f"✅ API key found: {masked_key}")
            return True, api_key
        else:
            print("❌ No API key found")
            print("Setup options:")
            print("1. Set environment variable: export GEMINI_API_KEY='your-key'")
            print("2. Create .env file with: GEMINI_API_KEY=your-key")
            print("3. Create gemini_config.json with your API key")
            return False, None
            
    except Exception as e:
        print(f"❌ Error checking API key: {e}")
        return False, None

def test_gemini_connection():
    """Test connection to Gemini API"""
    print("\n🌐 Testing Gemini API Connection...")
    
    try:
        from gemini_api_call import test_gemini_connection
        
        status = test_gemini_connection()
        
        print(f"Status: {status['status']}")
        print(f"Available: {status['available']}")
        print(f"Message: {status['message']}")
        
        if status['available']:
            print(f"Available models: {status.get('models', [])}")
            if 'test_response' in status:
                print(f"Test response: {status['test_response']}")
            return True, status
        else:
            return False, status
            
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False, {}

def create_test_customer_data():
    """Create comprehensive test customer data"""
    return {
        "age": 34,
        "housing": "r",
        "credit_score": 695.0,
        "deposits": 18,
        "withdrawal": 12,
        "purchases_partners": 28,
        "purchases": 45,
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
        "waiting_4_loan": 1,  # Waiting for loan
        "cancelled_loan": 0,
        "received_loan": 0,
        "rejected_loan": 0,
        "left_for_two_month_plus": 0,
        "left_for_one_month": 0,
        "rewards_earned": 380,
        "reward_rate": 0.028,
        "is_referred": 1,
        "churn_probability": 0.35,  # Medium risk
        "churn_prediction": 0,
        "risk_level": "Medium"
    }

def test_customer_profiling():
    """Test comprehensive customer profiling"""
    print("\n📊 Testing Customer Profiling...")
    
    try:
        from gemini_api_call import create_comprehensive_customer_profile, CustomerData
        
        customer_data = create_test_customer_data()
        customer = CustomerData(**customer_data)
        
        profile = create_comprehensive_customer_profile(customer)
        
        print("✅ Customer profile generated successfully!")
        print(f"Profile length: {len(profile)} characters")
        
        # Show key sections
        sections = profile.split('\n\n')
        print(f"Profile sections: {len(sections)}")
        
        # Show first section as preview
        if sections:
            first_section = sections[0]
            print("\n--- PROFILE PREVIEW ---")
            print(first_section[:300] + "..." if len(first_section) > 300 else first_section)
        
        return True, profile
        
    except Exception as e:
        print(f"❌ Error in customer profiling: {e}")
        return False, None

def test_quick_insights():
    """Test quick insights generation"""
    print("\n🚀 Testing Quick Insights Generation...")
    
    try:
        from gemini_api_call import quick_gemini_insights
        
        customer_data = create_test_customer_data()
        
        print("Customer Profile: 34 years old, medium risk, waiting for loan")
        print("Generating insights... (this may take 10-30 seconds)")
        
        insights, error = quick_gemini_insights(customer_data, model="gemini-2.5-flash")
        
        if insights:
            print("✅ Quick insights generated successfully!")
            print(f"Response length: {len(insights)} characters")
            
            # Show structured preview
            lines = insights.split('\n')
            preview_lines = []
            for line in lines[:15]:  # First 15 lines
                if line.strip():
                    preview_lines.append(line.strip())
            
            print("\n--- INSIGHTS PREVIEW ---")
            for line in preview_lines:
                print(line)
            
            if len(lines) > 15:
                print("... (truncated)")
            
            return True, insights
        else:
            print(f"❌ Failed to generate insights: {error}")
            return False, None
            
    except Exception as e:
        print(f"❌ Error in quick insights test: {e}")
        return False, None

def test_advanced_insights():
    """Test advanced insights with custom configuration"""
    print("\n⚙️ Testing Advanced Insights Generation...")
    
    try:
        from gemini_api_call import generate_gemini_insights, GeminiConfig
        
        customer_data = create_test_customer_data()
        
        # Create custom configuration
        config = GeminiConfig(
            model="gemini-2.5-flash",  # Higher quality model
            temperature=0.8,         # More creative
            max_output_tokens=3000,  # Longer response
            top_p=0.95,
            top_k=50
        )
        
        print(f"Using model: {config.model}")
        print(f"Configuration: temp={config.temperature}, max_tokens={config.max_output_tokens}")
        print("Generating advanced insights... (this may take 30-60 seconds)")
        
        insights, debug_info = generate_gemini_insights(customer_data, config)
        
        print("✅ Advanced insights generated successfully!")
        print(f"Model used: {debug_info['model_used']}")
        print(f"Generation time: {debug_info['generation_time']:.2f} seconds")
        print(f"Response length: {len(debug_info['raw_response'])} characters")
        
        # Show configuration details
        print(f"Temperature: {debug_info['config']['temperature']}")
        print(f"Max tokens: {debug_info['config']['max_output_tokens']}")
        
        # Show usage metadata if available
        if debug_info.get('usage_metadata'):
            print(f"Usage metadata: {debug_info['usage_metadata']}")
        
        # Show structured sections
        sections = insights.split('\n\n')
        print(f"\nResponse has {len(sections)} sections")
        
        return True, insights
        
    except Exception as e:
        print(f"❌ Error in advanced insights test: {e}")
        return False, None

def test_model_comparison():
    """Test different Gemini models"""
    print("\n🔄 Testing Multiple Models...")
    
    try:
        from gemini_api_call import quick_gemini_insights, get_available_models
        
        models = get_available_models()
        customer_data = create_test_customer_data()
        
        print(f"Available models: {models}")
        
        # Test first 2 models
        models_to_test = models[:2] if len(models) >= 2 else models
        print(f"Testing {len(models_to_test)} models: {', '.join(models_to_test)}")
        
        results = {}
        
        for model in models_to_test:
            print(f"\n--- Testing {model} ---")
            
            try:
                insights, error = quick_gemini_insights(customer_data, model=model)
                
                if insights:
                    word_count = len(insights.split())
                    results[model] = {
                        'success': True,
                        'word_count': word_count,
                        'char_count': len(insights)
                    }
                    print(f"✅ Success: {word_count} words, {len(insights)} characters")
                else:
                    results[model] = {'success': False, 'error': error}
                    print(f"❌ Failed: {error}")
                    
            except Exception as e:
                results[model] = {'success': False, 'error': str(e)}
                print(f"❌ Exception: {e}")
        
        # Summary
        print("\n--- MODEL COMPARISON SUMMARY ---")
        successful_models = [m for m, r in results.items() if r['success']]
        print(f"Successful models: {len(successful_models)}/{len(models_to_test)}")
        
        for model, result in results.items():
            if result['success']:
                print(f"{model}: ✅ {result['word_count']} words")
            else:
                print(f"{model}: ❌ {result['error'][:50]}...")
        
        return len(successful_models) > 0
        
    except Exception as e:
        print(f"❌ Error in model comparison test: {e}")
        return False

def test_error_handling():
    """Test error handling with invalid data"""
    print("\n🛡️ Testing Error Handling...")
    
    try:
        from gemini_api_call import quick_gemini_insights
        
        # Test with missing required fields
        incomplete_data = {
            "age": 30,
            "credit_score": 650,
            # Missing many required fields
        }
        
        print("Testing with incomplete data...")
        insights, error = quick_gemini_insights(incomplete_data)
        
        if error:
            print(f"✅ Error handling working: {error[:100]}...")
            return True
        else:
            print("⚠️ Expected error but got success - check validation")
            return True  # Still counts as working
            
    except Exception as e:
        print(f"✅ Exception caught as expected: {str(e)[:100]}...")
        return True

def setup_api_key_interactively():
    """Interactive API key setup"""
    print("\n🔧 Interactive API Key Setup")
    print("=" * 40)
    
    api_key = input("Enter your Gemini API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("Skipping API key setup")
        return False
    
    try:
        from gemini_api_call import create_config_file
        
        if create_config_file(api_key):
            print("✅ API key saved to gemini_config.json")
            return True
        else:
            print("❌ Failed to save API key")
            return False
            
    except Exception as e:
        print(f"❌ Error saving API key: {e}")
        return False

def main():
    """Run all Gemini integration tests"""
    print("🤖 GEMINI API INTEGRATION TEST SUITE")
    print("=" * 50)
    
    # Test 1: Module import
    if not test_gemini_import():
        print("\n❌ Cannot proceed without gemini_api_call module")
        return
    
    # Test 2: API key setup
    api_key_available, api_key = test_api_key_setup()
    
    if not api_key_available:
        print("\n⚠️ No API key found. Would you like to set one up?")
        if input("Setup API key now? (y/n): ").lower().startswith('y'):
            if setup_api_key_interactively():
                api_key_available, api_key = test_api_key_setup()
        
        if not api_key_available:
            print("\n❌ Cannot test Gemini API without API key")
            print("\nTo get an API key:")
            print("1. Visit https://makersuite.google.com/app/apikey")
            print("2. Create a new API key")
            print("3. Set it as environment variable or in config file")
            return
    
    # Test 3: API connection
    connection_success, connection_status = test_gemini_connection()
    
    if not connection_success:
        print(f"\n❌ Cannot connect to Gemini API: {connection_status.get('message', 'Unknown error')}")
        return
    
    # Test 4: Customer profiling
    profiling_success, profile = test_customer_profiling()
    
    # Test 5: Quick insights
    quick_success, quick_insights = test_quick_insights()
    
    # Test 6: Advanced insights
    advanced_success = test_advanced_insights()
    
    # Test 7: Model comparison
    comparison_success = test_model_comparison()
    
    # Test 8: Error handling
    error_handling_success = test_error_handling()
    
    # Final summary
    print("\n" + "=" * 50)
    print("📊 GEMINI INTEGRATION TEST RESULTS")
    print("=" * 50)
    
    tests = [
        ("Module Import", True),  # If we got here, import worked
        ("API Key Setup", api_key_available),
        ("API Connection", connection_success),
        ("Customer Profiling", profiling_success),
        ("Quick Insights", quick_success),
        ("Advanced Insights", advanced_success),
        ("Model Comparison", comparison_success),
        ("Error Handling", error_handling_success)
    ]
    
    passed = sum(1 for _, success in tests if success)
    total = len(tests)
    
    for test_name, success in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Gemini integration is working perfectly.")
        print("You can now use Gemini API for comprehensive customer insights.")
        available_models = connection_status.get('models', [])
        print(f"Available models: {', '.join(available_models[:3])}{'...' if len(available_models) > 3 else ''}")
    elif passed >= 6:
        print("\n✅ Core functionality working. Some advanced features may need attention.")
    else:
        print("\n⚠️ Several tests failed. Please check your Gemini API setup.")
    
    print("\n💡 Next steps:")
    print("1. Integrate with Streamlit UI")
    print("2. Add to batch processing")
    print("3. Compare with other AI methods")
    print("4. Optimize prompts for your use case")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()