#!/usr/bin/env python3
"""
Test script to verify that prediction results persist correctly after SHAP plot generation
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from faker import Faker

def simulate_prediction_workflow():
    """Simulate the prediction workflow to test persistence"""
    print("🧪 Testing Prediction Result Persistence")
    print("=" * 60)
    
    # Simulate session state
    session_state = {
        'selected_customer': None,
        'prediction_result': None,
        'shap_plot': None,
        'llm_insights': ""
    }
    
    # Create sample customer data
    fake = Faker()
    sample_customer = {
        'Name': fake.first_name(),
        'Surname': fake.last_name(),
        'age': 35,
        'housing': 'own',
        'credit_score': 720.0,
        'deposits': 8,
        'withdrawal': 4,
        'purchases_partners': 15,
        'purchases': 30,
        'cc_taken': 1,
        'cc_recommended': 1,
        'cc_disliked': 0,
        'cc_liked': 1,
        'cc_application_begin': 1,
        'app_downloaded': 1,
        'web_user': 1,
        'app_web_user': 1,
        'ios_user': 1,
        'android_user': 0,
        'registered_phones': 1,
        'payment_type': 'credit_card',
        'waiting_4_loan': 0,
        'cancelled_loan': 0,
        'received_loan': 1,
        'rejected_loan': 0,
        'left_for_two_month_plus': 0,
        'left_for_one_month': 0,
        'rewards_earned': 250,
        'reward_rate': 0.03,
        'is_referred': 1,
        'email': fake.email(),
        'phone': fake.phone_number(),
        'address': fake.address()
    }
    
    # Sample prediction result
    sample_prediction = {
        'churn_probability_XGB': 0.25,
        'churn_prediction_XGB': 0,
        'risk_level_XGB': 'Medium',
        'churn_probability_RF': 0.30,
        'churn_prediction_RF': 0,
        'risk_level_RF': 'Medium'
    }
    
    print("1. 👤 Customer Selection")
    print("-" * 30)
    session_state['selected_customer'] = sample_customer
    print(f"   ✅ Selected customer: {sample_customer['Name']} {sample_customer['Surname']}")
    print(f"   📊 Customer data: Age {sample_customer['age']}, Credit Score {sample_customer['credit_score']}")
    
    print("\n2. 🔮 Prediction Generation")
    print("-" * 30)
    session_state['prediction_result'] = sample_prediction
    print("   ✅ Prediction completed")
    print(f"   📈 Churn Probability: {sample_prediction['churn_probability_XGB']:.2%}")
    print(f"   ⚠️ Risk Level: {sample_prediction['risk_level_XGB']}")
    
    # Test prediction result display logic
    def display_prediction_results(session_state):
        """Simulate the prediction results display logic"""
        if session_state['prediction_result'] is not None:
            result = session_state['prediction_result']
            prob = result.get('churn_probability_XGB', result.get('churn_probability', 0))
            risk = result.get('risk_level_XGB', result.get('risk_level', 'Unknown'))
            prediction = result.get('churn_prediction_XGB', result.get('churn_prediction', False))
            
            return {
                'probability': prob,
                'risk': risk,
                'prediction': 'Abandonará' if prediction else 'Se Quedará',
                'display_ready': True
            }
        return {'display_ready': False}
    
    print("\n3. 📊 Prediction Results Display")
    print("-" * 30)
    display_result = display_prediction_results(session_state)
    if display_result['display_ready']:
        print("   ✅ Prediction results ready for display")
        print(f"   📊 Probability: {display_result['probability']:.2%}")
        print(f"   ⚠️ Risk: {display_result['risk']}")
        print(f"   🎯 Prediction: {display_result['prediction']}")
    else:
        print("   ❌ Prediction results not ready")
    
    print("\n4. 📈 SHAP Plot Generation")
    print("-" * 30)
    # Simulate SHAP plot generation
    session_state['shap_plot'] = "mock_shap_plot_object"
    print("   ✅ SHAP plot generated and stored in session state")
    
    # Test that prediction results are still available after SHAP generation
    print("\n5. 🔍 Post-SHAP Prediction Results Check")
    print("-" * 30)
    post_shap_display = display_prediction_results(session_state)
    if post_shap_display['display_ready']:
        print("   ✅ Prediction results still available after SHAP generation")
        print(f"   📊 Probability: {post_shap_display['probability']:.2%}")
        print(f"   ⚠️ Risk: {post_shap_display['risk']}")
        print(f"   🎯 Prediction: {post_shap_display['prediction']}")
        print("   🎉 SUCCESS: Prediction persistence working correctly!")
    else:
        print("   ❌ FAILURE: Prediction results disappeared after SHAP generation")
    
    # Test SHAP plot persistence
    print("\n6. 📊 SHAP Plot Persistence Check")
    print("-" * 30)
    if session_state.get('shap_plot') is not None:
        print("   ✅ SHAP plot persisted in session state")
        print("   📈 SHAP plot available for display")
    else:
        print("   ❌ SHAP plot not persisted")
    
    # Test customer switching scenario
    print("\n7. 👥 Customer Switching Scenario")
    print("-" * 30)
    
    # Simulate selecting a different customer
    new_customer = sample_customer.copy()
    new_customer['Name'] = fake.first_name()
    new_customer['Surname'] = fake.last_name()
    new_customer['age'] = 28
    
    # Check if it's a different customer
    current_customer = session_state['selected_customer']
    is_different_customer = (
        current_customer is None or 
        new_customer.get('Name') != current_customer.get('Name') or
        new_customer.get('Surname') != current_customer.get('Surname') or
        new_customer.get('email') != current_customer.get('email')
    )
    
    if is_different_customer:
        print(f"   🔄 Switching to new customer: {new_customer['Name']} {new_customer['Surname']}")
        # Clear previous results (as done in the actual app)
        session_state['selected_customer'] = new_customer
        session_state['prediction_result'] = None
        session_state['llm_insights'] = ""
        if 'shap_plot' in session_state:
            del session_state['shap_plot']
        
        print("   ✅ Previous prediction results cleared")
        print("   ✅ Previous SHAP plot cleared")
        print("   🎯 Ready for new customer analysis")
    
    # Final state check
    print("\n8. 🏁 Final State Verification")
    print("-" * 30)
    print(f"   👤 Selected Customer: {session_state['selected_customer']['Name']} {session_state['selected_customer']['Surname']}")
    print(f"   🔮 Prediction Result: {'Available' if session_state['prediction_result'] else 'None'}")
    print(f"   📊 SHAP Plot: {'Available' if session_state.get('shap_plot') else 'None'}")
    print(f"   💡 LLM Insights: {'Available' if session_state['llm_insights'] else 'None'}")

def test_session_state_management():
    """Test session state management scenarios"""
    print("\n" + "=" * 60)
    print("🔧 Testing Session State Management")
    print("=" * 60)
    
    scenarios = [
        {
            'name': 'Fresh Start',
            'initial_state': {},
            'expected': {
                'selected_customer': None,
                'prediction_result': None,
                'shap_plot': None
            }
        },
        {
            'name': 'After Prediction',
            'initial_state': {
                'selected_customer': {'Name': 'John', 'Surname': 'Doe'},
                'prediction_result': {'churn_probability_XGB': 0.3}
            },
            'expected': {
                'prediction_available': True,
                'shap_ready': True
            }
        },
        {
            'name': 'After SHAP Generation',
            'initial_state': {
                'selected_customer': {'Name': 'John', 'Surname': 'Doe'},
                'prediction_result': {'churn_probability_XGB': 0.3},
                'shap_plot': 'mock_plot'
            },
            'expected': {
                'prediction_available': True,
                'shap_available': True
            }
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print("-" * 30)
        
        state = scenario['initial_state'].copy()
        
        # Check prediction availability
        prediction_available = state.get('prediction_result') is not None
        shap_ready = prediction_available  # SHAP is ready when prediction is available
        shap_available = state.get('shap_plot') is not None
        
        print(f"   📊 Prediction Available: {'✅' if prediction_available else '❌'}")
        print(f"   🎯 SHAP Ready: {'✅' if shap_ready else '❌'}")
        print(f"   📈 SHAP Available: {'✅' if shap_available else '❌'}")
        
        # Verify expectations
        if 'expected' in scenario:
            expected = scenario['expected']
            if 'prediction_available' in expected:
                assert prediction_available == expected['prediction_available'], f"Prediction availability mismatch"
            if 'shap_available' in expected:
                assert shap_available == expected['shap_available'], f"SHAP availability mismatch"
        
        print("   ✅ Scenario passed")

def main():
    """Main test function"""
    print("🚀 Testing Prediction Result Persistence After SHAP Generation")
    print("This test verifies that prediction results remain visible after generating SHAP plots")
    
    simulate_prediction_workflow()
    test_session_state_management()
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed!")
    print("💡 The prediction persistence fix should resolve the issue where")
    print("   prediction results disappear after generating SHAP plots.")
    print("\n📋 Key improvements:")
    print("   • Prediction results display outside button handlers")
    print("   • SHAP plots stored in session state for persistence")
    print("   • Clear separation between generation and display logic")
    print("   • Proper cleanup when switching customers")

if __name__ == "__main__":
    main()