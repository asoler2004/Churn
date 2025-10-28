#!/usr/bin/env python3
"""
Gemini API Setup and Verification Script

This script helps set up and verify the Google Gemini API integration.
"""

import os
import sys
import subprocess
import json

def check_library_installation():
    """Check if the Google Generative AI library is installed"""
    try:
        import google.generativeai as genai
        print("✅ Google Generative AI library is installed")
        return True
    except ImportError as e:
        print("❌ Google Generative AI library not found")
        print(f"Error: {e}")
        return False

def install_library():
    """Install the Google Generative AI library"""
    print("📦 Installing Google Generative AI library...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "google-generativeai"
        ])
        print("✅ Library installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install library: {e}")
        return False

def setup_api_key():
    """Interactive API key setup"""
    print("\n🔑 API Key Setup")
    print("=" * 30)
    
    # Check if API key already exists
    existing_key = os.getenv('GEMINI_API_KEY')
    if existing_key:
        masked_key = existing_key[:8] + "..." + existing_key[-4:] if len(existing_key) > 12 else "***"
        print(f"✅ API key found in environment: {masked_key}")
        return existing_key
    
    # Check config file
    try:
        with open('gemini_config.json', 'r') as f:
            config = json.load(f)
            if config.get('api_key'):
                print("✅ API key found in gemini_config.json")
                return config['api_key']
    except FileNotFoundError:
        pass
    
    print("No API key found. Let's set one up!")
    print("\n📋 To get a Gemini API key:")
    print("1. Visit: https://makersuite.google.com/app/apikey")
    print("2. Sign in with your Google account")
    print("3. Click 'Create API Key'")
    print("4. Copy the generated key")
    
    api_key = input("\nEnter your Gemini API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("⏭️ Skipping API key setup")
        return None
    
    # Save to config file
    config = {
        "api_key": api_key,
        "default_model": "gemini-2.5-flash",
        "created_at": "2024-01-01T00:00:00"
    }
    
    try:
        with open('gemini_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        print("✅ API key saved to gemini_config.json")
        return api_key
    except Exception as e:
        print(f"❌ Failed to save API key: {e}")
        return api_key

def test_api_connection(api_key):
    """Test the Gemini API connection"""
    if not api_key:
        print("⏭️ Skipping API test (no API key)")
        return False
    
    print("\n🧪 Testing Gemini API Connection...")
    
    try:
        import google.generativeai as genai
        
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Test with a simple request
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Say 'Hello from Gemini!' in Spanish")
        
        if response.text:
            print("✅ Gemini API connection successful!")
            print(f"Test response: {response.text.strip()}")
            return True
        else:
            print("❌ Gemini API connected but returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        
        # Provide specific error guidance
        error_str = str(e).lower()
        if "api key" in error_str or "authentication" in error_str:
            print("💡 This looks like an API key issue:")
            print("   • Verify your API key is correct")
            print("   • Check if the key has proper permissions")
            print("   • Try generating a new key")
        elif "quota" in error_str or "limit" in error_str:
            print("💡 This looks like a quota/limit issue:")
            print("   • Check your API usage limits")
            print("   • Wait a moment and try again")
        elif "network" in error_str or "connection" in error_str:
            print("💡 This looks like a network issue:")
            print("   • Check your internet connection")
            print("   • Try again in a moment")
        
        return False

def create_example_usage():
    """Create an example usage file"""
    example_code = '''#!/usr/bin/env python3
"""
Simple Gemini API Usage Example
"""

from gemini_api_call import quick_gemini_insights, test_gemini_connection

def main():
    # Test connection
    status = test_gemini_connection()
    if not status['available']:
        print(f"❌ Gemini not available: {status['message']}")
        return
    
    # Sample customer data
    customer_data = {
        "age": 35,
        "housing": "r",
        "credit_score": 680.0,
        "deposits": 15,
        "withdrawal": 8,
        "purchases_partners": 20,
        "purchases": 30,
        "cc_taken": 1,
        "cc_recommended": 1,
        "cc_disliked": 0,
        "cc_liked": 1,
        "cc_application_begin": 1,
        "app_downloaded": 1,
        "web_user": 1,
        "app_web_user": 1,
        "ios_user": 0,
        "android_user": 1,
        "registered_phones": 1,
        "payment_type": "monthly",
        "waiting_4_loan": 0,
        "cancelled_loan": 0,
        "received_loan": 1,
        "rejected_loan": 0,
        "left_for_two_month_plus": 0,
        "left_for_one_month": 0,
        "rewards_earned": 250,
        "reward_rate": 0.025,
        "is_referred": 1,
        "churn_probability": 0.30,
        "churn_prediction": 0,
        "risk_level": "Medium"
    }
    
    print("🤖 Generating insights with Gemini...")
    insights, error = quick_gemini_insights(customer_data)
    
    if insights:
        print("✅ Success!")
        print("=" * 50)
        print(insights[:500] + "..." if len(insights) > 500 else insights)
    else:
        print(f"❌ Error: {error}")

if __name__ == "__main__":
    main()
'''
    
    try:
        with open('gemini_example.py', 'w') as f:
            f.write(example_code)
        print("✅ Created gemini_example.py")
        return True
    except Exception as e:
        print(f"❌ Failed to create example: {e}")
        return False

def main():
    """Main setup process"""
    print("🤖 GEMINI API SETUP WIZARD")
    print("=" * 40)
    
    # Step 1: Check library installation
    print("\n1. Checking library installation...")
    if not check_library_installation():
        print("\n📦 Installing required library...")
        if not install_library():
            print("❌ Setup failed. Please install manually:")
            print("   pip install google-generativeai")
            return
        
        # Verify installation
        if not check_library_installation():
            print("❌ Library installation verification failed")
            return
    
    # Step 2: Setup API key
    print("\n2. Setting up API key...")
    api_key = setup_api_key()
    
    # Step 3: Test connection
    if api_key:
        print("\n3. Testing API connection...")
        connection_success = test_api_connection(api_key)
    else:
        connection_success = False
        print("\n⏭️ Skipping connection test (no API key)")
    
    # Step 4: Create example
    print("\n4. Creating usage example...")
    create_example_usage()
    
    # Final summary
    print("\n" + "=" * 40)
    print("📊 SETUP SUMMARY")
    print("=" * 40)
    
    print(f"Library installed: ✅")
    print(f"API key configured: {'✅' if api_key else '❌'}")
    print(f"Connection test: {'✅' if connection_success else '❌' if api_key else '⏭️'}")
    print(f"Example created: ✅")
    
    if connection_success:
        print("\n🎉 Gemini API setup complete!")
        print("You can now use Gemini for AI insights.")
        print("\nNext steps:")
        print("• Run: python gemini_example.py")
        print("• Use Gemini in Streamlit UI")
        print("• Run: python test_gemini_integration.py")
    elif api_key:
        print("\n⚠️ Setup partially complete")
        print("API key is configured but connection test failed.")
        print("Check the error messages above for guidance.")
    else:
        print("\n💡 Setup incomplete")
        print("To complete setup:")
        print("1. Get API key from: https://makersuite.google.com/app/apikey")
        print("2. Run this script again")
        print("3. Or set GEMINI_API_KEY environment variable")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Setup interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()