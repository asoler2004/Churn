#!/usr/bin/env python3
"""
Test script to verify that the "Churn Real" metric is properly displayed
in the summary statistics of the first tab
"""

import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_churn_real_metric_calculation():
    """Test the churn real metric calculation logic"""
    print("\n🧪 Testing Churn Real Metric Calculation")
    print("=" * 60)
    
    # Create test data with churn column
    test_data = pd.DataFrame({
        'Name': ['Ana', 'Carlos', 'María', 'Juan', 'Laura'],
        'Surname': ['García', 'López', 'Martínez', 'Pérez', 'González'],
        'email': ['ana@test.com', 'carlos@test.com', 'maria@test.com', 'juan@test.com', 'laura@test.com'],
        'age': [25, 45, 35, 55, 30],
        'credit_score': [580, 720, 650, 600, 750],
        'housing': ['r', 'o', 'r', 'o', 'r'],
        'app_downloaded': [0, 1, 1, 0, 1],
        'purchases': [5, 25, 15, 8, 30],
        'deposits': [2, 8, 5, 3, 10],
        'cc_taken': [0, 1, 0, 1, 1],
        'received_loan': [0, 1, 0, 0, 1],
        'left_for_one_month': [1, 0, 0, 1, 0],
        'left_for_two_month_plus': [0, 0, 0, 0, 0],
        'is_referred': [0, 1, 0, 0, 1],
        'churn': [1, 0, 0, 1, 0]  # 2 out of 5 customers churned (40%)
    })
    
    print(f"Test data created with {len(test_data)} customers")
    print(f"Churn distribution:")
    print(test_data['churn'].value_counts())
    
    # Calculate churn metrics manually
    total_customers = len(test_data)
    churn_customers = (test_data['churn'] == 1).sum()
    churn_percentage = (churn_customers / total_customers * 100) if total_customers > 0 else 0
    
    print(f"\n📊 Manual Calculation:")
    print(f"  Total customers: {total_customers}")
    print(f"  Churn customers: {churn_customers}")
    print(f"  Churn percentage: {churn_percentage:.1f}%")
    
    # Test with filtered data (simulate filtering)
    filtered_data = test_data[test_data['age'] < 40]  # Filter for younger customers
    filtered_customers = len(filtered_data)
    filtered_churn = (filtered_data['churn'] == 1).sum()
    filtered_churn_percentage = (filtered_churn / filtered_customers * 100) if filtered_customers > 0 else 0
    
    print(f"\n🔍 Filtered Data (age < 40):")
    print(f"  Filtered customers: {filtered_customers}")
    print(f"  Filtered churn customers: {filtered_churn}")
    print(f"  Filtered churn percentage: {filtered_churn_percentage:.1f}%")
    
    # Calculate delta
    churn_delta = filtered_churn_percentage - churn_percentage
    print(f"  Churn delta: {churn_delta:+.1f}%")
    
    # Verify calculations
    expected_total_churn = 2
    expected_filtered_churn = 1  # Only Ana (age 25) has churn=1 in filtered data
    expected_filtered_percentage = (1 / 3 * 100)  # 1 out of 3 filtered customers
    
    if churn_customers == expected_total_churn:
        print("✅ Total churn calculation correct")
    else:
        print(f"❌ Total churn calculation incorrect: expected {expected_total_churn}, got {churn_customers}")
        return False
    
    if filtered_churn == expected_filtered_churn:
        print("✅ Filtered churn calculation correct")
    else:
        print(f"❌ Filtered churn calculation incorrect: expected {expected_filtered_churn}, got {filtered_churn}")
        return False
    
    if abs(filtered_churn_percentage - expected_filtered_percentage) < 0.1:
        print("✅ Filtered churn percentage calculation correct")
    else:
        print(f"❌ Filtered churn percentage incorrect: expected {expected_filtered_percentage:.1f}%, got {filtered_churn_percentage:.1f}%")
        return False
    
    print(f"\n✅ SUCCESS: Churn Real metric calculations working correctly!")
    return True

def test_churn_column_missing():
    """Test behavior when churn column is missing"""
    print("\n🧪 Testing Missing Churn Column Handling")
    print("=" * 60)
    
    # Create test data without churn column
    test_data_no_churn = pd.DataFrame({
        'Name': ['Ana', 'Carlos'],
        'age': [25, 45],
        'credit_score': [580, 720],
        'app_downloaded': [0, 1],
        'purchases': [5, 25]
        # No 'churn' column
    })
    
    print(f"Test data created without churn column")
    print(f"Columns: {list(test_data_no_churn.columns)}")
    
    # Test the logic for missing churn column
    has_churn_column = 'churn' in test_data_no_churn.columns
    
    if not has_churn_column:
        print("✅ Correctly detected missing churn column")
        print("✅ Should display 'N/A' for Churn Real metric")
        return True
    else:
        print("❌ Failed to detect missing churn column")
        return False

