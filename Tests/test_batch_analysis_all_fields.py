#!/usr/bin/env python3
"""
Test script to verify that run_batch_analysis includes all CSV fields in customer_result
"""

import pandas as pd
import numpy as np
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from streamlit_ui import run_batch_analysis, load_sample_data
    print("✅ Successfully imported batch analysis functions")
except ImportError as e:
    print(f"❌ Failed to import functions: {e}")
    sys.exit(1)

def test_all_fields_included():
    """Test that run_batch_analysis includes all fields from the CSV"""
    print("\n🧪 Testing All Fields Inclusion in Batch Analysis")
    print("=" * 60)
    
    # Load sample data
    sample_data = load_sample_data()
    
    # Take first 3 customers for testing
    test_customers = sample_data.head(3)
    
    print(f"Original data columns ({len(test_customers.columns)}):")
    for i, col in enumerate(test_customers.columns, 1):
        print(f"  {i:2d}. {col}")
    
    print(f"\nRunning batch analysis on {len(test_customers)} customers...")
    
    # Run batch analysis without predictions to focus on field inclusion
    try:
        # Mock the predict_churn function to avoid API dependency
        import streamlit_ui
        
        def mock_predict_churn(customer_data):
            return {
                'churn_probability_XGB': 0.5,
                'risk_level_XGB': 'Medium',
                'churn_prediction_XGB': 0,
                'churn_probability_RF': 0.4,
                'risk_level_RF': 'Medium'
            }, None
        
        # Temporarily replace the predict_churn function
        original_predict_churn = getattr(streamlit_ui, 'predict_churn', None)
        streamlit_ui.predict_churn = mock_predict_churn
        
        # Run batch analysis
        batch_results = run_batch_analysis(
            test_customers,
            include_predictions=True,
            include_insights=False,
            use_transformers=False
        )
        
        # Restore original function
        if original_predict_churn:
            streamlit_ui.predict_churn = original_predict_churn
        
        if batch_results is None:
            print("❌ Batch analysis returned None")
            return False
        
        print(f"\nBatch results columns ({len(batch_results.columns)}):")
        for i, col in enumerate(batch_results.columns, 1):
            print(f"  {i:2d}. {col}")
        
        # Check if all original columns are present
        original_columns = set(test_customers.columns)
        result_columns = set(batch_results.columns)
        
        # Remove prediction-specific columns for comparison
        prediction_columns = {
            'churn_probability_XGB', 'risk_level_XGB', 'churn_prediction_XGB',
            'churn_probability_RF', 'risk_level_RF', 'prediction_status'
        }
        result_columns_without_predictions = result_columns - prediction_columns
        
        missing_columns = original_columns - result_columns_without_predictions
        extra_columns = result_columns_without_predictions - original_columns
        
        print(f"\n📊 Field Comparison:")
        print(f"  Original CSV fields: {len(original_columns)}")
        print(f"  Result fields (excluding predictions): {len(result_columns_without_predictions)}")
        print(f"  Prediction fields added: {len(prediction_columns)}")
        print(f"  Total result fields: {len(result_columns)}")
        
        if missing_columns:
            print(f"\n❌ Missing columns from original data:")
            for col in sorted(missing_columns):
                print(f"    - {col}")
            return False
        
        if extra_columns:
            print(f"\n⚠️  Extra columns not in original data:")
            for col in sorted(extra_columns):
                print(f"    + {col}")
        
        # Verify data integrity for a sample customer
        print(f"\n🔍 Data Integrity Check (Customer 1):")
        original_customer = test_customers.iloc[0]
        result_customer = batch_results.iloc[0]
        
        integrity_issues = []
        for col in original_columns:
            if col in result_customer:
                original_val = original_customer[col]
                result_val = result_customer[col]
                
                # Handle NaN comparison
                if pd.isna(original_val) and pd.isna(result_val):
                    continue
                elif pd.isna(original_val) or pd.isna(result_val):
                    if not (pd.isna(original_val) and result_val in [0, 'N/A', 'Desconocido', 'Cliente']):
                        integrity_issues.append(f"    {col}: {original_val} → {result_val}")
                elif original_val != result_val:
                    # Allow for default value replacements
                    if not (pd.isna(original_val) and result_val in [0, 'N/A', 'Desconocido', 'Cliente']):
                        integrity_issues.append(f"    {col}: {original_val} → {result_val}")
        
        if integrity_issues:
            print(f"  ⚠️  Value changes detected:")
            for issue in integrity_issues[:5]:  # Show first 5 issues
                print(issue)
            if len(integrity_issues) > 5:
                print(f"    ... and {len(integrity_issues) - 5} more")
        else:
            print(f"  ✅ All values preserved correctly")
        
        # Check prediction fields
        prediction_fields_present = all(col in result_columns for col in prediction_columns)
        print(f"\n🤖 Prediction Fields:")
        print(f"  All prediction fields present: {'✅' if prediction_fields_present else '❌'}")
        
        if not missing_columns and prediction_fields_present:
            print(f"\n✅ SUCCESS: All original CSV fields included in batch results!")
            print(f"   - Original fields: {len(original_columns)} ✅")
            print(f"   - Prediction fields: {len(prediction_columns)} ✅") 
            print(f"   - Total fields: {len(result_columns)} ✅")
            return True
        else:
            print(f"\n❌ FAILURE: Some fields are missing from batch results")
            return False
            
    except Exception as e:
        print(f"❌ Error during batch analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_field_preservation_with_missing_data():
    """Test field preservation when some data is missing"""
    print("\n🧪 Testing Field Preservation with Missing Data")
    print("=" * 60)
    
    # Create test data with some missing values
    test_data = pd.DataFrame({
        'Name': ['Juan', 'María', None],
        'Surname': ['Pérez', None, 'López'],
        'email': ['juan@test.com', 'maria@test.com', None],
        'age': [30, None, 45],
        'credit_score': [650.5, 720.0, None],
        'housing': ['o', 'r', None],
        'app_downloaded': [1, 0, None],
        'purchases': [10, 15, None],
        'deposits': [5, 8, None],
        'custom_field': ['A', 'B', 'C'],  # Custom field to test preservation
        'another_field': [100, 200, 300]
    })
    
    print(f"Test data with missing values:")
    print(test_data.to_string())
    
    try:
        # Mock predict_churn for this test
        import streamlit_ui
        
        def mock_predict_churn(customer_data):
            return {
                'churn_probability_XGB': 0.3,
                'risk_level_XGB': 'Low',
                'churn_prediction_XGB': 0,
                'churn_probability_RF': 0.25,
                'risk_level_RF': 'Low'
            }, None
        
        original_predict_churn = getattr(streamlit_ui, 'predict_churn', None)
        streamlit_ui.predict_churn = mock_predict_churn
        
        # Run batch analysis
        batch_results = run_batch_analysis(
            test_data,
            include_predictions=True,
            include_insights=False,
            use_transformers=False
        )
        
        # Restore original function
        if original_predict_churn:
            streamlit_ui.predict_churn = original_predict_churn
        
        if batch_results is None:
            print("❌ Batch analysis returned None")
            return False
        
        print(f"\nBatch results:")
        print(batch_results.to_string())
        
        # Check that custom fields are preserved
        custom_fields = ['custom_field', 'another_field']
        custom_fields_preserved = all(field in batch_results.columns for field in custom_fields)
        
        print(f"\n📋 Custom Field Preservation:")
        for field in custom_fields:
            if field in batch_results.columns:
                print(f"  ✅ {field}: preserved")
                # Check values
                for i in range(len(test_data)):
                    original = test_data.iloc[i][field]
                    result = batch_results.iloc[i][field]
                    if original != result:
                        print(f"    ⚠️  Row {i}: {original} → {result}")
            else:
                print(f"  ❌ {field}: missing")
        
        # Check default value handling
        print(f"\n🔧 Default Value Handling:")
        for i in range(len(test_data)):
            print(f"  Row {i}:")
            if pd.isna(test_data.iloc[i]['Name']):
                result_name = batch_results.iloc[i]['Name']
                print(f"    Name: None → {result_name} {'✅' if result_name == 'Desconocido' else '❌'}")
            
            if pd.isna(test_data.iloc[i]['age']):
                result_age = batch_results.iloc[i]['age']
                print(f"    Age: None → {result_age} {'✅' if result_age == 0 else '❌'}")
        
        if custom_fields_preserved:
            print(f"\n✅ SUCCESS: Custom fields preserved with proper default handling!")
            return True
        else:
            print(f"\n❌ FAILURE: Some custom fields were not preserved")
            return False
            
    except Exception as e:
        print(f"❌ Error during missing data test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all batch analysis field tests"""
    print("🚀 Starting Batch Analysis Field Inclusion Tests")
    print("=" * 70)
    
    tests = [
        ("All Fields Inclusion", test_all_fields_included),
        ("Field Preservation with Missing Data", test_field_preservation_with_missing_data)
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
        print("🎉 All batch analysis field tests passed!")
        print("✅ run_batch_analysis now includes ALL CSV fields in results!")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)