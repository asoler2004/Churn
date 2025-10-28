#!/usr/bin/env python3
"""
Ollama Usage Examples for Fintech Churn Prediction System

This file demonstrates various ways to use the Ollama integration
for generating customer retention insights.
"""

import requests
import json
from typing import Dict, Any
from ollama_local import (
    quick_generate_insights,
    generate_ollama_insights,
    OllamaConfig,
    CustomerInsightRequest,
    test_ollama_connection,
    get_available_models,
    get_recommended_model
)

def example_1_basic_usage():
    """Example 1: Basic usage with default settings"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Ollama Usage")
    print("=" * 60)
    
    # Sample customer data
    customer_data = {
        "age": 28,
        "housing": "r",
        "credit_score": 680.0,
        "deposits": 12,
        "withdrawal": 6,
        "purchases_partners": 8,
        "purchases": 25,
        "cc_taken": 0,
        "cc_recommended": 1,
        "cc_disliked": 0,
        "cc_liked": 0,
        "cc_application_begin": 0,
        "app_downloaded": 1,
        "web_user": 1,
        "app_web_user": 1,
        "ios_user": 1,
        "android_user": 0,
        "registered_phones": 1,
        "payment_type": "monthly",
        "waiting_4_loan": 0,
        "cancelled_loan": 0,
        "received_loan": 0,
        "rejected_loan": 0,
        "left_for_two_month_plus": 0,
        "left_for_one_month": 1,  # Risk indicator
        "rewards_earned": 85,
        "reward_rate": 0.02,
        "is_referred": 1,
        "churn_probability": 0.65,  # High risk
        "churn_prediction": 1,
        "risk_level": "High"
    }
    
    print("Customer Profile: Young professional, high churn risk, inactive for 1 month")
    print(f"Churn Probability: {customer_data['churn_probability']:.1%}")
    print(f"Risk Level: {customer_data['risk_level']}")
    
    # Generate insights using quick function
    insights, error = quick_generate_insights(customer_data, model="llama3.2")
    
    if insights:
        print("\n✅ Insights Generated Successfully!")
        print("\n" + "="*50)
        print(insights[:500] + "..." if len(insights) > 500 else insights)
    else:
        print(f"\n❌ Error: {error}")

def example_2_advanced_configuration():
    """Example 2: Advanced configuration with custom settings"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Advanced Configuration")
    print("=" * 60)
    
    # High-value customer with medium risk
    customer_data = CustomerInsightRequest(
        age=45,
        housing="o",  # Owns home
        credit_score=780.0,
        deposits=25,
        withdrawal=8,
        purchases_partners=35,
        purchases=120,
        cc_taken=1,
        cc_recommended=1,
        cc_disliked=0,
        cc_liked=1,
        cc_application_begin=1,
        app_downloaded=1,
        web_user=1,
        app_web_user=1,
        ios_user=1,
        android_user=1,
        registered_phones=2,
        payment_type="monthly",
        waiting_4_loan=1,  # Waiting for loan
        cancelled_loan=0,
        received_loan=0,
        rejected_loan=0,
        left_for_two_month_plus=0,
        left_for_one_month=0,
        rewards_earned=850,
        reward_rate=0.035,
        is_referred=0,
        churn_probability=0.35,  # Medium risk
        churn_prediction=0,
        risk_level="Medium"
    )
    
    # Custom Ollama configuration
    config = OllamaConfig(
        model="llama3.1",  # Higher quality model
        temperature=0.8,   # More creative
        top_p=0.95,
        max_tokens=1200,   # Longer response
        timeout=90
    )
    
    print("Customer Profile: High-value customer, medium risk, waiting for loan")
    print(f"Credit Score: {customer_data.credit_score}")
    print(f"Rewards Earned: {customer_data.rewards_earned}")
    print(f"Model: {config.model}")
    
    try:
        insights, debug_info = generate_ollama_insights(customer_data, config)
        
        print("\n✅ Advanced Insights Generated!")
        print(f"Model Used: {debug_info['model_used']}")
        print(f"Response Length: {len(debug_info['raw_response'])} characters")
        print("\n" + "="*50)
        print(insights[:600] + "..." if len(insights) > 600 else insights)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

