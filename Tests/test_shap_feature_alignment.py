#!/usr/bin/env python3
"""
Test SHAP plot feature alignment with the trained model
"""

import pandas as pd
import numpy as np
import json
import joblib
from faker import Faker

def test_feature_alignment():
    """Test that SHAP plot uses correct feature alignment"""
    print("🧪 Testing SHAP Feature Alignment")
    print("=" * 50)
    
    try:
        # Load model and metadata (same as API)
        print("📂 Loading model and metadata...")
        model = joblib.load('Modelos/XGBoost_model.pkl')
        
        with open('Modelos/XGBoost_model_metadata.json', 'r') as f:
            metadata = json.load(f)
        feature_columns = metadata['feature_columns']
        
        print(f"✅ Model loaded successfully")
        print(f"📊 Expected features: {len(feature_columns)}")
        print(f"🏷️ Feature columns: {feature_columns[:10]}..." if len(feature_columns) > 10 else f"🏷️ Feature columns: {feature_columns}")
        
        # Create sample customer data
        fake = Faker()
        customer_data = {
            'Name': fake.first_name(),
            'Surname': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'address': fake.address(),
            'age': 35,
            'housing': 'own',
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
            'payment_type': 'credit_card',
            'waiting_4_loan': 0,
            'cancelled_loan': 0,
            'received_loan': 1,
            'rejected_loan': 0,
            'zodiac_sign': 'leo',
            'left_for_two_month_plus': 0,
            'left_for_one_month': 0,
            'rewards_earned': 150,
            'reward_rate': 0.025,
            'is_referred': 1
        }
        
        print(f"\\n👤 Test customer: {customer_data['Name']} {customer_data['Surname']}")
        
        # Prepare data (same as SHAP function)
        print("\\n🔧 Preparing data for SHAP...")
        api_data = {k: v for k, v in customer_data.items() 
                   if k not in ['Name', 'Surname', 'email', 'phone', 'address']}
        
        print(f"📊 Customer data fields: {len(api_data)}")
        
        # Create DataFrame
        customer_df = pd.DataFrame([api_data])
        print(f"📋 Initial DataFrame shape: {customer_df.shape}")
        print(f"📋 Initial columns: {list(customer_df.columns)}")
        
        # Ensure all feature columns are present (same as API)
        missing_features = []
        for col in feature_columns:
            if col not in customer_df.columns:
                customer_df[col] = 0
                missing_features.append(col)
        
        if missing_features:
            print(f"➕ Added {len(missing_features)} missing features: {missing_features[:5]}..." if len(missing_features) > 5 else f"➕ Added missing features: {missing_features}")
        
        # Reorder columns to match training data
        customer_df = customer_df[feature_columns]
        print(f"📋 Final DataFrame shape: {customer_df.shape}")
        print(f"✅ Feature alignment: {customer_df.shape[1]} == {len(feature_columns)}")
        
        # Ensure all columns are numeric
        print("\\n🔢 Converting to numeric types...")
        for col in customer_df.columns:
            original_dtype = customer_df[col].dtype
            customer_df[col] = pd.to_numeric(customer_df[col], errors='coerce').fillna(0)
            if original_dtype != customer_df[col].dtype:
                print(f"   {col}: {original_dtype} → {customer_df[col].dtype}")
        
        # Test model prediction
        print("\\n🔮 Testing model prediction...")
        prediction = model.predict_proba(customer_df)[0][1]
        print(f"✅ Prediction successful: {prediction:.2%} churn probability")
        
        # Test SHAP explainer
        print("\\n📊 Testing SHAP explainer...")
        import shap
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(customer_df)
        
        print(f"✅ SHAP values generated successfully")
        print(f"📊 SHAP values shape: {np.array(shap_values).shape}")
        print(f"📊 Expected value: {explainer.expected_value}")
        
        # Show top contributing features
        feature_importance = list(zip(feature_columns, shap_values[0]))
        feature_importance.sort(key=lambda x: abs(x[1]), reverse=True)
        
        print("\\n🏆 Top 5 contributing features:")
        for i, (feature, importance) in enumerate(feature_importance[:5]):
            print(f"   {i+1}. {feature}: {importance:.4f}")
        
        print("\\n🎯 SHAP feature alignment test PASSED!")
        return True
        
    except FileNotFoundError as e:
        print(f"❌ Model files not found: {str(e)}")
        print("   Run 'python train_model.py' to generate model files")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_api_compatibility():
    """Test that SHAP function matches API preprocessing"""
    print("\\n🧪 Testing API Compatibility")
    print("=" * 40)
    
    try:
        # Simulate API preprocessing
        print("📤 Simulating API preprocessing...")
        
        # Sample data (same as API CustomerData model)
        api_customer_data = {
            "age": 35,
            "credit_score": 720.5,
            "withdrawal": 3,
            "deposits": 8,
            "purchases_partners": 12,
            "cc_recommended": 0,
            "web_user": 1,
            "ios_user": 0,
            "registered_phones": 1,
            "waiting_4_loan": 0,
            "cancelled_loan": 0,
            "received_loan": 1,
            "rejected_loan": 0,
            "left_for_two_month_plus": 0,
            "left_for_one_month": 0,
            "reward_rate": 0.025,
            "is_referred": 1
        }
        
        # Load feature columns
        with open('Modelos/XGBoost_model_metadata.json', 'r') as f:
            metadata = json.load(f)
        feature_columns = metadata['feature_columns']
        
        # Create DataFrame (same as API)
        df = pd.DataFrame([api_customer_data])
        
        # Ensure all feature columns are present (same as API)
        for col in feature_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Reorder columns to match training data (same as API)
        df = df[feature_columns]
        
        print(f"✅ API-style preprocessing successful")
        print(f"📊 Final shape: {df.shape}")
        print(f"📊 Features: {len(feature_columns)}")
        
        # Test with model
        model = joblib.load('Modelos/XGBoost_model.pkl')
        prediction = model.predict_proba(df)[0][1]
        print(f"✅ Model prediction: {prediction:.2%}")
        
        print("\\n🎯 API compatibility test PASSED!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 SHAP Feature Alignment Tests")
    print("=" * 60)
    
    test1_success = test_feature_alignment()
    test2_success = test_api_compatibility()
    
    print("\\n📋 Test Results:")
    print(f"   Feature Alignment: {'✅ PASSED' if test1_success else '❌ FAILED'}")
    print(f"   API Compatibility: {'✅ PASSED' if test2_success else '❌ FAILED'}")
    
    if test1_success and test2_success:
        print("\\n🎉 All tests passed! SHAP plot should work correctly.")
        print("\\n💡 Key fixes applied:")
        print("   • Using same model as API (Modelos/XGBoost_model.pkl)")
        print("   • Loading feature columns from metadata")
        print("   • Ensuring correct feature alignment")
        print("   • Matching API preprocessing exactly")
    else:
        print("\\n⚠️ Some tests failed. Check model files and feature alignment.")

if __name__ == "__main__":
    main()