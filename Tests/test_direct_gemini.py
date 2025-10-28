#!/usr/bin/env python3
"""
Test Gemini directly without CustomerData structure
"""

def test_direct_gemini():
    """Test Gemini with direct API call"""
    
    try:
        from gemini_api_call import get_api_key, setup_gemini_client
        import google.generativeai as genai
        
        # Get API key and setup
        api_key = get_api_key()
        if not api_key:
            print("❌ No API key found")
            return
            
        setup_gemini_client(api_key)
        
        # Simple test prompt
        simple_prompt = """You are a customer success consultant. A fintech customer has this profile:

- Age: 35 years
- Credit score: 680
- Monthly activity: 53 transactions
- Mobile app: Yes
- Rewards earned: 250 points

Please provide 3 brief recommendations in Spanish to improve this customer's experience and engagement with the platform."""

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
        
        print("🧪 Testing direct Gemini call...")
        
        try:
            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                safety_settings=safety_settings
            )
            
            response = model.generate_content(simple_prompt)
            
            if hasattr(response, 'text') and response.text:
                print("✅ Success!")
                print(f"Response: {response.text}")
                return True
            else:
                print("❌ No text in response")
                return False
                        
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Setup error: {e}")
        return False

if __name__ == "__main__":
    test_direct_gemini()