def example_3_batch_processing_simulation():
    """Example 3: Simulate batch processing with multiple customers"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Batch Processing Simulation")
    print("=" * 60)
    
    # Multiple customer scenarios
    customers = [
        {
            "name": "Young Professional - High Risk",
            "data": {
                "age": 26, "credit_score": 620, "churn_probability": 0.75,
                "risk_level": "High", "app_downloaded": 0, "cc_taken": 0,
                "left_for_one_month": 1, "purchases": 8, "rewards_earned": 25
            }
        },
        {
            "name": "Established Customer - Low Risk", 
            "data": {
                "age": 42, "credit_score": 750, "churn_probability": 0.15,
                "risk_level": "Low", "app_downloaded": 1, "cc_taken": 1,
                "left_for_one_month": 0, "purchases": 45, "rewards_earned": 650
            }
        },
        {
            "name": "Senior Customer - Medium Risk",
            "data": {
                "age": 58, "credit_score": 690, "churn_probability": 0.45,
                "risk_level": "Medium", "app_downloaded": 0, "cc_taken": 1,
                "left_for_one_month": 0, "purchases": 22, "rewards_earned": 180
            }
        }
    ]
    
    # Fill in default values for each customer
    default_values = {
        "housing": "r", "deposits": 10, "withdrawal": 5, "purchases_partners": 15,
        "cc_recommended": 1, "cc_disliked": 0, "cc_liked": 1, "cc_application_begin": 0,
        "web_user": 1, "app_web_user": 0, "ios_user": 1, "android_user": 0,
        "registered_phones": 1, "payment_type": "monthly", "waiting_4_loan": 0,
        "cancelled_loan": 0, "received_loan": 0, "rejected_loan": 0,
        "left_for_two_month_plus": 0, "reward_rate": 0.025, "is_referred": 0,
        "churn_prediction": 0
    }
    
    print(f"Processing {len(customers)} customers...")
    
    for i, customer in enumerate(customers, 1):
        print(f"\n--- Customer {i}: {customer['name']} ---")
        
        # Merge customer data with defaults
        full_data = {**default_values, **customer['data']}
        
        print(f"Age: {full_data['age']}, Credit: {full_data['credit_score']}, Risk: {full_data['risk_level']}")
        
        # Generate insights (using a faster model for batch processing)
        insights, error = quick_generate_insights(full_data, model="llama3.2")
        
        if insights:
            # Extract key recommendations (first few lines)
            lines = insights.split('\n')
            key_recommendations = []
            for line in lines:
                if line.strip() and ('•' in line or line.startswith('1.') or line.startswith('2.')):
                    key_recommendations.append(line.strip())
                    if len(key_recommendations) >= 3:
                        break
            
            print("Key Recommendations:")
            for rec in key_recommendations:
                print(f"  {rec}")
        else:
            print(f"  ❌ Error: {error}")

def example_4_model_comparison():
    """Example 4: Compare different models for the same customer"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Model Comparison")
    print("=" * 60)
    
    # Get available models
    available_models = get_available_models()
    
    if not available_models:
        print("❌ No Ollama models available for comparison")
        return
    
    print(f"Available models: {available_models}")
    
    # Test customer data
    customer_data = {
        "age": 35, "housing": "r", "credit_score": 650, "deposits": 15,
        "withdrawal": 7, "purchases_partners": 20, "purchases": 30,
        "cc_taken": 1, "cc_recommended": 1, "cc_disliked": 0, "cc_liked": 1,
        "cc_application_begin": 1, "app_downloaded": 1, "web_user": 1,
        "app_web_user": 1, "ios_user": 0, "android_user": 1,
        "registered_phones": 1, "payment_type": "monthly", "waiting_4_loan": 0,
        "cancelled_loan": 0, "received_loan": 1, "rejected_loan": 0,
        "left_for_two_month_plus": 0, "left_for_one_month": 0,
        "rewards_earned": 320, "reward_rate": 0.025, "is_referred": 1,
        "churn_probability": 0.25, "churn_prediction": 0, "risk_level": "Low"
    }
    
    # Test up to 3 models
    models_to_test = available_models[:3] if len(available_models) >= 3 else available_models
    
    print(f"\nTesting customer with {len(models_to_test)} models...")
    print("Customer: 35 years old, good credit, low churn risk")
    
    results = {}
    
    for model in models_to_test:
        print(f"\n--- Testing {model} ---")
        
        try:
            insights, error = quick_generate_insights(customer_data, model=model)
            
            if insights:
                # Analyze response characteristics
                word_count = len(insights.split())
                char_count = len(insights)
                
                results[model] = {
                    'success': True,
                    'word_count': word_count,
                    'char_count': char_count,
                    'preview': insights[:150] + "..." if len(insights) > 150 else insights
                }
                
                print(f"✅ Success - {word_count} words, {char_count} characters")
                print(f"Preview: {results[model]['preview']}")
                
            else:
                results[model] = {'success': False, 'error': error}
                print(f"❌ Failed: {error}")
                
        except Exception as e:
            results[model] = {'success': False, 'error': str(e)}
            print(f"❌ Exception: {e}")
    
    # Summary
    print("\n" + "="*40)
    print("MODEL COMPARISON SUMMARY:")
    print("="*40)
    
    for model, result in results.items():
        if result['success']:
            print(f"{model}: ✅ {result['word_count']} words")
        else:
            print(f"{model}: ❌ {result['error'][:50]}...")

