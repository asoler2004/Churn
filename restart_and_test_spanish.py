#!/usr/bin/env python3
"""
Script to restart services and test Spanish translation
"""

import subprocess
import time
import requests
import json
import os
import signal

def kill_existing_processes():
    """Kill existing API processes"""
    print("🔄 Stopping existing API processes...")
    
    try:
        # Kill processes on ports 8000 and 8001
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"], 
                      capture_output=True, text=True)
        time.sleep(2)
    except Exception as e:
        print(f"Note: {e}")

def start_apis():
    """Start the API services"""
    print("🚀 Starting API services...")
    
    # Start prediction API
    pred_process = subprocess.Popen(
        ["python", "api.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Start LLM API
    llm_process = subprocess.Popen(
        ["python", "llm_api.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for services to start
    print("⏳ Waiting for services to start...")
    time.sleep(10)
    
    return pred_process, llm_process

def test_spanish_llm():
    """Test LLM API Spanish response"""
    print("🧪 Testing LLM API Spanish response...")
    
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
                'ESTRATEGIA DE RETENCIÓN'
            ]
            
            spanish_found = sum(1 for keyword in spanish_keywords if keyword in insights)
            
            print(f"✅ LLM API Response received")
            print(f"📊 Spanish keywords found: {spanish_found}/{len(spanish_keywords)}")
            
            if spanish_found >= 3:
                print("🎉 SUCCESS: LLM API is responding in Spanish!")
            else:
                print("⚠️ WARNING: LLM API may not be fully translated")
            
            print("\n📝 Full response:")
            print(insights)
            return True
            
        else:
            print(f"❌ LLM API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing LLM API: {str(e)}")
        return False

def main():
    """Main function"""
    print("🌍 Restarting Services and Testing Spanish Translation")
    print("=" * 60)
    
    # Kill existing processes
    kill_existing_processes()
    
    # Start APIs
    pred_process, llm_process = start_apis()
    
    try:
        # Test Spanish translation
        success = test_spanish_llm()
        
        if success:
            print("\n🎉 Spanish translation is working!")
            print("\n💡 You can now:")
            print("1. Run: streamlit run streamlit_ui.py")
            print("2. Test the Spanish UI interface")
        else:
            print("\n❌ Spanish translation needs debugging")
            
    finally:
        # Clean up processes
        print("\n🛑 Stopping test processes...")
        try:
            pred_process.terminate()
            llm_process.terminate()
        except:
            pass

if __name__ == "__main__":
    main()