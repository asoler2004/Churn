#!/usr/bin/env python3
"""
Test script to verify customer selection functionality
"""

import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker

# Initialize Faker
fake = Faker()

def create_test_data():
    """Create test customer data"""
    np.random.seed(42)
    n_samples = 10
    
    data = {
        "Name": [fake.first_name() for _ in range(n_samples)],
        "Surname": [fake.last_name() for _ in range(n_samples)],
        "age": np.random.randint(18, 80, n_samples),
        "credit_score": np.random.normal(650, 100, n_samples).clip(300, 850),
        "housing": np.random.choice(["own", "rent", "mortgage"], n_samples),
        "deposits": np.random.poisson(5, n_samples),
        "purchases": np.random.poisson(25, n_samples),
        "app_downloaded": np.random.binomial(1, 0.7, n_samples),
        "email": [fake.email() for _ in range(n_samples)]
    }
    
    return pd.DataFrame(data)

def test_customer_selection():
    """Test customer selection logic"""
    print("🧪 Testing Customer Selection Logic")
    print("=" * 50)
    
    # Create test data
    df = create_test_data()
    print(f"✅ Created test data with {len(df)} customers")
    
    # Simulate AgGrid response formats
    test_cases = [
        # Case 1: DataFrame response (newer AgGrid versions)
        {
            "name": "DataFrame Response",
            "selected_rows": df.iloc[[0]],  # Single row DataFrame
            "expected": True
        },
        # Case 2: List response (older AgGrid versions)
        {
            "name": "List Response", 
            "selected_rows": [df.iloc[0].to_dict()],  # List with dict
            "expected": True
        },
        # Case 3: Empty selection
        {
            "name": "Empty Selection",
            "selected_rows": [],
            "expected": False
        },
        # Case 4: None response
        {
            "name": "None Response",
            "selected_rows": None,
            "expected": False
        }
    ]
    
    for case in test_cases:
        print(f"\\n🔍 Testing: {case['name']}")
        selected_rows = case['selected_rows']
        
        # Test the selection logic
        try:
            # Check if selected_rows is a DataFrame or list
            if isinstance(selected_rows, pd.DataFrame):
                has_selection = not selected_rows.empty
                selected_data = selected_rows.iloc[0].to_dict() if has_selection else None
                print(f"   📊 DataFrame format detected, has_selection: {has_selection}")
            elif isinstance(selected_rows, list):
                has_selection = len(selected_rows) > 0
                selected_data = selected_rows[0] if has_selection else None
                print(f"   📋 List format detected, has_selection: {has_selection}")
            else:
                has_selection = False
                selected_data = None
                print(f"   ❌ No valid selection format")
            
            if has_selection and selected_data:
                # Convert pandas/numpy types to native Python types
                clean_customer = {}
                for key, value in selected_data.items():
                    if pd.isna(value):
                        clean_customer[key] = None
                    elif isinstance(value, (np.integer, np.floating)):
                        clean_customer[key] = value.item()
                    elif isinstance(value, np.bool_):
                        clean_customer[key] = bool(value)
                    else:
                        clean_customer[key] = value
                
                name = clean_customer.get('Name', 'Unknown')
                surname = clean_customer.get('Surname', 'Customer')
                print(f"   ✅ Successfully processed: {name} {surname}")
                
                result = True
            else:
                print(f"   ℹ️ No customer selected")
                result = False
            
            # Check if result matches expected
            if result == case['expected']:
                print(f"   ✅ Test PASSED")
            else:
                print(f"   ❌ Test FAILED - Expected: {case['expected']}, Got: {result}")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
    
    print("\\n🎯 Customer Selection Test Complete!")

if __name__ == "__main__":
    test_customer_selection()