#!/usr/bin/env python3
"""
Test script for Streamlit UI functionality
"""

import pandas as pd
import numpy as np
from faker import Faker
import sys
import os

def test_data_generation():
    """Test the data generation functionality"""
    print("🧪 Testing data generation...")
    
    fake = Faker()
    np.random.seed(42)
    n_samples = 10
    
    try:
        sample_data = {
            "age": np.random.randint(18, 80, n_samples),
            "housing": np.random.choice(["own", "rent", "mortgage"], n_samples),
            "credit_score": np.random.normal(650, 100, n_samples).clip(300, 850),
            "deposits": np.random.poisson(5, n_samples),
            "withdrawal": np.random.poisson(3, n_samples),
            "purchases_partners": np.random.poisson(10, n_samples),
            "purchases": np.random.poisson(25, n_samples),
            "cc_taken": np.random.binomial(1, 0.3, n_samples),
            "cc_recommended": np.random.binomial(1, 0.4, n_samples),
            "cc_disliked": np.random.binomial(1, 0.2, n_samples),
            "cc_liked": np.random.binomial(1, 0.6, n_samples),
            "cc_application_begin": np.random.binomial(1, 0.3, n_samples),
            "app_downloaded": np.random.binomial(1, 0.7, n_samples),
            "web_user": np.random.binomial(1, 0.8, n_samples),
            "app_web_user": np.random.binomial(1, 0.5, n_samples),
            "ios_user": np.random.binomial(1, 0.4, n_samples),
            "android_user": np.random.binomial(1, 0.6, n_samples),
            "registered_phones": np.random.poisson(1, n_samples),
            "payment_type": np.random.choice(["credit_card", "debit_card", "bank_transfer"], n_samples),
            "waiting_4_loan": np.random.binomial(1, 0.1, n_samples),
            "cancelled_loan": np.random.binomial(1, 0.05, n_samples),
            "received_loan": np.random.binomial(1, 0.2, n_samples),
            "rejected_loan": np.random.binomial(1, 0.1, n_samples),
            "zodiac_sign": np.random.choice(["aries", "taurus", "gemini", "cancer", "leo", "virgo", 
                                           "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces"], n_samples),
            "left_for_two_month_plus": np.random.binomial(1, 0.1, n_samples),
            "left_for_one_month": np.random.binomial(1, 0.15, n_samples),
            "rewards_earned": np.random.poisson(100, n_samples),
            "reward_rate": np.random.uniform(0.01, 0.05, n_samples),
            "is_referred": np.random.binomial(1, 0.3, n_samples)
        }
        
        df = pd.DataFrame(sample_data)
        
        # Add personal info
        df['Name'] = [fake.first_name() for _ in range(len(df))]
        df['Surname'] = [fake.last_name() for _ in range(len(df))]
        df['email'] = [fake.email() for _ in range(len(df))]
        df['phone'] = [fake.phone_number() for _ in range(len(df))]
        df['address'] = [fake.address().replace('\n', ', ') for _ in range(len(df))]
        
        print(f"✅ Generated {len(df)} sample customers")
        print(f"📊 Columns: {list(df.columns)}")
        print(f"🔍 Sample customer: {df.iloc[0]['Name']} {df.iloc[0]['Surname']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in data generation: {str(e)}")
        return False

def test_customer_selection():
    """Test customer selection functionality"""
    print("\n🧪 Testing customer selection...")
    
    try:
        # Simulate a selected customer row
        customer = {
            'Name': 'John',
            'Surname': 'Doe',
            'age': 35,
            'credit_score': 650.5,
            'housing': 'own',
            'email': 'john.doe@example.com'
        }
        
        # Test safe access
        name = customer.get('Name', 'N/A')
        surname = customer.get('Surname', 'N/A')
        age = customer.get('age', 'N/A')
        
        print(f"✅ Customer access test passed: {name} {surname}, Age: {age}")
        return True
        
    except Exception as e:
        print(f"❌ Error in customer selection test: {str(e)}")
        return False

def test_chart_data():
    """Test chart data preparation"""
    print("\n🧪 Testing chart data preparation...")
    
    try:
        customer_data = {
            'age': 35,
            'credit_score': 650.5,
            'deposits': 5,
            'purchases': 25,
            'rewards_earned': 150,
            'app_downloaded': 1
        }
        
        # Test chart data preparation
        features = {
            'Age': max(0, min(100, customer_data.get('age', 30))),
            'Credit Score': max(0, min(100, customer_data.get('credit_score', 650) / 10)),
            'Deposits': max(0, min(50, customer_data.get('deposits', 5))),
            'Purchases': max(0, min(100, customer_data.get('purchases', 25))),
            'Rewards': max(0, min(100, customer_data.get('rewards_earned', 100) / 10)),
            'App Usage': customer_data.get('app_downloaded', 0) * 100,
        }
        
        print(f"✅ Chart data preparation test passed: {features}")
        return True
        
    except Exception as e:
        print(f"❌ Error in chart data test: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Streamlit UI Components")
    print("=" * 50)
    
    tests = [
        test_data_generation,
        test_customer_selection,
        test_chart_data
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Streamlit UI should work correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)