# 🤖 Gemini API Setup Guide

This guide will help you set up Google's Gemini API for enhanced AI insights in the fintech churn prediction system.

## 🚀 Quick Setup

Run the automated setup wizard:
```bash
python setup_gemini.py
```

This will:
- Install required libraries
- Help you configure your API key
- Test the connection
- Create usage examples

## 📋 Manual Setup

### 1. Install Required Library

```bash
pip install google-generativeai
```

Or update your requirements:
```bash
pip install -r requirements.txt
```

### 2. Get API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated key

### 3. Configure API Key

**Option A: Environment Variable**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

**Option B: Config File**
Create `gemini_config.json`:
```json
{
  "api_key": "your-api-key-here",
  "default_model": "gemini-2.5-flash"
}
```

**Option C: .env File**
Create `.env`:
```
GEMINI_API_KEY=your-api-key-here
```

### 4. Test Setup

```bash
python test_gemini_integration.py
```

## 🎯 Usage in Streamlit

Once configured, Gemini will appear as an option in the Streamlit UI:

1. Start Streamlit: `streamlit run streamlit_ui.py`
2. Go to **Insights** tab
3. Select **"Gemini"** as AI method
4. Choose your model (gemini-2.5-flash recommended)
5. Generate insights!

## 🤖 Available Models

| Model | Speed | Quality | Cost | Best For |
|-------|-------|---------|------|----------|
| `gemini-2.5-flash` | ⚡⚡⚡ | ⭐⭐⭐⭐ | $ | **Recommended** |
| `gemini-pro-vision` | ⚡⚡ | ⭐⭐⭐⭐ | $ | Text + Vision |

**Note**: Run `python discover_gemini_models.py` to see all available models in your region.

## 🔧 Configuration Options

### Basic Configuration
```python
from gemini_api_call import GeminiConfig

config = GeminiConfig(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_output_tokens=2048
)
```

### Advanced Configuration
```python
config = GeminiConfig(
    model="gemini-2.5-flash",
    temperature=0.8,          # More creative
    max_output_tokens=3000,   # Longer responses
    top_p=0.95,
    top_k=50,
    timeout=60
)
```

## 📊 Performance Comparison

| Method | Speed | Quality | Privacy | Cost |
|--------|-------|---------|---------|------|
| Rule-based | ⚡⚡⚡ | ⭐⭐ | ✅ | Free |
| Ollama | ⚡⚡ | ⭐⭐⭐⭐ | ✅ | Free |
| **Gemini** | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | ⚠️ | $ |
| Transformers | ⚡ | ⭐⭐⭐ | ✅ | Free |

## 🛠️ Troubleshooting

### Common Issues

#### "Module has no attribute 'configure'"
```bash
# Reinstall the correct library
pip uninstall google-genai google-generativeai
pip install google-generativeai
```

#### "API key not found"
```bash
# Check environment variable
echo $GEMINI_API_KEY

# Or run setup wizard
python setup_gemini.py
```

#### "Authentication failed"
- Verify your API key is correct
- Check if the key has proper permissions
- Try generating a new key

#### "Quota exceeded"
- Check your API usage limits
- Wait for quota reset
- Consider upgrading your plan

### Debug Commands

```bash
# Test library installation
python -c "import google.generativeai; print('✅ Library OK')"

# Test API key
python -c "from gemini_api_call import get_api_key; print('Key found:', bool(get_api_key()))"

# Full connection test
python -c "from gemini_api_call import test_gemini_connection; print(test_gemini_connection())"
```

## 💡 Usage Examples

### Simple Usage
```python
from gemini_api_call import quick_gemini_insights

customer_data = {
    "age": 35,
    "credit_score": 680,
    "churn_probability": 0.45,
    "risk_level": "Medium",
    # ... other fields
}

insights, error = quick_gemini_insights(customer_data)
if insights:
    print(insights)
else:
    print(f"Error: {error}")
```

### Advanced Usage
```python
from gemini_api_call import generate_gemini_insights, GeminiConfig

config = GeminiConfig(
    model="gemini-2.5-flash",
    temperature=0.8,
    max_output_tokens=3000
)

insights, debug_info = generate_gemini_insights(customer_data, config)
print(f"Generated in {debug_info['generation_time']:.2f} seconds")
```

## 🔒 Security & Privacy

### Data Handling
- Personal information (names, emails, etc.) is automatically excluded
- Only behavioral and financial metrics are sent to Gemini
- No data is stored by Google beyond the API call

### Best Practices
- Use environment variables for API keys
- Don't commit API keys to version control
- Rotate API keys regularly
- Monitor API usage and costs

## 💰 Cost Management

### Pricing (as of 2024)
- **gemini-2.5-flash**: ~$0.075 per 1K tokens
- **gemini-1.5-pro**: ~$1.25 per 1K tokens

### Cost Optimization
- Use `gemini-2.5-flash` for most cases
- Set reasonable `max_output_tokens` limits
- Monitor usage in Google Cloud Console
- Consider batch processing for multiple customers

## 🎯 Integration Benefits

### Advantages of Gemini
- **High Quality**: State-of-the-art language model
- **Fast Response**: Optimized for speed
- **Comprehensive Analysis**: Detailed customer insights
- **Reliable**: Google's robust infrastructure

### When to Use Gemini
- Need highest quality insights
- Processing important/high-value customers
- Require detailed analysis
- Have API budget available

### When to Use Alternatives
- **Ollama**: For privacy-first approach
- **Rule-based**: For fast, consistent results
- **Transformers**: For offline processing

---

## 🆘 Need Help?

1. **Run setup wizard**: `python setup_gemini.py`
2. **Check documentation**: [Google AI Studio Docs](https://ai.google.dev/)
3. **Test integration**: `python test_gemini_integration.py`
4. **Check API status**: [Google Cloud Status](https://status.cloud.google.com/)

**Quick Setup Command:**
```bash
pip install google-generativeai && python setup_gemini.py
```