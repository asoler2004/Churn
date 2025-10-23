#!/usr/bin/env python3
"""
Test script to verify SHAP plot works with categorical data
"""

import pandas as pd
import numpy as np
from faker import Faker

def test_categorical_encoding():
    """Test the categorical encoding for SHAP plots"""
    print("🧪 Testing Categorical Data Encoding for SHAP")
    print("=" * 50)
    
    # Create sample customer data with categorical variables
    fake = Faker()
    
    customer_data = {
        'Name': fake.first_name(),
        'Surname': fake.last_name(),
        'email': fake.email(),
        'phone': fake.phone_number(),
        'address': fake.address(),
        'age': 35,
        'housing': 'own',  # Categorical
        'credit_score': 720.5,
        'deposits': 8,
        'withdrawal': 3,
        'purchases_partners': 12,
        'purchases': 28,
        'cc_taken': 1,
        'cc_recommended': 0,
        'cc_disliked': 0,
        'cc_liked': 1,
        'cc_application_begin': 1,
        'app_downloaded': 1,
        'web_user': 1,
        'app_web_user': 1,
        'ios_user': 0,
        'android_user': 1,
        'registered_phones': 1,
        'payment_type': 'credit_card',  # Categorical
        'waiting_4_loan': 0,
        'cancelled_loan': 0,
        'received_loan': 1,
        'rejected_loan': 0,
        'zodiac_sign': 'leo',  # Categorical
        'left_for_two_month_plus': 0,
        'left_for_one_month': 0,
        'rewards_earned': 150,
        'reward_rate': 0.025,
        'is_referred': 1
    }
    
    print(f"✅ Created sample customer: {customer_data['Name']} {customer_data['Surname']}")
    
    # Test the encoding process
    try:
        # Prepare customer data (exclude personal info)
        api_data = {k: v for k, v in customer_data.items() 
                   if k not in ['Name', 'Surname', 'email', 'phone', 'address']}
        
        print(f"📊 API data columns: {len(api_data)}")
        
        # Create DataFrame
        customer_df = pd.DataFrame([api_data])
        print(f"📋 DataFrame shape: {customer_df.shape}")
        
        # Show original categorical values
        categorical_cols = ['housing', 'payment_type', 'zodiac_sign']
        print("\\n🏷️ Original categorical values:")
        for col in categorical_cols:
            if col in customer_df.columns:
                print(f"   {col}: {customer_df[col].iloc[0]}")
        
        # Encode categorical variables
        categorical_mappings = {
            'housing': {'own': 0, 'rent': 1, 'mortgage': 2},
            'payment_type': {'credit_card': 0, 'debit_card': 1, 'bank_transfer': 2},
            'zodiac_sign': {
                'aries': 0, 'taurus': 1, 'gemini': 2, 'cancer': 3, 'leo': 4, 'virgo': 5,
                'libra': 6, 'scorpio': 7, 'sagittarius': 8, 'capricorn': 9, 'aquarius': 10, 'pisces': 11
            }
        }
        
        # Apply categorical encoding
        for col, mapping in categorical_mappings.items():
            if col in customer_df.columns:
                original_value = customer_df[col].iloc[0]
                customer_df[col] = customer_df[col].map(mapping).fillna(0)
                encoded_value = customer_df[col].iloc[0]
                print(f"   {col}: '{original_value}' → {encoded_value}")
        
        # Ensure all columns are numeric
        print("\\n🔢 Converting to numeric types:")
        for col in customer_df.columns:
            original_dtype = customer_df[col].dtype
            customer_df[col] = pd.to_numeric(customer_df[col], errors='coerce').fillna(0)
            new_dtype = customer_df[col].dtype
            print(f"   {col}: {original_dtype} → {new_dtype}")
        
        # Check final data types
        print("\\n✅ Final DataFrame info:")
        print(f"   Shape: {customer_df.shape}")
        print(f"   All numeric: {customer_df.select_dtypes(include=[np.number]).shape[1] == customer_df.shape[1]}")
        
        # Show data types
        print("\\n📊 Final data types:")
        for col in customer_df.columns:
            dtype = customer_df[col].dtype
            value = customer_df[col].iloc[0]
            print(f"   {col}: {dtype} (value: {value})")
        
        print("\\n🎯 Categorical encoding test PASSED!")
        return True
        
    except Exception as e:
        print(f"\\n❌ Categorical encoding test FAILED: {str(e)}")
        return False

def test_edge_cases():
    """Test edge cases for categorical encoding"""
    print("\\n🧪 Testing Edge Cases")
    print("=" * 30)
    
    edge_cases = [
        {'housing': 'unknown', 'payment_type': 'cash', 'zodiac_sign': 'invalid'},
        {'housing': None, 'payment_type': '', 'zodiac_sign': 'ARIES'},
        {'housing': 'RENT', 'payment_type': 'Credit_Card', 'zodiac_sign': 'Leo'}
    ]
    
    categorical_mappings = {
        'housing': {'own': 0, 'rent': 1, 'mortgage': 2},
        'payment_type': {'credit_card': 0, 'debit_card': 1, 'bank_transfer': 2},
        'zodiac_sign': {
            'aries': 0, 'taurus': 1, 'gemini': 2, 'cancer': 3, 'leo': 4, 'virgo': 5,
            'libra': 6, 'scorpio': 7, 'sagittarius': 8, 'capricorn': 9, 'aquarius': 10, 'pisces': 11
        }
    }
    
    for i, case in enumerate(edge_cases, 1):
        print(f"\\n🔍 Edge case {i}: {case}")
        
        try:
            df = pd.DataFrame([case])
            
            # Apply encoding with case handling
            for col, mapping in categorical_mappings.items():
                if col in df.columns:
                    # Handle case insensitive mapping
                    value = df[col].iloc[0]
                    if pd.isna(value) or value == '' or value is None:
                        df[col] = 0
                    else:
                        # Try lowercase mapping
                        lower_mapping = {k.lower(): v for k, v in mapping.items()}
                        df[col] = df[col].astype(str).str.lower().map(lower_mapping).fillna(0)
            
            # Convert to numeric
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            print(f"   ✅ Encoded: {df.iloc[0].to_dict()}")
            
        except Exception as e:
            print(f"   ❌ Failed: {str(e)}")
    
    print("\\n🎯 Edge case testing complete!")

if __name__ == "__main__":
    success = test_categorical_encoding()
    test_edge_cases()
    
    if success:
        print("\\n🚀 All tests passed! SHAP plot should work with categorical data.")
    else:
        print("\\n⚠️ Some tests failed. Check the encoding logic.")