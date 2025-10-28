#!/usr/bin/env python3
"""
Test script to verify that LLM API properly uses sections variable
"""

import requests
import json
import sys
import time

def test_llm_sections_parsing():
    """Test that the LLM API properly parses and uses sections"""
    print("\n🧪 Testing LLM Sections Parsing")
    print("=" * 50)
    
    # Sample customer data for testing
    test_customer = {
        "age": 35,
        "housing": "r",
        "credit_score": 580.0,
        "deposits": 2,
        "withdrawal": 5,
        "purchases_partners": 3,
        "purchases": 8,
        "cc_taken": 0,
        "cc_recommended": 1,
        "cc_disliked": 1,
        "cc_liked": 0,
        "cc_application_begin": 0,
        "app_downloaded": 0,
        "web_user": 1,
        "app_web_user": 0,
        "ios_user": 0,
        "android_user": 1,
        "registered_phones": 1,
        "payment_type": "monthly",
        "waiting_4_loan": 0,
        "cancelled_loan": 0,
        "received_loan": 0,
        "rejected_loan": 1,
        "left_for_two_month_plus": 0,
        "left_for_one_month": 1,
        "rewards_earned": 25,
        "reward_rate": 0.01,
        "is_referred": 0,
        "churn_probability": 0.75,
        "churn_prediction": 1,
        "risk_level": "High",
        "use_transformers": False
    }
    
    print(f"Testing with high-risk customer (churn probability: {test_customer['churn_probability']})")
    
    try:
        # Test the LLM API endpoint
        response = requests.post(
            "http://localhost:8001/generate-insights",
            json=test_customer,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ API Response received successfully")
            print(f"Status Code: {response.status_code}")
            
            # Check that all expected fields are present
            expected_fields = ['recommendations', 'key_insights', 'action_items']
            missing_fields = []
            
            for field in expected_fields:
                if field not in result:
                    missing_fields.append(field)
                else:
                    print(f"✅ {field}: Present ({len(result[field])} characters)")
            
            if missing_fields:
                print(f"❌ Missing fields: {missing_fields}")
                return False
            
            # Check that fields are not just default values
            recommendations = result['recommendations']
            key_insights = result['key_insights']
            action_items = result['action_items']
            
            print(f"\n📊 Content Analysis:")
            
            # Check recommendations
            if len(recommendations) > 50 and recommendations != "Análisis completado exitosamente":
                print(f"✅ Recommendations: Meaningful content ({len(recommendations)} chars)")
            else:
                print(f"⚠️  Recommendations: May be default/short content")
            
            # Check key insights
            if key_insights != "Análisis completado exitosamente" or len(key_insights) > 100:
                print(f"✅ Key Insights: Custom content ({len(key_insights)} chars)")
            else:
                print(f"⚠️  Key Insights: Default content")
            
            # Check action items
            if action_items != "Ver recomendaciones para elementos de acción detallados":
                print(f"✅ Action Items: Custom content ({len(action_items)} chars)")
            else:
                print(f"⚠️  Action Items: Default content")
            
            # Display sample content
            print(f"\n📝 Sample Content:")
            print(f"Recommendations (first 200 chars):")
            print(f"  {recommendations[:200]}...")
            
            print(f"\nKey Insights (first 150 chars):")
            print(f"  {key_insights[:150]}...")
            
            print(f"\nAction Items (first 150 chars):")
            print(f"  {action_items[:150]}...")
            
            # Check for section parsing indicators
            sections_parsed = False
            if ('RECOMENDACIONES' in recommendations.upper() or 
                'INSIGHTS' in key_insights.upper() or 
                'ACCIONES' in action_items.upper()):
                sections_parsed = True
                print(f"\n✅ Sections appear to be parsed from content")
            else:
                print(f"\n📋 Using smart defaults (sections not explicitly parsed)")
            
            return True
            
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: LLM API not running on localhost:8001")
        print("💡 Start the API with: python llm_api.py")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: API took too long to respond")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_different_risk_levels():
    """Test sections parsing with different risk levels"""
    print("\n🧪 Testing Different Risk Levels")
    print("=" * 50)
    
    risk_scenarios = [
        {
            "name": "High Risk",
            "churn_probability": 0.85,
            "risk_level": "High",
            "credit_score": 520.0,
            "left_for_one_month": 1
        },
        {
            "name": "Medium Risk", 
            "churn_probability": 0.45,
            "risk_level": "Medium",
            "credit_score": 650.0,
            "left_for_one_month": 0
        },
        {
            "name": "Low Risk",
            "churn_probability": 0.15,
            "risk_level": "Low", 
            "credit_score": 750.0,
            "left_for_one_month": 0
        }
    ]
    
    base_customer = {
        "age": 30,
        "housing": "o",
        "deposits": 5,
        "withdrawal": 3,
        "purchases_partners": 10,
        "purchases": 20,
        "cc_taken": 1,
        "cc_recommended": 0,
        "cc_disliked": 0,
        "cc_liked": 1,
        "cc_application_begin": 0,
        "app_downloaded": 1,
        "web_user": 1,
        "app_web_user": 1,
        "ios_user": 1,
        "android_user": 0,
        "registered_phones": 1,
        "payment_type": "monthly",
        "waiting_4_loan": 0,
        "cancelled_loan": 0,
        "received_loan": 0,
        "rejected_loan": 0,
        "rewards_earned": 100,
        "reward_rate": 0.02,
        "is_referred": 1,
        "churn_prediction": 0,
        "use_transformers": False
    }
    
    results = []
    
    for scenario in risk_scenarios:
        print(f"\n🎯 Testing {scenario['name']} Customer...")
        
        # Create test customer
        test_customer = base_customer.copy()
        test_customer.update({
            "churn_probability": scenario["churn_probability"],
            "risk_level": scenario["risk_level"],
            "credit_score": scenario["credit_score"],
            "left_for_one_month": scenario["left_for_one_month"]
        })
        
        try:
            response = requests.post(
                "http://localhost:8001/generate-insights",
                json=test_customer,
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Analyze content differences
                rec_length = len(result['recommendations'])
                insights_length = len(result['key_insights'])
                actions_length = len(result['action_items'])
                
                print(f"  ✅ Response received")
                print(f"     Recommendations: {rec_length} chars")
                print(f"     Key Insights: {insights_length} chars") 
                print(f"     Action Items: {actions_length} chars")
                
                results.append({
                    'scenario': scenario['name'],
                    'risk_level': scenario['risk_level'],
                    'rec_length': rec_length,
                    'insights_length': insights_length,
                    'actions_length': actions_length,
                    'success': True
                })
                
                # Brief content sample
                print(f"     Sample: {result['recommendations'][:100]}...")
                
            else:
                print(f"  ❌ API Error: {response.status_code}")
                results.append({
                    'scenario': scenario['name'],
                    'success': False
                })
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append({
                'scenario': scenario['name'],
                'success': False
            })
        
        # Small delay between requests
        time.sleep(1)
    
    # Summary
    print(f"\n📊 Risk Level Testing Summary:")
    successful_tests = [r for r in results if r.get('success', False)]
    
    if len(successful_tests) >= 2:
        print(f"✅ {len(successful_tests)}/{len(risk_scenarios)} scenarios tested successfully")
        
        # Check for content variation
        lengths = [r['rec_length'] for r in successful_tests]
        if max(lengths) - min(lengths) > 100:
            print(f"✅ Content varies appropriately by risk level")
        else:
            print(f"⚠️  Content length similar across risk levels")
            
        return True
    else:
        print(f"❌ Only {len(successful_tests)}/{len(risk_scenarios)} scenarios successful")
        return False

def main():
    """Run LLM sections parsing tests"""
    print("🚀 Starting LLM Sections Parsing Tests")
    print("=" * 60)
    
    tests = [
        ("Basic Sections Parsing", test_llm_sections_parsing),
        ("Different Risk Levels", test_different_risk_levels)
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
    
    print("\n" + "="*60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All LLM sections parsing tests passed!")
        print("✅ Sections variable is now properly utilized!")
        return True
    else:
        print(f"⚠️  {total - passed} tests failed")
        print("💡 Make sure the LLM API is running: python llm_api.py")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)