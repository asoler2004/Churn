# 🚀 Quick Start Guide: Ollama Integration

Get up and running with Ollama-powered AI insights in 5 minutes!

## Prerequisites

- Python 3.8+
- 8GB+ RAM recommended
- Internet connection for initial model download

## Step 1: Install Ollama

### Windows
```bash
# Download and install from https://ollama.ai/download/windows
# Or use winget
winget install Ollama.Ollama
```

### macOS
```bash
# Download from https://ollama.ai/download/mac
# Or use Homebrew
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

## Step 2: Install a Model

```bash
# Install the recommended model (fast and efficient)
ollama pull llama3.2

# Optional: Install additional models
ollama pull mistral     # Alternative fast model
ollama pull llama3.1    # Higher quality, slower
ollama pull phi3        # Good for reasoning tasks
```

## Step 3: Verify Installation

```bash
# Check if Ollama is running
ollama list

# You should see something like:
# NAME            ID              SIZE    MODIFIED
# llama3.2:latest 1234567890ab    2.0GB   2 hours ago
```

## Step 4: Start the Services

```bash
# Terminal 1: Start Streamlit (Ollama works directly!)
streamlit run streamlit_ui.py

# Terminal 2: (Optional) Start LLM API for additional features
python llm_api.py
```

**Note**: Ollama now works independently! You don't need the LLM API running to use Ollama insights.

## Step 5: Test Integration

```bash
# Test Ollama standalone (no LLM API needed)
python test_ollama_standalone.py

# Or test full integration (requires LLM API)
python test_ollama_integration.py
```

You should see:
- ✅ Ollama is running!
- ✅ Quick insights generated successfully!
- ✅ Streamlit compatibility confirmed!

## Step 6: Use in the App

1. Open your browser to `http://localhost:8501`
2. Go to the **Datos de Clientes** tab and load some data
3. Select a customer and go to **Predicciones** tab
4. Run a prediction
5. Go to **Insights** tab
6. Select **"Ollama"** as AI method
7. Choose your model (e.g., "llama3.2")
8. Click **"Generar con Ollama"**

## 🎯 Quick Example

Here's a minimal Python example to test Ollama directly:

```python
from ollama_local import quick_generate_insights

# Sample customer data
customer_data = {
    "age": 35,
    "credit_score": 680,
    "churn_probability": 0.65,
    "risk_level": "High",
    "app_downloaded": 0,
    "cc_taken": 0,
    "purchases": 15,
    "rewards_earned": 120,
    # ... (other required fields with defaults)
}

# Generate insights
insights, error = quick_generate_insights(customer_data, model="llama3.2")

if insights:
    print("✅ Success!")
    print(insights)
else:
    print(f"❌ Error: {error}")
```

## 🔧 Troubleshooting

### "Connection refused" error
```bash
# Make sure Ollama is running
ollama serve

# Check if it's accessible
curl http://localhost:11434/api/tags
```

### "Model not found" error
```bash
# List installed models
ollama list

# Install missing model
ollama pull llama3.2
```

### Slow responses
- Use smaller models like `llama3.2` instead of `llama3.1`
- Ensure you have enough RAM (8GB+ recommended)
- Close other applications to free up memory

### API not starting
```bash
# Check if port 8001 is available
netstat -an | grep 8001

# Kill any process using the port (if needed)
# Then restart: python llm_api.py
```

## 🎨 Customization

### Change Default Model
Edit `ollama_local.py`:
```python
RECOMMENDED_MODELS = {
    'balanced': 'your-preferred-model',  # Change this
    # ...
}
```

### Adjust Response Length
In your code:
```python
from ollama_local import OllamaConfig, generate_ollama_insights

config = OllamaConfig(
    model="llama3.2",
    max_tokens=1500,  # Longer responses
    temperature=0.8   # More creative
)
```

## 📊 Performance Tips

1. **Model Selection**:
   - `llama3.2`: Best balance of speed/quality
   - `mistral`: Fastest option
   - `phi3`: Good for analytical tasks
   - `llama3.1`: Highest quality, slower

2. **Hardware**:
   - 16GB+ RAM for best performance
   - SSD storage for faster model loading
   - GPU support (if available) for faster inference

3. **Batch Processing**:
   - Use smaller models for batch analysis
   - Process customers in smaller chunks
   - Monitor system resources

## 🎉 Next Steps

Once you have Ollama working:

1. **Explore Models**: Try different models for various use cases
2. **Batch Analysis**: Use Ollama for processing multiple customers
3. **Custom Prompts**: Modify prompts in `ollama_local.py` for your needs
4. **Integration**: Use the REST API for your own applications

## 📚 Additional Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [Available Models](https://ollama.ai/library)
- [Model Comparison Guide](OLLAMA_SETUP.md#performance-comparison)
- [Usage Examples](ollama_usage_examples.py)

## 🆘 Need Help?

1. Run the diagnostic: `python test_ollama_integration.py`
2. Check the logs in your terminal
3. Verify Ollama is running: `ollama list`
4. Ensure all dependencies are installed: `pip install -r requirements.txt`

---

**🎯 Goal**: Generate high-quality, personalized customer retention insights using local AI models without sending data to external services.

**✅ Success**: When you can generate detailed, actionable insights for customer retention using Ollama models in under 30 seconds per customer.