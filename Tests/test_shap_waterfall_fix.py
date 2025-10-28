#!/usr/bin/env python3
"""
Test SHAP waterfall plot with the new API format
"""

import pandas as pd
import numpy as np
import json
import joblib
import matplotlib.pyplot as plt
import shap

def test_shap_waterfall():
    """Test SHAP waterfall plot generation"""
    print("🧪 Testing SHAP Waterfall Plot")
    print("=" * 40)
    
    try:
        # Load model and metadata
        print("📂 Loading model and metadata...")
        model = joblib.load('Modelos/XGBoost_model.pkl')
        
        with open('Modelos/XGBoost_model_metadata.json', 'r') as f:
            metadata = json.load(f)
        feature_columns = metadata['feature_columns']
        
        print(f"✅ Model loaded successfully")
        print(f"📊 Features: {len(feature_columns)}")
        
        # Create sample customer data
        customer_data = {
            'Name': 'Test Customer',
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
            'is_referred': 1
        }
        
        print(f"\\n👤 Test customer: {customer_data['Name']}")
        
        # Prepare data - only include features the model was trained on
        api_data = {}
        for col in feature_columns:
            if col in customer_data:
                api_data[col] = customer_data[col]
            else:
                api_data[col] = 0
        
        # Create DataFrame with only the required features
        customer_df = pd.DataFrame([api_data])
        customer_df = customer_df[feature_columns]
        
        # Ensure all columns are numeric
        for col in customer_df.columns:
            customer_df[col] = pd.to_numeric(customer_df[col], errors='coerce').fillna(0)
        
        print(f"📋 DataFrame shape: {customer_df.shape}")
        
        # Create SHAP explainer
        print("\\n📊 Creating SHAP explainer...")
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(customer_df)
        
        print(f"✅ SHAP values generated")
        print(f"📊 SHAP values shape: {np.array(shap_values).shape}")
        
        # Test old API (should fail)
        print("\\n🧪 Testing old waterfall API...")
        try:
            fig_old, ax = plt.subplots(figsize=(8, 6))
            shap.waterfall_plot(explainer.expected_value, shap_values[0], customer_df.iloc[0], show=False)
            plt.close(fig_old)
            print("⚠️ Old API worked (unexpected)")
        except Exception as e:
            print(f"❌ Old API failed as expected: {str(e)[:100]}...")
        
        # Test new API (should work)
        print("\\n🧪 Testing new waterfall API...")
        try:
            fig_new, ax = plt.subplots(figsize=(10, 8))
            
            # Create SHAP Explanation object
            explanation = shap.Explanation(
                values=shap_values[0],
                base_values=explainer.expected_value,
                data=customer_df.iloc[0],
                feature_names=customer_df.columns.tolist()
            )
            
            # Generate waterfall plot
            shap.waterfall_plot(explanation, show=False)
            plt.title(f"SHAP Explanation for {customer_data['Name']}")
            plt.tight_layout()
            
            print("✅ New API worked successfully!")
            
            # Save the plot for verification
            plt.savefig('test_shap_waterfall.png', dpi=150, bbox_inches='tight')
            print("💾 Plot saved as 'test_shap_waterfall.png'")
            
            plt.close(fig_new)
            
        except Exception as e:
            print(f"❌ New API failed: {str(e)}")
            return False
        
        # Test alternative approach if needed
        print("\\n🧪 Testing alternative approach...")
        try:
            fig_alt, ax = plt.subplots(figsize=(10, 8))
            
            # Use shap.plots.waterfall (newer interface)
            shap.plots.waterfall(explanation, show=False)
            plt.title(f"SHAP Explanation (Alternative) for {customer_data['Name']}")
            plt.tight_layout()
            
            print("✅ Alternative API also works!")
            plt.close(fig_alt)
            
        except Exception as e:
            print(f"⚠️ Alternative API failed: {str(e)}")
        
        print("\\n🎯 SHAP waterfall test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

def test_shap_versions():
    """Check SHAP version and available functions"""
    print("\\n🔍 Checking SHAP Version and API")
    print("=" * 40)
    
    try:
        import shap
        print(f"📦 SHAP version: {shap.__version__}")
        
        # Check available waterfall functions
        waterfall_functions = []
        if hasattr(shap, 'waterfall_plot'):
            waterfall_functions.append('shap.waterfall_plot')
        if hasattr(shap, 'plots') and hasattr(shap.plots, 'waterfall'):
            waterfall_functions.append('shap.plots.waterfall')
        
        print(f"🔧 Available waterfall functions: {waterfall_functions}")
        
        # Check Explanation class
        if hasattr(shap, 'Explanation'):
            print("✅ shap.Explanation class available")
        else:
            print("❌ shap.Explanation class not available")
        
    except Exception as e:
        print(f"❌ Error checking SHAP: {str(e)}")

if __name__ == "__main__":
    print("🚀 SHAP Waterfall Plot Fix Test")
    print("=" * 50)
    
    test_shap_versions()
    success = test_shap_waterfall()
    
    if success:
        print("\\n🎉 SHAP waterfall fix successful!")
        print("\\n💡 Key changes:")
        print("   • Using shap.Explanation object")
        print("   • Modern waterfall_plot API")
        print("   • Proper parameter handling")
    else:
        print("\\n⚠️ SHAP waterfall fix needs more work")
        print("\\n🔧 Try:")
        print("   • Update SHAP library: pip install --upgrade shap")
        print("   • Check SHAP documentation for API changes")