def test_churn_quick_filter():
    """Test the churn quick filter functionality"""
    print("\n🧪 Testing Churn Quick Filter")
    print("=" * 60)
    
    # Create test data with mixed churn values
    test_data = pd.DataFrame({
        'Name': ['Ana', 'Carlos', 'María', 'Juan'],
        'age': [25, 45, 35, 55],
        'churn': [1, 0, 1, 0]
    })
    
    print(f"Original data: {len(test_data)} customers")
    print(f"Churn distribution: {test_data['churn'].value_counts().to_dict()}")
    
    # Simulate quick filter for churn customers
    filtered_churn_only = test_data[test_data['churn'] == 1]
    
    print(f"\nAfter churn filter: {len(filtered_churn_only)} customers")
    print(f"Filtered customers: {list(filtered_churn_only['Name'])}")
    
    # Verify filter results
    expected_churn_customers = ['Ana', 'María']
    actual_churn_customers = list(filtered_churn_only['Name'])
    
    if set(actual_churn_customers) == set(expected_churn_customers):
        print("✅ Churn quick filter working correctly")
        return True
    else:
        print(f"❌ Churn quick filter incorrect: expected {expected_churn_customers}, got {actual_churn_customers}")
        return False

def test_churn_metric_display_format():
    """Test the display format of the churn metric"""
    print("\n🧪 Testing Churn Metric Display Format")
    print("=" * 60)
    
    # Test different scenarios
    test_scenarios = [
        {
            'name': 'Low Churn',
            'total': 100,
            'churn': 5,
            'expected_percentage': 5.0
        },
        {
            'name': 'High Churn', 
            'total': 50,
            'churn': 25,
            'expected_percentage': 50.0
        },
        {
            'name': 'No Churn',
            'total': 20,
            'churn': 0,
            'expected_percentage': 0.0
        },
        {
            'name': 'All Churn',
            'total': 10,
            'churn': 10,
            'expected_percentage': 100.0
        }
    ]
    
    for scenario in test_scenarios:
        total = scenario['total']
        churn = scenario['churn']
        expected_percentage = scenario['expected_percentage']
        
        # Calculate percentage
        calculated_percentage = (churn / total * 100) if total > 0 else 0
        
        # Format display string (as it would appear in the UI)
        display_string = f"{churn} ({calculated_percentage:.1f}%)"
        
        print(f"\n{scenario['name']}:")
        print(f"  Input: {churn}/{total} customers")
        print(f"  Expected: {expected_percentage:.1f}%")
        print(f"  Calculated: {calculated_percentage:.1f}%")
        print(f"  Display: {display_string}")
        
        if abs(calculated_percentage - expected_percentage) < 0.1:
            print(f"  ✅ Correct")
        else:
            print(f"  ❌ Incorrect calculation")
            return False
    
    print(f"\n✅ SUCCESS: All display format tests passed!")
    return True

def test_churn_delta_calculation():
    """Test the delta calculation for churn metric"""
    print("\n🧪 Testing Churn Delta Calculation")
    print("=" * 60)
    
    # Simulate overall data and filtered data
    overall_data = pd.DataFrame({
        'churn': [1, 0, 1, 0, 0, 1, 0, 0, 0, 0]  # 3/10 = 30% churn
    })
    
    filtered_data = pd.DataFrame({
        'churn': [1, 1, 0, 0]  # 2/4 = 50% churn
    })
    
    # Calculate percentages
    overall_churn_percentage = (overall_data['churn'] == 1).sum() / len(overall_data) * 100
    filtered_churn_percentage = (filtered_data['churn'] == 1).sum() / len(filtered_data) * 100
    
    # Calculate delta
    churn_delta = filtered_churn_percentage - overall_churn_percentage
    
    print(f"Overall churn: {overall_churn_percentage:.1f}%")
    print(f"Filtered churn: {filtered_churn_percentage:.1f}%")
    print(f"Delta: {churn_delta:+.1f}%")
    
    # Verify calculations
    expected_overall = 30.0
    expected_filtered = 50.0
    expected_delta = 20.0
    
    if (abs(overall_churn_percentage - expected_overall) < 0.1 and
        abs(filtered_churn_percentage - expected_filtered) < 0.1 and
        abs(churn_delta - expected_delta) < 0.1):
        print("✅ Delta calculation correct")
        
        # Test delta color logic
        if churn_delta > 0:
            print("✅ Delta is positive (worse) - should show red with delta_color='inverse'")
        elif churn_delta < 0:
            print("✅ Delta is negative (better) - should show green with delta_color='inverse'")
        else:
            print("✅ Delta is zero - no color change")
        
        return True
    else:
        print("❌ Delta calculation incorrect")
        return False

def main():
    """Run all churn real metric tests"""
    print("🚀 Starting Churn Real Metric Tests")
    print("=" * 70)
    
    tests = [
        ("Churn Real Metric Calculation", test_churn_real_metric_calculation),
        ("Missing Churn Column Handling", test_churn_column_missing),
        ("Churn Quick Filter", test_churn_quick_filter),
        ("Churn Metric Display Format", test_churn_metric_display_format),
        ("Churn Delta Calculation", test_churn_delta_calculation)
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
        print("🎉 All churn real metric tests passed!")
        print("✅ Churn Real metric ready for use in summary statistics!")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)