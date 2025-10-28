#!/usr/bin/env python3
"""
Test script to verify that batch analysis properly handles separate insights
and that transformer responses are unique for different customers
"""

import pandas as pd
import numpy as np
import sys
import os
import time

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from streamlit_ui import run_batch_analysis, load_sample_data
    print("✅ Successfully imported batch analysis functions")
except ImportError as e:
    print(f"❌ Failed to import functions: {e}")
    sys.exit(1)

def test_separate_insights_generation():
    """Test that batch analysis generates separate rule-based and transformer insights"""
    print("\n🧪 Testing Separate Insights Generation")
    print("=" * 60)
    
    # Load sample data
    sample_data = load_sample_data()
    
    # Take first 3 customers for testing
    test_customers = sample_data.head(3)
    
    print(f"Testing with {len(test_customers)} customers...")
    
    # Mock the predict_churn function to avoid API dependency
    import streamlit_ui
    
    def mock_predict_churn(customer_data):
        # Generate varied predictions based on customer data
        age = customer_data.get('age', 30)
        credit_score = customer_data.get('credit_score', 650)
        
        # Create varied risk levels based on customer characteristics
        if credit_score < 600 or age > 60:
            risk_level = 'High'
            churn_prob = np.random.uniform(0.7, 0.9)
        elif credit_score > 750 and age < 40:
            risk_level = 'Low'
            churn_prob = np.random.uniform(0.1, 0.3)
        else:
            risk_level = 'Medium'
            churn_prob = np.random.uniform(0.3, 0.7)
        
        return {
            'churn_probability_XGB': churn_prob,
            'risk_level_XGB': risk_level,
            'churn_prediction_XGB': 1 if churn_prob > 0.5 else 0,
            'churn_probability_RF': churn_prob * 0.9,
            'risk_level_RF': risk_level
        }, None
    
    # Temporarily replace the predict_churn function
    original_predict_churn = getattr(streamlit_ui, 'predict_churn', None)
    streamlit_ui.predict_churn = mock_predict_churn
    
    try:
        # Test with both rule-based and transformer insights
        print("\n📊 Running batch analysis with both insight types...")
        
        batch_results = run_batch_analysis(
            test_customers,
            include_predictions=True,
            include_insights=True,
            use_transformers=True
        )
        
        if batch_results is None:
            print("❌ Batch analysis returned None")
            return False
        
        print(f"✅ Batch analysis completed for {len(batch_results)} customers")
        
        # Check for separate insights columns
        expected_columns = [
            'insights_rule_based',
            'insights_transformers', 
            'rule_based_status',
            'transformers_status',
            'insights_status'
        ]
        
        missing_columns = []
        for col in expected_columns:
            if col not in batch_results.columns:
                missing_columns.append(col)
        
        if missing_columns:
            print(f"❌ Missing expected columns: {missing_columns}")
            return False
        
        print("✅ All expected insights columns present")
        
        # Check content of insights
        print(f"\n📋 Insights Content Analysis:")
        
        for idx, row in batch_results.iterrows():
            customer_name = f"{row.get('Name', 'Cliente')} {row.get('Surname', '')}"
            print(f"\nCustomer {idx + 1}: {customer_name}")
            
            # Rule-based insights
            rule_insights = row['insights_rule_based']
            rule_status = row['rule_based_status']
            print(f"  Rule-based: {rule_status} ({len(str(rule_insights))} chars)")
            
            # Transformer insights
            transformer_insights = row['insights_transformers']
            transformer_status = row['transformers_status']
            print(f"  Transformers: {transformer_status} ({len(str(transformer_insights))} chars)")
            
            # Check that insights are not truncated
            if rule_status == 'Success' and len(str(rule_insights)) < 100:
                print(f"  ⚠️  Rule-based insights seem too short")
            
            if transformer_status == 'Success' and len(str(transformer_insights)) < 100:
                print(f"  ⚠️  Transformer insights seem too short")
        
        # Check for uniqueness in transformer responses
        transformer_insights_list = []
        for idx, row in batch_results.iterrows():
            if row['transformers_status'] == 'Success':
                transformer_insights_list.append(row['insights_transformers'])
        
        if len(transformer_insights_list) > 1:
            # Check if all transformer insights are identical
            all_identical = all(insight == transformer_insights_list[0] for insight in transformer_insights_list)
            
            if all_identical:
                print(f"\n⚠️  WARNING: All transformer insights are identical!")
                print(f"First insight preview: {transformer_insights_list[0][:200]}...")
                return False
            else:
                print(f"\n✅ Transformer insights show variation across customers")
        
        print(f"\n✅ SUCCESS: Separate insights generation working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error during batch analysis: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Restore original function
        if original_predict_churn:
            streamlit_ui.predict_churn = original_predict_churn

def test_insights_without_truncation():
    """Test that insights are not truncated in the new implementation"""
    print("\n🧪 Testing Insights Without Truncation")
    print("=" * 60)
    
    # Create test data
    test_data = pd.DataFrame({
        'Name': ['Ana', 'Carlos', 'María'],
        'Surname': ['García', 'López', 'Martínez'],
        'email': ['ana@test.com', 'carlos@test.com', 'maria@test.com'],
        'age': [25, 45, 35],
        'credit_score': [580, 720, 650],
        'housing': ['r', 'o', 'r'],
        'app_downloaded': [0, 1, 1],
        'purchases': [5, 20, 15],
        'deposits': [2, 8, 5],
        'withdrawal': [3, 2, 4],
        'purchases_partners': [1, 5, 3],
        'cc_taken': [0, 1, 0],
        'cc_recommended': [1, 0, 1],
        'cc_disliked': [1, 0, 0],
        'cc_liked': [0, 1, 1],
        'cc_application_begin': [0, 0, 1],
        'web_user': [1, 1, 1],
        'app_web_user': [0, 1, 1],
        'ios_user': [0, 1, 0],
        'android_user': [1, 0, 1],
        'registered_phones': [1, 1, 2],
        'payment_type': ['monthly', 'bi-weekly', 'monthly'],
        'waiting_4_loan': [0, 0, 0],
        'cancelled_loan': [0, 0, 0],
        'received_loan': [0, 1, 0],
        'rejected_loan': [1, 0, 0],
        'left_for_two_month_plus': [0, 0, 0],
        'left_for_one_month': [1, 0, 0],
        'rewards_earned': [25, 150, 75],
        'reward_rate': [0.01, 0.03, 0.02],
        'is_referred': [0, 1, 0],
        'zodiac_sign': ['leo', 'aries', 'gemini']
    })
    
    print(f"Testing truncation with {len(test_data)} customers...")
    
    # Mock predict_churn with varied results
    import streamlit_ui
    
    def mock_predict_churn_varied(customer_data):
        name = customer_data.get('Name', 'Cliente')
        
        # Create different risk profiles for each customer
        risk_profiles = {
            'Ana': ('High', 0.82),
            'Carlos': ('Low', 0.18),
            'María': ('Medium', 0.45)
        }
        
        risk_level, churn_prob = risk_profiles.get(name, ('Medium', 0.5))
        
        return {
            'churn_probability_XGB': churn_prob,
            'risk_level_XGB': risk_level,
            'churn_prediction_XGB': 1 if churn_prob > 0.5 else 0,
            'churn_probability_RF': churn_prob * 0.9,
            'risk_level_RF': risk_level
        }, None
    
    original_predict_churn = getattr(streamlit_ui, 'predict_churn', None)
    streamlit_ui.predict_churn = mock_predict_churn_varied
    
    try:
        # Run batch analysis
        batch_results = run_batch_analysis(
            test_data,
            include_predictions=True,
            include_insights=True,
            use_transformers=False  # Only test rule-based for truncation
        )
        
        if batch_results is None:
            print("❌ Batch analysis returned None")
            return False
        
        print(f"✅ Batch analysis completed")
        
        # Check for truncation indicators
        truncation_found = False
        
        for idx, row in batch_results.iterrows():
            rule_insights = str(row.get('insights_rule_based', ''))
            
            # Check for truncation indicators
            if '...' in rule_insights and len(rule_insights) < 250:
                print(f"❌ Customer {idx + 1}: Insights appear to be truncated")
                print(f"   Content: {rule_insights}")
                truncation_found = True
            elif len(rule_insights) > 200:
                print(f"✅ Customer {idx + 1}: Full insights preserved ({len(rule_insights)} chars)")
            
        if not truncation_found:
            print(f"\n✅ SUCCESS: No truncation detected in insights!")
            return True
        else:
            print(f"\n❌ FAILURE: Truncation detected in some insights")
            return False
            
    except Exception as e:
        print(f"❌ Error during truncation test: {e}")
        return False
    
    finally:
        if original_predict_churn:
            streamlit_ui.predict_churn = original_predict_churn

def test_export_with_separate_insights():
    """Test that export includes both types of insights"""
    print("\n🧪 Testing Export with Separate Insights")
    print("=" * 60)
    
    # Create mock batch results with separate insights
    mock_results = pd.DataFrame({
        'Name': ['Test1', 'Test2'],
        'Surname': ['Customer1', 'Customer2'],
        'age': [30, 40],
        'credit_score': [650, 720],
        'churn_probability_XGB': [0.6, 0.3],
        'risk_level_XGB': ['High', 'Low'],
        'insights_rule_based': [
            'INSIGHTS CLAVE:\n• Cliente de alto riesgo\n\nRECOMENDACIONES:\n• Contacto inmediato\n\nACCIONES:\n• Llamar en 24h',
            'INSIGHTS CLAVE:\n• Cliente estable\n\nRECOMENDACIONES:\n• Mantener satisfacción\n\nACCIONES:\n• Seguimiento mensual'
        ],
        'insights_transformers': [
            'ANÁLISIS IA:\nEste cliente requiere atención urgente debido a su alto riesgo de abandono...',
            'ANÁLISIS IA:\nCliente con buen perfil, enfocarse en fidelización y productos premium...'
        ],
        'rule_based_status': ['Success', 'Success'],
        'transformers_status': ['Success', 'Success']
    })
    
    try:
        from streamlit_ui import prepare_batch_results_for_export
        
        # Test export
        csv_export = prepare_batch_results_for_export(mock_results)
        
        print(f"✅ Export generated ({len(csv_export)} characters)")
        
        # Check that both insight types are in export
        if 'insights_rule_based' in csv_export and 'insights_transformers' in csv_export:
            print("✅ Both insight types present in export")
        else:
            print("❌ Missing insight types in export")
            return False
        
        # Check that full content is preserved
        lines = csv_export.split('\n')
        if len(lines) > 2:  # Header + 2 data rows
            sample_row = lines[1]  # First data row
            if len(sample_row) > 200:  # Should be substantial with full insights
                print("✅ Full content appears to be preserved in export")
            else:
                print("⚠️  Export content seems short, may be truncated")
        
        print(f"\n✅ SUCCESS: Export with separate insights working!")
        return True
        
    except Exception as e:
        print(f"❌ Error during export test: {e}")
        return False

def main():
    """Run all batch analysis insights tests"""
    print("🚀 Starting Batch Analysis Insights Fix Tests")
    print("=" * 70)
    
    tests = [
        ("Separate Insights Generation", test_separate_insights_generation),
        ("Insights Without Truncation", test_insights_without_truncation),
        ("Export with Separate Insights", test_export_with_separate_insights)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            if result:
                print(f"✅ {test_name} PASSED")
                passed += 1
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "="*70)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All batch analysis insights tests passed!")
        print("✅ Separate insights generation working correctly!")
        print("✅ No truncation in insights!")
        print("✅ Transformer responses should be unique!")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)