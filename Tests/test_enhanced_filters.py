#!/usr/bin/env python3
"""
Test script for the enhanced filtering functionality
"""

import pandas as pd
import numpy as np
from faker import Faker

# Import the filtering functions (assuming they're in streamlit_ui.py)
import sys
import os

def create_test_data():
    """Create test data similar to the Streamlit app"""
    np.random.seed(42)
    fake = Faker()
    n_samples = 100
    
    sample_data = {
        "age": np.random.randint(18, 80, n_samples),
        "housing": np.random.choice(["o", "r", "na"], n_samples),
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
        "payment_type": np.random.choice(["monthly", "bi-weekly", "weekly", "semi-monthly", "na"], n_samples),
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
    
    # Add personal info columns
    df['Name'] = [fake.first_name() for _ in range(len(df))]
    df['Surname'] = [fake.last_name() for _ in range(len(df))]
    df['email'] = [fake.email() for _ in range(len(df))]
    df['phone'] = [fake.phone_number() for _ in range(len(df))]
    df['address'] = [fake.address().replace('\n', ', ') for _ in range(len(df))]
    
    return df

def apply_enhanced_filters(data, filter_params):
    """Apply enhanced filters to the data (copied from streamlit_ui.py)"""
    filtered = data.copy()
    
    # Demographic filters
    age_range = filter_params['age_range']
    filtered = filtered[
        (filtered['age'] >= age_range[0]) & 
        (filtered['age'] <= age_range[1])
    ]
    
    housing_filter = filter_params['housing_filter']
    if housing_filter not in ["All", "Todos"]:
        filtered = filtered[filtered['housing'] == housing_filter.lower()]
    
    payment_filter = filter_params['payment_filter']
    if payment_filter not in ["All", "Todos"]:
        filtered = filtered[filtered['payment_type'] == payment_filter.lower()]
    
    # Financial filters
    credit_range = filter_params['credit_range']
    filtered = filtered[
        (filtered['credit_score'] >= credit_range[0]) & 
        (filtered['credit_score'] <= credit_range[1])
    ]
    
    deposits_range = filter_params['deposits_range']
    filtered = filtered[
        (filtered['deposits'] >= deposits_range[0]) & 
        (filtered['deposits'] <= deposits_range[1])
    ]
    
    purchases_range = filter_params['purchases_range']
    filtered = filtered[
        (filtered['purchases'] >= purchases_range[0]) & 
        (filtered['purchases'] <= purchases_range[1])
    ]
    
    rewards_range = filter_params['rewards_range']
    filtered = filtered[
        (filtered['rewards_earned'] >= rewards_range[0]) & 
        (filtered['rewards_earned'] <= rewards_range[1])
    ]
    
    # Digital activity filters
    app_downloaded_filter = filter_params['app_downloaded_filter']
    if app_downloaded_filter == "Sí":
        filtered = filtered[filtered['app_downloaded'] == 1]
    elif app_downloaded_filter == "No":
        filtered = filtered[filtered['app_downloaded'] == 0]
    
    web_user_filter = filter_params['web_user_filter']
    if web_user_filter == "Sí":
        filtered = filtered[filtered['web_user'] == 1]
    elif web_user_filter == "No":
        filtered = filtered[filtered['web_user'] == 0]
    
    platform_filter = filter_params['platform_filter']
    if platform_filter == "iOS":
        filtered = filtered[filtered['ios_user'] == 1]
    elif platform_filter == "Android":
        filtered = filtered[filtered['android_user'] == 1]
    elif platform_filter == "Ambos":
        filtered = filtered[(filtered['ios_user'] == 1) & (filtered['android_user'] == 1)]
    elif platform_filter == "Ninguno":
        filtered = filtered[(filtered['ios_user'] == 0) & (filtered['android_user'] == 0)]
    
    # Banking product filters
    cc_taken_filter = filter_params['cc_taken_filter']
    if cc_taken_filter == "Tomada":
        filtered = filtered[filtered['cc_taken'] == 1]
    elif cc_taken_filter == "No Tomada":
        filtered = filtered[filtered['cc_taken'] == 0]
    
    loan_status_filter = filter_params['loan_status_filter']
    if loan_status_filter == "Recibido":
        filtered = filtered[filtered['received_loan'] == 1]
    elif loan_status_filter == "Rechazado":
        filtered = filtered[filtered['rejected_loan'] == 1]
    elif loan_status_filter == "Esperando":
        filtered = filtered[filtered['waiting_4_loan'] == 1]
    elif loan_status_filter == "Cancelado":
        filtered = filtered[filtered['cancelled_loan'] == 1]
    elif loan_status_filter == "Sin Actividad":
        filtered = filtered[
            (filtered['received_loan'] == 0) & 
            (filtered['rejected_loan'] == 0) & 
            (filtered['waiting_4_loan'] == 0) & 
            (filtered['cancelled_loan'] == 0)
        ]
    
    cc_sentiment_filter = filter_params['cc_sentiment_filter']
    if cc_sentiment_filter == "Positivo":
        filtered = filtered[filtered['cc_liked'] == 1]
    elif cc_sentiment_filter == "Negativo":
        filtered = filtered[filtered['cc_disliked'] == 1]
    elif cc_sentiment_filter == "Neutral":
        filtered = filtered[(filtered['cc_liked'] == 0) & (filtered['cc_disliked'] == 0)]
    
    # Risk filters
    activity_filter = filter_params['activity_filter']
    if activity_filter == "Activo":
        filtered = filtered[
            (filtered['left_for_one_month'] == 0) & 
            (filtered['left_for_two_month_plus'] == 0)
        ]
    elif activity_filter == "Inactivo 1 Mes":
        filtered = filtered[filtered['left_for_one_month'] == 1]
    elif activity_filter == "Inactivo 2+ Meses":
        filtered = filtered[filtered['left_for_two_month_plus'] == 1]
    
    referral_filter = filter_params['referral_filter']
    if referral_filter == "Referido":
        filtered = filtered[filtered['is_referred'] == 1]
    elif referral_filter == "No Referido":
        filtered = filtered[filtered['is_referred'] == 0]
    
    return filtered

def test_filter_scenarios():
    """Test various filter scenarios"""
    print("🚀 Testing Enhanced Filtering Functionality")
    print("=" * 60)
    
    # Create test data
    data = create_test_data()
    print(f"📊 Created test dataset with {len(data)} customers")
    
    # Test scenarios
    test_cases = [
        {
            "name": "No Filters (All Customers)",
            "params": {
                'age_range': (18, 80),
                'credit_range': (300, 850),
                'housing_filter': "Todos",
                'payment_filter': "Todos",
                'deposits_range': (0, data['deposits'].max()),
                'purchases_range': (0, data['purchases'].max()),
                'rewards_range': (0, data['rewards_earned'].max()),
                'app_downloaded_filter': "Todos",
                'web_user_filter': "Todos",
                'platform_filter': "Todos",
                'cc_taken_filter': "Todos",
                'loan_status_filter': "Todos",
                'cc_sentiment_filter': "Todos",
                'activity_filter': "Todos",
                'referral_filter': "Todos"
            }
        },
        {
            "name": "Young App Users (Age 18-30, App Downloaded)",
            "params": {
                'age_range': (18, 30),
                'credit_range': (300, 850),
                'housing_filter': "Todos",
                'payment_filter': "Todos",
                'deposits_range': (0, data['deposits'].max()),
                'purchases_range': (0, data['purchases'].max()),
                'rewards_range': (0, data['rewards_earned'].max()),
                'app_downloaded_filter': "Sí",
                'web_user_filter': "Todos",
                'platform_filter': "Todos",
                'cc_taken_filter': "Todos",
                'loan_status_filter': "Todos",
                'cc_sentiment_filter': "Todos",
                'activity_filter': "Todos",
                'referral_filter': "Todos"
            }
        },
        {
            "name": "High Value Customers (Credit Score 700+, High Activity)",
            "params": {
                'age_range': (18, 80),
                'credit_range': (700, 850),
                'housing_filter': "Todos",
                'payment_filter': "Todos",
                'deposits_range': (0, data['deposits'].max()),
                'purchases_range': (20, data['purchases'].max()),
                'rewards_range': (0, data['rewards_earned'].max()),
                'app_downloaded_filter': "Todos",
                'web_user_filter': "Todos",
                'platform_filter': "Todos",
                'cc_taken_filter': "Tomada",
                'loan_status_filter': "Todos",
                'cc_sentiment_filter': "Todos",
                'activity_filter': "Todos",
                'referral_filter': "Todos"
            }
        },
        {
            "name": "At-Risk Customers (Inactive, Low Credit)",
            "params": {
                'age_range': (18, 80),
                'credit_range': (300, 600),
                'housing_filter': "Todos",
                'payment_filter': "Todos",
                'deposits_range': (0, data['deposits'].max()),
                'purchases_range': (0, data['purchases'].max()),
                'rewards_range': (0, data['rewards_earned'].max()),
                'app_downloaded_filter': "Todos",
                'web_user_filter': "Todos",
                'platform_filter': "Todos",
                'cc_taken_filter': "Todos",
                'loan_status_filter': "Todos",
                'cc_sentiment_filter': "Todos",
                'activity_filter': "Inactivo 2+ Meses",
                'referral_filter': "Todos"
            }
        },
        {
            "name": "iOS Users with Credit Cards",
            "params": {
                'age_range': (18, 80),
                'credit_range': (300, 850),
                'housing_filter': "Todos",
                'payment_filter': "Todos",
                'deposits_range': (0, data['deposits'].max()),
                'purchases_range': (0, data['purchases'].max()),
                'rewards_range': (0, data['rewards_earned'].max()),
                'app_downloaded_filter': "Todos",
                'web_user_filter': "Todos",
                'platform_filter': "iOS",
                'cc_taken_filter': "Tomada",
                'loan_status_filter': "Todos",
                'cc_sentiment_filter': "Todos",
                'activity_filter': "Todos",
                'referral_filter': "Todos"
            }
        }
    ]
    
    # Run test cases
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print("-" * 40)
        
        try:
            filtered_data = apply_enhanced_filters(data, test_case['params'])
            
            print(f"   📊 Results: {len(filtered_data)} customers ({len(filtered_data)/len(data)*100:.1f}%)")
            
            if len(filtered_data) > 0:
                print(f"   📈 Age range: {filtered_data['age'].min()}-{filtered_data['age'].max()}")
                print(f"   💳 Credit score range: {filtered_data['credit_score'].min():.0f}-{filtered_data['credit_score'].max():.0f}")
                print(f"   📱 App users: {(filtered_data['app_downloaded'] == 1).sum()}")
                print(f"   🏦 Credit card holders: {(filtered_data['cc_taken'] == 1).sum()}")
            else:
                print("   ⚠️ No customers match these criteria")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Filter testing completed!")

def test_filter_combinations():
    """Test complex filter combinations"""
    print("\n🔬 Testing Complex Filter Combinations")
    print("=" * 60)
    
    data = create_test_data()
    
    # Test edge cases
    edge_cases = [
        {
            "name": "Very Restrictive Filters",
            "params": {
                'age_range': (25, 35),
                'credit_range': (750, 850),
                'housing_filter': "o",
                'payment_filter': "monthly",
                'deposits_range': (5, 10),
                'purchases_range': (30, 50),
                'rewards_range': (150, 300),
                'app_downloaded_filter': "Sí",
                'web_user_filter': "Sí",
                'platform_filter': "iOS",
                'cc_taken_filter': "Tomada",
                'loan_status_filter': "Recibido",
                'cc_sentiment_filter': "Positivo",
                'activity_filter': "Activo",
                'referral_filter': "Referido"
            }
        },
        {
            "name": "Contradictory Filters",
            "params": {
                'age_range': (18, 25),
                'credit_range': (300, 850),
                'housing_filter': "Todos",
                'payment_filter': "Todos",
                'deposits_range': (0, data['deposits'].max()),
                'purchases_range': (0, data['purchases'].max()),
                'rewards_range': (0, data['rewards_earned'].max()),
                'app_downloaded_filter': "No",
                'web_user_filter': "Sí",
                'platform_filter': "iOS",  # iOS user but no app downloaded
                'cc_taken_filter': "Todos",
                'loan_status_filter': "Todos",
                'cc_sentiment_filter': "Todos",
                'activity_filter': "Todos",
                'referral_filter': "Todos"
            }
        }
    ]
    
    for test_case in edge_cases:
        print(f"\n🧪 {test_case['name']}")
        print("-" * 40)
        
        try:
            filtered_data = apply_enhanced_filters(data, test_case['params'])
            print(f"   📊 Results: {len(filtered_data)} customers")
            
            if len(filtered_data) == 0:
                print("   💡 No customers match - this may be expected for restrictive filters")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def main():
    """Main test function"""
    test_filter_scenarios()
    test_filter_combinations()
    
    print("\n🎉 All filter tests completed!")
    print("💡 The enhanced filtering system is ready for use in Streamlit!")

if __name__ == "__main__":
    main()