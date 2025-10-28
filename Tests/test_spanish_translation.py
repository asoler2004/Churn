#!/usr/bin/env python3
"""
Test script to verify Spanish translations in the UI
"""

import requests
import json
import time

def test_llm_api_spanish():
    """Test that LLM API responds in Spanish"""
    print("🧪 Testing LLM API Spanish responses...")
    
    # Sample customer data for testing
    test_data = {
        "age": 35,
        "housing": "rent",
        "credit_score": 650.0,
        "deposits": 5,
        "withdrawal": 3,
        "purchases_partners": 10,
        "purchases": 25,
        "cc_taken": 1,
        "cc_recommended": 0,
        "cc_disliked": 0,
        "cc_liked": 1,
        "cc_application_begin": 1,
        "app_downloaded": 1,
        "web_user": 1,
        "app_web_user": 1,
        "ios_user": 1,
        "android_user": 0,
        "registered_phones": 1,
        "payment_type": "credit_card",
        "waiting_4_loan": 0,
        "cancelled_loan": 0,
        "received_loan": 0,
        "rejected_loan": 0,
        "left_for_two_month_plus": 0,
        "left_for_one_month": 0,
        "rewards_earned": 100,
        "reward_rate": 0.02,
        "is_referred": 1,
        "churn_probability": 0.3,
        "churn_prediction": 0,
        "risk_level": "Medium"
    }
    
    try:
        # Test LLM API
        response = requests.post(
            "http://localhost:8001/generate-insights",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            insights = result.get('recommendations', '')
            
            # Check for Spanish keywords
            spanish_keywords = [
                'INSIGHTS CLAVE',
                'RECOMENDACIONES',
                'ACCIONES INMEDIATAS',
                'ESTRATEGIA DE RETENCIÓN',
                'PRÓXIMOS PASOS'
            ]
            
            spanish_found = sum(1 for keyword in spanish_keywords if keyword in insights)
            
            print(f"✅ LLM API Response received")
            print(f"📊 Spanish keywords found: {spanish_found}/{len(spanish_keywords)}")
            
            if spanish_found >= 3:
                print("🎉 LLM API is responding in Spanish!")
            else:
                print("⚠️ LLM API may not be fully translated to Spanish")
            
            # Show sample of response
            print("\n📝 Sample response (first 200 characters):")
            print(insights[:200] + "..." if len(insights) > 200 else insights)
            
        else:
            print(f"❌ LLM API Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ LLM API is not running. Please start llm_api.py first.")
    except Exception as e:
        print(f"❌ Error testing LLM API: {str(e)}")

def test_prediction_api():
    """Test that prediction API is working"""
    print("\n🧪 Testing Prediction API...")
    
    # Sample customer data for prediction
    test_data = {
        "age": 35,
        "credit_score": 650.0,
        "withdrawal": 3,
        "deposits": 5,
        "purchases_partners": 10,
        "cc_recommended": 0,
        "web_user": 1,
        "ios_user": 1,
        "registered_phones": 1,
        "waiting_4_loan": 0,
        "cancelled_loan": 0,
        "received_loan": 0,
        "rejected_loan": 0,
        "left_for_two_month_plus": 0,
        "left_for_one_month": 0,
        "reward_rate": 0.02,
        "is_referred": 1
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            prob_xgb = result.get('churn_probability_XGB', 0)
            risk_xgb = result.get('risk_level_XGB', 'Unknown')
            
            print(f"✅ Prediction API Response received")
            print(f"📊 XGBoost Churn Probability: {prob_xgb:.2%}")
            print(f"📊 XGBoost Risk Level: {risk_xgb}")
            
        else:
            print(f"❌ Prediction API Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Prediction API is not running. Please start api.py first.")
    except Exception as e:
        print(f"❌ Error testing Prediction API: {str(e)}")

def check_ui_files():
    """Check that UI files contain Spanish text"""
    print("\n🧪 Checking UI files for Spanish translations...")
    
    files_to_check = [
        ('streamlit_ui.py', [
            'Panel de Predicción de Abandono Fintech',
            'Datos de Clientes',
            'Agregar Cliente',
            'Predicciones',
            'Insights'
        ]),
        ('churn_ui.py', [
            'Panel de Predicción de Abandono Fintech',
            'Gestión de Datos',
            'Cargar Datos de Muestra',
            'Predicción de Abandono'
        ]),
        ('llm_api.py', [
            'INSIGHTS CLAVE',
            'RECOMENDACIONES',
            'ACCIONES INMEDIATAS',
            'ESTRATEGIA DE RETENCIÓN'
        ])
    ]
    
    for filename, spanish_terms in files_to_check:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            found_terms = sum(1 for term in spanish_terms if term in content)
            
            print(f"📄 {filename}: {found_terms}/{len(spanish_terms)} Spanish terms found")
            
            if found_terms >= len(spanish_terms) * 0.8:  # 80% threshold
                print(f"  ✅ {filename} appears to be translated")
            else:
                print(f"  ⚠️ {filename} may need more translation")
                
        except FileNotFoundError:
            print(f"  ❌ {filename} not found")
        except Exception as e:
            print(f"  ❌ Error checking {filename}: {str(e)}")

def main():
    """Run all translation tests"""
    print("🌍 Testing Spanish Translation Implementation")
    print("=" * 50)
    
    # Check UI files first
    check_ui_files()
    
    # Test APIs
    test_prediction_api()
    test_llm_api_spanish()
    
    print("\n" + "=" * 50)
    print("🎯 Translation Test Complete!")
    print("\n💡 To test the full UI:")
    print("1. Start the APIs: python api.py & python llm_api.py")
    print("2. Start Streamlit: streamlit run streamlit_ui.py")
    print("3. Check that all text appears in Spanish")

if __name__ == "__main__":
    main()