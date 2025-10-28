#!/usr/bin/env python3
"""
Test Gemini with a simple prompt to isolate the issue
"""

def test_simple_gemini():
    """Test Gemini with a very simple prompt"""
    
    try:
        from gemini_api_call import GeminiConfig, setup_gemini_client, get_api_key
        import google.generativeai as genai
        
        # Get API key and setup
        api_key = get_api_key()
        if not api_key:
            print("❌ No API key found")
            return
            
        setup_gemini_client(api_key)
        
        # Simple test prompt
        simple_prompt = """You are a business analyst. 

A customer has the following profile:
- Age: 35 years old
- Credit score: 680
- Monthly transactions: 25
- Uses mobile app: Yes
- Risk level: Medium

Please provide 3 brief recommendations to improve customer retention."""

        # Configure safety settings
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH", 
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            }
        ]
        
        # Test with different models
        models_to_test = ["gemini-2.5-flash", "gemini-pro"]
        
        for model_name in models_to_test:
            print(f"\n🧪 Testing {model_name}...")
            
            try:
                model = genai.GenerativeModel(
                    model_name=model_name,
                    safety_settings=safety_settings
                )
                
                response = model.generate_content(simple_prompt)
                
                if hasattr(response, 'text') and response.text:
                    print(f"✅ {model_name} works!")
                    print(f"Response: {response.text[:200]}...")
                    return True
                else:
                    print(f"❌ {model_name} blocked response")
                    if hasattr(response, 'candidates') and response.candidates:
                        finish_reason = response.candidates[0].finish_reason
                        print(f"   Finish reason: {finish_reason}")
                        
            except Exception as e:
                print(f"❌ {model_name} error: {e}")
        
        return False
        
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

if __name__ == "__main__":
    print("🤖 Testing Simple Gemini Prompt")
    print("=" * 40)
    test_simple_gemini()