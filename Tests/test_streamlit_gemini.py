#!/usr/bin/env python3
"""
Quick test for Streamlit Gemini integration
"""

def test_gemini_imports():
    """Test if all Gemini functions can be imported"""
    try:
        from gemini_api_call import (
            generate_gemini_insights,
            quick_gemini_insights,
            test_gemini_connection,
            is_gemini_available,
            get_available_models,
            GeminiConfig
        )
        print("✅ All Gemini imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_gemini_availability():
    """Test if Gemini is available and configured"""
    try:
        from gemini_api_call import is_gemini_available, test_gemini_connection
        
        if is_gemini_available():
            print("✅ Gemini API key is configured")
            
            # Test connection
            status = test_gemini_connection()
            if status['available']:
                print("✅ Gemini API connection successful")
                print(f"   Test response: {status.get('test_response', 'N/A')}")
                return True
            else:
                print(f"❌ Gemini API connection failed: {status['message']}")
                return False
        else:
            print("❌ Gemini API key not configured")
            return False
    except Exception as e:
        print(f"❌ Error testing Gemini: {e}")
        return False

def test_streamlit_functions():
    """Test Streamlit-specific Gemini functions"""
    try:
        # Import the functions used in Streamlit
        import sys
        import os
        sys.path.append(os.path.dirname(__file__))
        
        from streamlit_ui import (
            get_gemini_insights_direct,
            check_gemini_status_direct,
            get_available_gemini_models_direct
        )
        
        print("✅ Streamlit Gemini functions imported successfully")
        
        # Test status check
        status = check_gemini_status_direct()
        print(f"   Gemini status: {'✅ Available' if status else '❌ Not available'}")
        
        # Test model list
        models = get_available_gemini_models_direct()
        print(f"   Available models: {len(models)} found")
        if models:
            print(f"   Models: {', '.join(models[:3])}{'...' if len(models) > 3 else ''}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing Streamlit functions: {e}")
        return False

def main():
    print("🤖 Testing Streamlit Gemini Integration")
    print("=" * 50)
    
    # Test 1: Imports
    print("\n1. Testing imports...")
    imports_ok = test_gemini_imports()
    
    # Test 2: Availability
    print("\n2. Testing Gemini availability...")
    availability_ok = test_gemini_availability()
    
    # Test 3: Streamlit functions
    print("\n3. Testing Streamlit functions...")
    streamlit_ok = test_streamlit_functions()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Imports: {'✅' if imports_ok else '❌'}")
    print(f"   Availability: {'✅' if availability_ok else '❌'}")
    print(f"   Streamlit functions: {'✅' if streamlit_ok else '❌'}")
    
    if all([imports_ok, availability_ok, streamlit_ok]):
        print("\n🎉 All tests passed! Gemini integration should work in Streamlit.")
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
        
        if not availability_ok:
            print("\n💡 To fix Gemini availability:")
            print("   1. Get API key from: https://makersuite.google.com/app/apikey")
            print("   2. Run: python setup_gemini.py")
            print("   3. Or set: export GEMINI_API_KEY='your-key'")

if __name__ == "__main__":
    main()