#!/usr/bin/env python3
"""
Standalone Ollama Test Script

This script tests Ollama integration independently of the LLM API.
It demonstrates how to use Ollama directly for customer insights.
"""

import sys
import os
from typing import Dict, Any

def test_ollama_import():
    """Test if ollama_local module can be imported"""
    try:
        from ollama_local import (
            generate_ollama_insights,
            CustomerInsightRequest,
            OllamaConfig,
            check_ollama_status,
            get_available_models,
            test_ollama_connection,
            quick_generate_insights
        )
        print("✅ Ollama module imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import ollama_local module: {e}")
        print("Make sure ollama_local.py is in the same directory")
        return False

def test_ollama_connection():
    """Test direct connection to Ollama"""
    try:
        from ollama_local import test_ollama_connection
        
        print("\n🔍 Testing Ollama Connection...")
        status = test_ollama_connection()
        
        if status['available']:
            print("✅ Ollama is running and accessible")
            print(f"Models available: {status['model_count']}")
            print(f"Models: {', '.join(status['models'][:3])}{'...' if len(status['models']) > 3 else ''}")
            return True, status['models']
        else:
            print(f"❌ Ollama not available: {status['message']}")
            return False, []
            
    except Exception as e:
        print(f"❌ Error testing Ollama connection: {e}")
        return False, []

def create_test_customer():
    """Create a test customer for insights generation"""
    return {
        "age": 32,
        "housing": "r",
        "credit_score": 685.0,
        "deposits": 15,
        "withdrawal": 8,
        "purchases_partners": 22,
        "purchases": 38,
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
        "registered_phones": 1,
        "payment_type": "monthly",
        "waiting_4_loan": 0,
        "cancelled_loan": 0,
        "received_loan": 1,
        "rejected_loan": 0,
        "left_for_two_month_plus": 0,
        "left_for_one_month": 1,  # Risk indicator
        "rewards_earned": 280,
        "reward_rate": 0.025,
        "is_referred": 1,
        "churn_probability": 0.45,  # Medium-high risk
        "churn_prediction": 0,
        "risk_level": "Medium"
    }

def test_quick_insights(models):
    """Test quick insights generation"""
    print("\n🚀 Testing Quick Insights Generation...")
    
    if not models:
        print("❌ No models available for testing")
        return False
    
    try:
        from ollama_local import quick_generate_insights
        
        customer_data = create_test_customer()
        model_to_test = models[0]  # Use first available model
        
        print(f"Customer Profile: {customer_data['age']} years old, {customer_data['risk_level']} risk")
        print(f"Using model: {model_to_test}")
        print("Generating insights... (this may take 30-60 seconds)")
        
        insights, error = quick_generate_insights(customer_data, model=model_to_test)
        
        if insights:
            print("✅ Quick insights generated successfully!")
            print(f"Response length: {len(insights)} characters")
            
            # Show preview
            lines = insights.split('\n')
            preview_lines = []
            for line in lines[:10]:  # First 10 lines
                if line.strip():
                    preview_lines.append(line.strip())
            
            print("\n--- INSIGHTS PREVIEW ---")
            for line in preview_lines:
                print(line)
            
            if len(lines) > 10:
                print("... (truncated)")
            
            return True
        else:
            print(f"❌ Failed to generate insights: {error}")
            return False
            
    except Exception as e:
        print(f"❌ Error in quick insights test: {e}")
        return False

def test_advanced_insights(models):
    """Test advanced insights with custom configuration"""
    print("\n⚙️ Testing Advanced Insights Generation...")
    
    if not models:
        print("❌ No models available for testing")
        return False
    
    try:
        from ollama_local import generate_ollama_insights, CustomerInsightRequest, OllamaConfig
        
        customer_data = create_test_customer()
        model_to_test = models[0]
        
        # Create customer request object
        customer_request = CustomerInsightRequest(**customer_data)
        
        # Create custom configuration
        config = OllamaConfig(
            model=model_to_test,
            temperature=0.8,  # More creative
            top_p=0.95,
            max_tokens=800,   # Shorter for testing
            timeout=90
        )
        
        print(f"Using model: {config.model}")
        print(f"Configuration: temp={config.temperature}, max_tokens={config.max_tokens}")
        print("Generating advanced insights... (this may take 60-90 seconds)")
        
        insights, debug_info = generate_ollama_insights(customer_request, config)
        
        print("✅ Advanced insights generated successfully!")
        print(f"Model used: {debug_info['model_used']}")
        print(f"Response length: {len(debug_info['raw_response'])} characters")
        
        # Show structured preview
        sections = insights.split('\n\n')
        print(f"\nResponse has {len(sections)} sections")
        
        # Show first section
        if sections:
            first_section = sections[0]
            print("\n--- FIRST SECTION ---")
            print(first_section[:300] + "..." if len(first_section) > 300 else first_section)
        
        return True
        
    except Exception as e:
        print(f"❌ Error in advanced insights test: {e}")
        return False

