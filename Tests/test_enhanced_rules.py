#!/usr/bin/env python3
"""
Test script for enhanced rule-based insights
Tests the 8 new rules added to the rule-based insights system
"""

import requests
import json

def test_enhanced_rules():
    """Test all 8 new enhanced rules"""
    
    print("🧪 Testing Enhanced Rule-Based Insights")
    print("=" * 60)
    
    # Test cases for each rule
    test_cases = [
        {
            "name": "Rule 1: Young + Low Credit + High Risk",
            "description": "Age < 30, credit_score < 600, high churn risk",
            "data": {
                "age": 25,
                "housing": "r",
                "credit_score": 450,
                "deposits": 2,
                "withdrawal": 5,
                "purchases_partners": 1,
                "purchases": 8,
                "cc_taken": 0,
                "cc_recommended": 1,
                "cc_disliked": 0,
                "cc_liked": 0,
                "cc_application_begin": 0,
                "app_downloaded": 0,
                "web_user": 1,
                "app_web_user": 0,
                "ios_user": 0,
                "android_user": 0,
                "registered_phones": 1,
                "payment_type": "monthly",
                "waiting_4_loan": 0,
                "cancelled_loan": 0,
                "received_loan": 0,
                "rejected_loan": 0,
                "left_for_two_month_plus": 0,
                "left_for_one_month": 0,
                "rewards_earned": 25,
                "reward_rate": 0.02,
                "is_referred": 0,
                "churn_probability": 0.75,
                "churn_prediction": 1,
                "risk_level": "High"
            },
            "expected_keywords": ["educación financiera", "score crediticio", "jóvenes"]
        },
        {
            "name": "Rule 2: Senior + Medium Risk",
            "description": "Age > 60, medium churn risk - digital engagement",
            "data": {
                "age": 65,
                "housing": "o",
                "credit_score": 650,
                "deposits": 3,
                "withdrawal": 2,
                "purchases_partners": 2,
                "purchases": 15,
                "cc_taken": 1,
                "cc_recommended": 0,
                "cc_disliked": 0,
                "cc_liked": 1,
                "cc_application_begin": 0,
                "app_downloaded": 0,
                "web_user": 0,
                "app_web_user": 0,
                "ios_user": 0,
                "android_user": 0,
                "registered_phones": 1,
                "payment_type": "monthly",
                "waiting_4_loan": 0,
                "cancelled_loan": 0,
                "received_loan": 1,
                "rejected_loan": 0,
                "left_for_two_month_plus": 0,
                "left_for_one_month": 0,
                "rewards_earned": 150,
                "reward_rate": 0.03,
                "is_referred": 0,
                "churn_probability": 0.55,
                "churn_prediction": 1,
                "risk_level": "Medium"
            },
            "expected_keywords": ["digital", "seniors", "entrenamiento"]
        },
        {
            "name": "Rule 3: Very Low Credit + High Risk",
            "description": "Credit score < 400, high churn risk",
            "data": {
                "age": 35,
                "housing": "r",
                "credit_score": 350,
                "deposits": 1,
                "withdrawal": 8,
                "purchases_partners": 0,
                "purchases": 5,
                "cc_taken": 0,
                "cc_recommended": 1,
                "cc_disliked": 1,
                "cc_liked": 0,
                "cc_application_begin": 0,
                "app_downloaded": 1,
                "web_user": 1,
                "app_web_user": 1,
                "ios_user": 1,
                "android_user": 0,
                "registered_phones": 1,
                "payment_type": "weekly",
                "waiting_4_loan": 0,
                "cancelled_loan": 1,
                "received_loan": 0,
                "rejected_loan": 1,
                "left_for_two_month_plus": 0,
                "left_for_one_month": 1,
                "rewards_earned": 10,
                "reward_rate": 0.01,
                "is_referred": 0,
                "churn_probability": 0.85,
                "churn_prediction": 1,
                "risk_level": "High"
            },
            "expected_keywords": ["soporte financiero", "emergencia", "reconstrucción"]
        },
        {
            "name": "Rule 4: Low Partner Purchases + Medium Risk",
            "description": "Low purchases_partners, medium churn risk",
            "data": {
                "age": 30,
                "housing": "o",
                "credit_score": 600,
                "deposits": 4,
                "withdrawal": 3,
                "purchases_partners": 1,
                "purchases": 20,
                "cc_taken": 1,
                "cc_recommended": 0,
                "cc_disliked": 0,
                "cc_liked": 1,
                "cc_application_begin": 0,
                "app_downloaded": 1,
                "web_user": 1,
                "app_web_user": 1,
                "ios_user": 0,
                "android_user": 1,
                "registered_phones": 1,
                "payment_type": "monthly",
                "waiting_4_loan": 0,
                "cancelled_loan": 0,
                "received_loan": 0,
                "rejected_loan": 0,
                "left_for_two_month_plus": 0,
                "left_for_one_month": 0,
                "rewards_earned": 75,
                "reward_rate": 0.025,
                "is_referred": 0,
                "churn_probability": 0.6,
                "churn_prediction": 1,
                "risk_level": "Medium"
            },
            "expected_keywords": ["socios", "incentivos", "cashback"]
        },
        {
            "name": "Rule 5: Referred Customer + High Risk",
            "description": "is_referred = 1, high churn risk",
            "data": {
                "age": 28,
                "housing": "r",
                "credit_score": 580,
                "deposits": 2,
                "withdrawal": 4,
                "purchases_partners": 3,
                "purchases": 12,
                "cc_taken": 0,
                "cc_recommended": 1,
                "cc_disliked": 0,
                "cc_liked": 0,
                "cc_application_begin": 1,
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
                "left_for_two_month_plus": 0,
                "left_for_one_month": 0,
                "rewards_earned": 45,
                "reward_rate": 0.02,
                "is_referred": 1,
                "churn_probability": 0.7,
                "churn_prediction": 1,
                "risk_level": "High"
            },
            "expected_keywords": ["referido", "recompensar", "referidos"]
        },
        {
            "name": "Rule 6: Low Risk + High Credit Score",
            "description": "Low churn risk, credit_score > 700 - referral opportunity",
            "data": {
                "age": 40,
                "housing": "o",
                "credit_score": 780,
                "deposits": 8,
                "withdrawal": 2,
                "purchases_partners": 15,
                "purchases": 45,
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
                "registered_phones": 2,
                "payment_type": "monthly",
                "waiting_4_loan": 0,
                "cancelled_loan": 0,
                "received_loan": 1,
                "rejected_loan": 0,
                "left_for_two_month_plus": 0,
                "left_for_one_month": 0,
                "rewards_earned": 500,
                "reward_rate": 0.04,
                "is_referred": 0,
                "churn_probability": 0.15,
                "churn_prediction": 0,
                "risk_level": "Low"
            },
            "expected_keywords": ["embajador", "VIP", "referidos"]
        },
        {
            "name": "Rule 7: Weekly Payment + Medium Risk",
            "description": "payment_type = weekly, medium churn risk",
            "data": {
                "age": 32,
                "housing": "r",
                "credit_score": 550,
                "deposits": 3,
                "withdrawal": 6,
                "purchases_partners": 4,
                "purchases": 18,
                "cc_taken": 0,
                "cc_recommended": 1,
                "cc_disliked": 0,
                "cc_liked": 0,
                "cc_application_begin": 0,
                "app_downloaded": 1,
                "web_user": 1,
                "app_web_user": 1,
                "ios_user": 0,
                "android_user": 1,
                "registered_phones": 1,
                "payment_type": "weekly",
                "waiting_4_loan": 0,
                "cancelled_loan": 0,
                "received_loan": 0,
                "rejected_loan": 0,
                "left_for_two_month_plus": 0,
                "left_for_one_month": 0,
                "rewards_earned": 80,
                "reward_rate": 0.025,
                "is_referred": 0,
                "churn_probability": 0.65,
                "churn_prediction": 1,
                "risk_level": "Medium"
            },
            "expected_keywords": ["pago", "flexibles", "quincenal"]
        },
        {
            "name": "Rule 8: Rented Home + High Credit + Waiting for Loan",
            "description": "housing = r, credit_score > 700, waiting_4_loan = 1",
            "data": {
                "age": 35,
                "housing": "r",
                "credit_score": 750,
                "deposits": 6,
                "withdrawal": 2,
                "purchases_partners": 8,
                "purchases": 25,
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
                "waiting_4_loan": 1,
                "cancelled_loan": 0,
                "received_loan": 0,
                "rejected_loan": 0,
                "left_for_two_month_plus": 0,
                "left_for_one_month": 0,
                "rewards_earned": 200,
                "reward_rate": 0.03,
                "is_referred": 0,
                "churn_probability": 0.3,
                "churn_prediction": 0,
                "risk_level": "Low"
            },
            "expected_keywords": ["hipotecario", "acelerar", "préstamo"]
        }
    ]
    
    # Test each rule
    passed_tests = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}/{total_tests}: {test_case['name']}")
        print(f"📝 {test_case['description']}")
        
        try:
            # Make API call
            response = requests.post(
                "http://localhost:8001/generate-insights",
                json=test_case['data'],
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                insights = result['recommendations']
                
                # Check if expected keywords are present
                keywords_found = []
                keywords_missing = []
                
                for keyword in test_case['expected_keywords']:
                    if keyword.lower() in insights.lower():
                        keywords_found.append(keyword)
                    else:
                        keywords_missing.append(keyword)
                
                if len(keywords_found) > 0:
                    print(f"✅ PASS - Found keywords: {', '.join(keywords_found)}")
                    passed_tests += 1
                    
                    if keywords_missing:
                        print(f"⚠️  Missing keywords: {', '.join(keywords_missing)}")
                else:
                    print(f"❌ FAIL - No expected keywords found")
                    print(f"   Expected: {', '.join(test_case['expected_keywords'])}")
                
                # Show a snippet of the insights
                print(f"📄 Insights preview: {insights[:150]}...")
                
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"🎯 TEST SUMMARY")
    print(f"   Passed: {passed_tests}/{total_tests}")
    print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("🎉 All enhanced rules are working correctly!")
    elif passed_tests > total_tests * 0.7:
        print("✅ Most rules are working - minor adjustments may be needed")
    else:
        print("⚠️  Several rules need attention - check implementation")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    # Check if API is running
    try:
        health_response = requests.get("http://localhost:8001/health", timeout=5)
        if health_response.status_code == 200:
            print("✅ LLM API is running")
            test_enhanced_rules()
        else:
            print("❌ LLM API health check failed")
    except requests.exceptions.ConnectionError:
        print("❌ LLM API is not running. Please start it with: python llm_api.py")
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")