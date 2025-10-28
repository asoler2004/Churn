#!/usr/bin/env python3
"""
Simple Ollama Standalone Example

This example shows how to use Ollama directly for customer insights
without needing the LLM API running.
"""

def main():
    print("🦙 Ollama Standalone Example")
    print("=" * 40)
    
    # Check if Ollama module is available
    try:
        from ollama_local import quick_generate_insights, check_ollama_status, get_available_models
        print("✅ Ollama module loaded successfully")
    except ImportError:
        print("❌ Ollama module not found. Make sure ollama_local.py is available.")
        return
    
    # Check if Ollama is running
    if not check_ollama_status():
        print("❌ Ollama is not running. Please start Ollama first:")
        print("   1. Install Ollama: https://ollama.ai/")
        print("   2. Run: ollama pull llama3.2")
        print("   3. Start Ollama service")
        return
    
    # Get available models
    models = get_available_models()
    if not models:
        print("❌ No Ollama models found. Please install a model:")
        print("   ollama pull llama3.2")
        return
    
    print(f"✅ Ollama is running with {len(models)} models")
    print(f"Available models: {', '.join(models[:3])}{'...' if len(models) > 3 else ''}")
    
    # Sample customer data (high-risk customer)
    customer_data = {
        "age": 29,
        "housing": "r",  # Rented
        "credit_score": 580.0,  # Low credit score
        "deposits": 3,  # Low activity
        "withdrawal": 8,
        "purchases_partners": 5,
        "purchases": 12,
        "cc_taken": 0,  # No credit card
        "cc_recommended": 1,
        "cc_disliked": 1,  # Negative sentiment
        "cc_liked": 0,
        "cc_application_begin": 0,
        "app_downloaded": 0,  # No app
        "web_user": 1,
        "app_web_user": 0,
        "ios_user": 0,
        "android_user": 0,
        "registered_phones": 1,
        "payment_type": "weekly",  # Frequent payments (financial stress?)
        "waiting_4_loan": 0,
        "cancelled_loan": 1,  # Cancelled loan (red flag)
        "received_loan": 0,
        "rejected_loan": 0,
        "left_for_two_month_plus": 0,
        "left_for_one_month": 1,  # Inactive for 1 month
        "rewards_earned": 25,  # Very low rewards
        "reward_rate": 0.015,
        "is_referred": 0,
        "churn_probability": 0.78,  # High churn risk
        "churn_prediction": 1,
        "risk_level": "High"
    }
    
    print("\n📊 Customer Profile:")
    print(f"   Age: {customer_data['age']} years")
    print(f"   Credit Score: {customer_data['credit_score']}")
    print(f"   Churn Risk: {customer_data['risk_level']} ({customer_data['churn_probability']:.1%})")
    print(f"   Key Issues: No app, cancelled loan, inactive 1 month, low engagement")
    
    # Generate insights using the first available model
    model_to_use = models[0]
    print(f"\n🤖 Generating insights with {model_to_use}...")
    print("   (This may take 30-60 seconds)")
    
    try:
        insights, error = quick_generate_insights(customer_data, model=model_to_use)
        
        if insights:
            print("\n✅ Insights generated successfully!")
            print("=" * 50)
            
            # Extract and display key sections
            lines = insights.split('\n')
            current_section = ""
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                # Detect section headers
                if any(keyword in line.upper() for keyword in ['INSIGHTS', 'RECOMENDACIONES', 'ESTRATEGIA', 'ACCIONES']):
                    if current_section:
                        print()  # Add spacing between sections
                    current_section = line
                    print(f"\n{line}")
                    print("-" * len(line))
                elif line.startswith('•') or line.startswith('-') or line.startswith('1.') or line.startswith('2.'):
                    print(f"  {line}")
                elif current_section and len(line) > 20:  # Regular content
                    print(f"  {line}")
            
            print("\n" + "=" * 50)
            print("🎯 This demonstrates Ollama working independently!")
            print("   No LLM API required - direct connection to Ollama.")
            
        else:
            print(f"\n❌ Failed to generate insights: {error}")
            
    except Exception as e:
        print(f"\n❌ Error generating insights: {e}")
        print("   Make sure Ollama is running and the model is available.")

if __name__ == "__main__":
    main()