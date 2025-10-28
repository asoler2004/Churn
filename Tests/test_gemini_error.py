#!/usr/bin/env python3
"""
Test to reproduce the Gemini error
"""

def test_gemini_direct():
    """Test the get_gemini_insights_direct function"""
    
    # Sample customer data
    customer_data = {
        'age': 35,
        'housing': 'r',
        'credit_score': 680.0,
        'deposits': 15,
        'withdrawal': 8,
        'purchases_partners': 20,
        'purchases': 30,
        'cc_taken': 1,
        'cc_recommended': 1,
        'cc_disliked': 0,
        'cc_liked': 1,
        'cc_application_begin': 1,
        'app_downloaded': 1,
        'web_user': 1,
        'app_web_user': 1,
        'ios_user': 0,
        'android_user': 1,
        'registered_phones': 1,
        'payment_type': 'monthly',
        'waiting_4_loan': 0,
        'cancelled_loan': 0,
        'received_loan': 1,
        'rejected_loan': 0,
        'left_for_two_month_plus': 0,
        'left_for_one_month': 0,
        'rewards_earned': 250,
        'reward_rate': 0.025,
        'is_referred': 1
    }
    
    # Sample prediction result
    prediction_result = {
        'churn_probability_XGB': 0.30,
        'churn_prediction_XGB': 0,
        'risk_level_XGB': 'Medium'
    }
    
    try:
        # Import the function
        from streamlit_ui import get_gemini_insights_direct
        
        print("🧪 Testing get_gemini_insights_direct...")
        
        # Call the function
        insights, error = get_gemini_insights_direct(customer_data, prediction_result, "gemini-2.5-flash")
        
        if insights:
            print("✅ Success! Insights generated:")
            print(insights[:200] + "..." if len(insights) > 200 else insights)
        else:
            print(f"❌ Error: {error}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini_direct()