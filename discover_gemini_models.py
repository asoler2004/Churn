#!/usr/bin/env python3
"""
Gemini Model Discovery Script

This script discovers available Gemini models and their capabilities.
"""

import os
import json

def discover_models():
    """Discover available Gemini models"""
    try:
        import google.generativeai as genai
        
        # Get API key
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            try:
                with open('gemini_config.json', 'r') as f:
                    config = json.load(f)
                    api_key = config.get('api_key')
            except FileNotFoundError:
                pass
        
        if not api_key:
            print("❌ No API key found. Please set GEMINI_API_KEY or run setup_gemini.py")
            return
        
        # Configure API
        genai.configure(api_key=api_key)
        
        print("🔍 Discovering available Gemini models...")
        print("=" * 50)
        
        # List all models
        models = genai.list_models()
        
        generation_models = []
        other_models = []
        
        for model in models:
            model_info = {
                'name': model.name,
                'display_name': model.display_name,
                'description': model.description,
                'supported_methods': model.supported_generation_methods,
                'input_token_limit': getattr(model, 'input_token_limit', 'Unknown'),
                'output_token_limit': getattr(model, 'output_token_limit', 'Unknown')
            }
            
            if 'generateContent' in model.supported_generation_methods:
                generation_models.append(model_info)
            else:
                other_models.append(model_info)
        
        # Display generation models (what we need)
        print(f"✅ Found {len(generation_models)} models supporting text generation:")
        print()
        
        for i, model in enumerate(generation_models, 1):
            # Extract short name
            short_name = model['name'].split('/')[-1] if '/' in model['name'] else model['name']
            
            print(f"{i}. {short_name}")
            print(f"   Full name: {model['name']}")
            print(f"   Display: {model['display_name']}")
            print(f"   Description: {model['description'][:100]}...")
            print(f"   Input limit: {model['input_token_limit']}")
            print(f"   Output limit: {model['output_token_limit']}")
            print(f"   Methods: {', '.join(model['supported_methods'])}")
            print()
        
        # Test the first available model
        if generation_models:
            test_model_name = generation_models[0]['name']
            print(f"🧪 Testing model: {test_model_name}")
            
            try:
                model = genai.GenerativeModel(test_model_name)
                response = model.generate_content("Say hello in Spanish")
                
                if response.text:
                    print(f"✅ Test successful!")
                    print(f"Response: {response.text.strip()}")
                else:
                    print("❌ Test failed: Empty response")
                    
            except Exception as e:
                print(f"❌ Test failed: {e}")
        
        # Show other models for reference
        if other_models:
            print(f"\n📋 Other available models ({len(other_models)}):")
            for model in other_models:
                short_name = model['name'].split('/')[-1] if '/' in model['name'] else model['name']
                print(f"   • {short_name} - {', '.join(model['supported_methods'])}")
        
        # Generate updated model configuration
        print("\n" + "=" * 50)
        print("📝 Recommended configuration update:")
        print("=" * 50)
        
        if generation_models:
            # Create updated GEMINI_MODELS dict
            working_models = [model['name'].split('/')[-1] for model in generation_models[:4]]
            
            print("Update GEMINI_MODELS in gemini_api_call.py:")
            print()
            print("GEMINI_MODELS = {")
            if len(working_models) >= 1:
                print(f"    'fast': '{working_models[0]}',")
                print(f"    'balanced': '{working_models[0]}',")
            if len(working_models) >= 2:
                print(f"    'quality': '{working_models[1]}',")
            else:
                print(f"    'quality': '{working_models[0]}',")
            if len(working_models) >= 3:
                print(f"    'legacy': '{working_models[2]}'")
            else:
                print(f"    'legacy': '{working_models[0]}'")
            print("}")
            
            print(f"\nDefault model: {working_models[0]}")
            
        return generation_models
        
    except ImportError:
        print("❌ google-generativeai library not installed")
        print("Run: pip install google-generativeai")
        return None
    except Exception as e:
        print(f"❌ Error discovering models: {e}")
        return None

def test_specific_model(model_name):
    """Test a specific model"""
    try:
        import google.generativeai as genai
        
        # Get API key
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            try:
                with open('gemini_config.json', 'r') as f:
                    config = json.load(f)
                    api_key = config.get('api_key')
            except FileNotFoundError:
                pass
        
        if not api_key:
            print("❌ No API key found")
            return False
        
        genai.configure(api_key=api_key)
        
        print(f"🧪 Testing model: {model_name}")
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Respond with 'Test successful' in Spanish")
        
        if response.text:
            print(f"✅ Success: {response.text.strip()}")
            return True
        else:
            print("❌ Empty response")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1:
        # Test specific model
        model_name = sys.argv[1]
        test_specific_model(model_name)
    else:
        # Discover all models
        models = discover_models()
        
        if models:
            print(f"\n💡 To test a specific model, run:")
            print(f"python {sys.argv[0]} <model-name>")
            print(f"\nExample:")
            short_name = models[0]['name'].split('/')[-1]
            print(f"python {sys.argv[0]} {short_name}")

if __name__ == "__main__":
    main()