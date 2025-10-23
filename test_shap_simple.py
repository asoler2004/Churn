#!/usr/bin/env python3
"""
Simple test for SHAP plot with correct feature alignment
"""

import pandas as pd
import json
import joblib

def test_shap_simple():
    """Simple test of SHAP feature alignment"""
    print("🧪 Simple SHAP Test")
    print("=" * 30)
    
    try:
        # Load model and metadata
        print("📂 Loading model...")
        model = joblib.load('XGBoost_model.pkl')
        
        with open('XGBoost_model_metadata.json', 'r') as f:
            metadata = json.load(f)
        feature_columns = metadata['feature_columns']
        
        print(f"✅ Model loaded")
        print(f"📊 Expected features: {len(feature_columns)}")
        print(f"🏷️ Features: {feature_columns}")
        
        # Create sample customer data
        customer_data = {
            'Name': 'John Doe',
            'age': 35,
            'credit_score': 720.5,
            'deposits': 8,
            'withdrawal': 3,
            'purchases_partners': 12,
            'cc_recommended': 0,
            'web_user': 1,
            'ios_user': 0,
            'registered_phones': 1,
            'waiting_4_loan': 0,
            'cancelled_loan': 0,
            'received_loan': 1,
            'rejected_loan': 0,
            'left_for_two_month_plus': 0,
            'left_for_one_month': 0,
            'reward_rate': 0.025,
            'is_referred': 1,
            # Extra fields that should be ignored
            'housing': 'own',
            'payment_type': 'credit_card',
            'zodiac_sign': 'leo'
        }
        
        print(f"\\n👤 Customer: {customer_data['Name']}")
        
        # Prepare data - only include features the model was trained on
        api_data = {}
        for col in feature_columns:
            if col in customer_data:
                api_data[col] = customer_data[col]
            else:
                api_data[col] = 0
        
        print(f"📊 API data fields: {len(api_data)}")
        
        # Create DataFrame
        customer_df = pd.DataFrame([api_data])
        customer_df = customer_df[feature_columns]
        
        print(f"📋 DataFrame shape: {customer_df.shape}")
        print(f"✅ Feature count matches: {customer_df.shape[1] == len(feature_columns)}")
        
        # Convert to numeric
        for col in customer_df.columns:
            customer_df[col] = pd.to_numeric(customer_df[col], errors='coerce').fillna(0)
        
        # Test model prediction
        prediction = model.predict_proba(customer_df)[0][1]
        print(f"🔮 Prediction: {prediction:.2%}")
        
        # Test SHAP
        import shap
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(customer_df)
        
        print(f"📊 SHAP values shape: {len(shap_values)}")
        print(f"✅ SHAP generation successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_shap_simple()
    if success:
        print("\\n🎉 SHAP test passed! The fix should work.")
    else:
        print("\\n⚠️ SHAP test failed. Check the implementation.")