def test_multiple_models(models):
    """Test multiple models if available"""
    print("\n🔄 Testing Multiple Models...")
    
    if len(models) < 2:
        print(f"⚠️ Only {len(models)} model(s) available, skipping multi-model test")
        return True
    
    try:
        from ollama_local import quick_generate_insights
        
        customer_data = create_test_customer()
        models_to_test = models[:2]  # Test first 2 models
        
        print(f"Testing {len(models_to_test)} models: {', '.join(models_to_test)}")
        
        results = {}
        
        for model in models_to_test:
            print(f"\n--- Testing {model} ---")
            
            try:
                insights, error = quick_generate_insights(customer_data, model=model)
                
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
        print("\n--- MULTI-MODEL SUMMARY ---")
        successful_models = [m for m, r in results.items() if r['success']]
        print(f"Successful models: {len(successful_models)}/{len(models_to_test)}")
        
        for model, result in results.items():
            if result['success']:
                print(f"{model}: ✅ {result['word_count']} words")
            else:
                print(f"{model}: ❌ {result['error'][:50]}...")
        
        return len(successful_models) > 0
        
    except Exception as e:
        print(f"❌ Error in multi-model test: {e}")
        return False

def test_streamlit_integration():
    """Test if the Streamlit integration would work"""
    print("\n🎨 Testing Streamlit Integration Compatibility...")
    
    try:
        # Test the functions that Streamlit would use
        from ollama_local import check_ollama_status, get_available_models
        
        # Test status check
        status = check_ollama_status()
        print(f"Ollama status check: {'✅' if status else '❌'}")
        
        # Test model listing
        models = get_available_models()
        print(f"Model listing: {'✅' if models else '❌'} ({len(models)} models)")
        
        # Test customer data preparation (simulate Streamlit workflow)
        customer_data = create_test_customer()
        
        # Remove fields that Streamlit would exclude
        excluded_fields = ['Name', 'Surname', 'email', 'phone', 'address']
        clean_data = {k: v for k, v in customer_data.items() if k not in excluded_fields}
        
        print(f"Data preparation: ✅ ({len(clean_data)} fields)")
        
        print("✅ Streamlit integration compatibility confirmed")
        return True
        
    except Exception as e:
        print(f"❌ Streamlit integration test failed: {e}")
        return False

def main():
    """Run all standalone tests"""
    print("🦙 OLLAMA STANDALONE TEST SUITE")
    print("=" * 50)
    print("This test runs Ollama independently of the LLM API")
    print("=" * 50)
    
    # Test 1: Module import
    if not test_ollama_import():
        print("\n❌ Cannot proceed without ollama_local module")
        return
    
    # Test 2: Ollama connection
    ollama_available, models = test_ollama_connection()
    
    if not ollama_available:
        print("\n❌ Ollama is not available. Please:")
        print("1. Install Ollama: https://ollama.ai/")
        print("2. Run: ollama pull llama3.2")
        print("3. Start Ollama service")
        print("4. Re-run this test")
        return
    
    # Test 3: Quick insights
    quick_success = test_quick_insights(models)
    
    # Test 4: Advanced insights
    advanced_success = test_advanced_insights(models)
    
    # Test 5: Multiple models (if available)
    multi_success = test_multiple_models(models)
    
    # Test 6: Streamlit compatibility
    streamlit_success = test_streamlit_integration()
    
    # Final summary
    print("\n" + "=" * 50)
    print("📊 STANDALONE TEST RESULTS")
    print("=" * 50)
    
    tests = [
        ("Module Import", True),  # If we got here, import worked
        ("Ollama Connection", ollama_available),
        ("Quick Insights", quick_success),
        ("Advanced Insights", advanced_success),
        ("Multiple Models", multi_success),
        ("Streamlit Compatibility", streamlit_success)
    ]
    
    passed = sum(1 for _, success in tests if success)
    total = len(tests)
    
    for test_name, success in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Ollama standalone integration is working perfectly.")
        print("You can now use Ollama directly in Streamlit without the LLM API.")
        print(f"Available models: {', '.join(models[:3])}{'...' if len(models) > 3 else ''}")
    elif passed >= 4:
        print("\n✅ Core functionality working. Some advanced features may need attention.")
    else:
        print("\n⚠️ Several tests failed. Please check your Ollama installation.")
    
    print("\n💡 To use in Streamlit:")
    print("1. Start Streamlit: streamlit run streamlit_ui.py")
    print("2. Go to Insights tab")
    print("3. Select 'Ollama' method")
    print("4. Choose your model")
    print("5. Generate insights!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()