def example_5_api_integration():
    """Example 5: Using the REST API directly"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: REST API Integration")
    print("=" * 60)
    
    # Check API health first
    try:
        health_response = requests.get("http://localhost:8001/health", timeout=5)
        if health_response.status_code == 200:
            health = health_response.json()
            print("✅ LLM API is running")
            print(f"Ollama available: {health.get('ollama_available', False)}")
            print(f"Available models: {health.get('ollama_model_count', 0)}")
        else:
            print("❌ LLM API not responding correctly")
            return
    except:
        print("❌ Cannot connect to LLM API")
        return
    
    # Sample customer data for API call
    api_data = {
        "age": 31,
        "housing": "o",
        "credit_score": 720.0,
        "deposits": 18,
        "withdrawal": 9,
        "purchases_partners": 25,
        "purchases": 55,
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
        "registered_phones": 2,
        "payment_type": "monthly",
        "waiting_4_loan": 0,
        "cancelled_loan": 0,
        "received_loan": 1,
        "rejected_loan": 0,
        "left_for_two_month_plus": 0,
        "left_for_one_month": 0,
        "rewards_earned": 450,
        "reward_rate": 0.03,
        "is_referred": 1,
        "churn_probability": 0.20,
        "churn_prediction": 0,
        "risk_level": "Low",
        "use_transformers": False,
        "use_ollama": True,
        "ollama_model": "llama3.2"
    }
    
    print("Making API call to generate insights...")
    print(f"Customer: {api_data['age']} years, {api_data['credit_score']} credit score")
    print(f"Using model: {api_data['ollama_model']}")
    
    try:
        response = requests.post(
            "http://localhost:8001/generate-insights",
            json=api_data,
            headers={"Content-Type": "application/json"},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print("\n✅ API call successful!")
            print(f"Recommendations length: {len(result['recommendations'])} chars")
            print(f"Key insights length: {len(result['key_insights'])} chars")
            print(f"Action items length: {len(result['action_items'])} chars")
            
            print("\n--- RECOMMENDATIONS ---")
            print(result['recommendations'][:300] + "..." if len(result['recommendations']) > 300 else result['recommendations'])
            
            if result.get('debug_raw_response'):
                print(f"\n--- DEBUG INFO ---")
                print(f"Raw response length: {len(result['debug_raw_response'])} chars")
                print(f"Model used: {api_data['ollama_model']}")
                
        else:
            print(f"❌ API call failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ API call error: {e}")

def main():
    """Run all examples"""
    print("🦙 OLLAMA USAGE EXAMPLES FOR FINTECH CHURN PREDICTION")
    print("=" * 70)
    
    # Check if Ollama is available
    status = test_ollama_connection()
    
    if not status['available']:
        print(f"❌ Ollama not available: {status['message']}")
        print("\nTo run these examples:")
        print("1. Install Ollama: https://ollama.ai/")
        print("2. Run: ollama pull llama3.2")
        print("3. Start Ollama service")
        print("4. Start LLM API: python llm_api.py")
        return
    
    print(f"✅ Ollama is available with {status['model_count']} models")
    print(f"Models: {', '.join(status['models'][:3])}{'...' if len(status['models']) > 3 else ''}")
    
    # Run examples
    try:
        example_1_basic_usage()
        example_2_advanced_configuration()
        example_3_batch_processing_simulation()
        example_4_model_comparison()
        example_5_api_integration()
        
        print("\n" + "=" * 70)
        print("🎉 All examples completed!")
        print("You can now use these patterns in your own applications.")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Examples interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error running examples: {e}")

if __name__ == "__main__":
    main()