# 🦙 Ollama Integration Setup Guide

This guide will help you set up Ollama for enhanced AI insights in the fintech churn prediction system.

## What is Ollama?

Ollama is a local LLM (Large Language Model) runner that allows you to run powerful AI models like Llama, Mistral, and others directly on your machine without sending data to external APIs.

## Benefits of Using Ollama

- **Privacy**: All data stays on your machine
- **No API costs**: Free to use once installed
- **Better insights**: More sophisticated AI analysis than rule-based approaches
- **Customizable**: Choose from various models based on your needs
- **Offline capable**: Works without internet connection

## Installation Steps

### 1. Install Ollama

**Windows:**
- Download from: https://ollama.ai/download/windows
- Run the installer and follow the setup wizard

**macOS:**
- Download from: https://ollama.ai/download/mac
- Or use Homebrew: `brew install ollama`

**Linux:**
- Run: `curl -fsSL https://ollama.ai/install.sh | sh`

### 2. Install a Model

After installing Ollama, you need to download at least one model. We recommend starting with Llama 3.2:

```bash
# Install the recommended model (3B parameters, good balance of speed/quality)
ollama pull llama3.2

# Alternative models you can try:
ollama pull llama3.1        # Larger, more capable
ollama pull mistral         # Fast and efficient
ollama pull phi3           # Microsoft's model, good for reasoning
ollama pull codellama      # Specialized for code analysis
```

### 3. Start Ollama Service

Ollama usually starts automatically, but you can manually start it:

```bash
# Start Ollama service
ollama serve
```

The service will run on `http://localhost:11434`

### 4. Verify Installation

Run our test script to verify everything is working:

```bash
python test_ollama_integration.py
```

You should see:
- ✅ Ollama is running!
- ✅ LLM API is running!
- ✅ Ollama insights generated successfully!

## Using Ollama in the App

Once Ollama is set up:

1. **Start the LLM API**: `python llm_api.py`
2. **Start Streamlit**: `streamlit run streamlit_ui.py`
3. **Navigate to Insights tab**
4. **Select "Ollama" as AI method**
5. **Choose your preferred model**
6. **Generate insights!**

## Model Recommendations

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| `llama3.2` | 3B | Fast | Good | General insights, recommended |
| `llama3.1` | 8B | Medium | Excellent | Detailed analysis |
| `mistral` | 7B | Fast | Very Good | Quick insights |
| `phi3` | 3.8B | Fast | Good | Reasoning tasks |
| `codellama` | 7B | Medium | Good | Technical analysis |

## Troubleshooting

### Ollama Not Starting
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start manually
ollama serve
```

### Model Not Found
```bash
# List installed models
ollama list

# Install missing model
ollama pull llama3.2
```

### Performance Issues
- Use smaller models (llama3.2, phi3) for faster responses
- Ensure you have enough RAM (8GB+ recommended)
- Close other applications to free up resources

### Connection Errors
- Verify Ollama is running on port 11434
- Check firewall settings
- Restart Ollama service

## Advanced Configuration

### Custom Model Parameters

You can customize model behavior by modifying the Ollama request in `llm_api.py`:

```python
payload = {
    "model": model_name,
    "prompt": prompt,
    "stream": False,
    "options": {
        "temperature": 0.7,    # Creativity (0.0-1.0)
        "top_p": 0.9,         # Nucleus sampling
        "max_tokens": 1000,   # Response length
        "stop": ["Human:", "Assistant:"]
    }
}
```

### Multiple Models

You can install multiple models and switch between them in the UI:

```bash
ollama pull llama3.2
ollama pull mistral
ollama pull phi3
```

Then select different models in the Streamlit interface for different use cases.

## Performance Comparison

Based on our testing:

| Method | Speed | Quality | Privacy | Cost |
|--------|-------|---------|---------|------|
| Rule-based | ⚡⚡⚡ | ⭐⭐ | ✅ | Free |
| Transformers | ⚡⚡ | ⭐⭐⭐ | ✅ | Free |
| Ollama | ⚡ | ⭐⭐⭐⭐ | ✅ | Free |
| External API | ⚡⚡ | ⭐⭐⭐⭐⭐ | ❌ | $$$ |

## Next Steps

1. Install Ollama following the steps above
2. Run the test script to verify setup
3. Try different models to find your preferred balance of speed vs quality
4. Use Ollama insights for better customer retention strategies!

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Run `python test_ollama_integration.py` for diagnostics
3. Check Ollama logs: `ollama logs`
4. Visit Ollama documentation: https://ollama.ai/docs