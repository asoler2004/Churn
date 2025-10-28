# 🕐 Ollama Timeout Troubleshooting Guide

If you're experiencing "Timeout al conectar con Ollama" errors, this guide will help you resolve them quickly.

## 🔍 Quick Diagnosis

Run this command to check your Ollama setup:
```bash
python ollama_troubleshoot.py quick
```

Or for a comprehensive diagnosis:
```bash
python ollama_troubleshoot.py
```

## 🚀 Common Solutions

### 1. **First Model Load (Most Common)**
**Problem**: First time loading a model takes 1-2 minutes
**Solution**: 
- Wait patiently for the first load
- Subsequent requests will be much faster
- Use smaller models for faster loading

```bash
# Use faster models
ollama pull llama3.2    # Recommended: Fast and efficient
ollama pull phi3        # Alternative: Very fast
```

### 2. **Ollama Not Running**
**Problem**: Ollama service is not started
**Solution**:
```bash
# Start Ollama service
ollama serve

# Or restart if already running
pkill ollama
ollama serve
```

### 3. **No Models Installed**
**Problem**: No models available
**Solution**:
```bash
# Install a fast model
ollama pull llama3.2

# Verify installation
ollama list
```

### 4. **System Resources**
**Problem**: Insufficient memory or CPU
**Solution**:
- Close other applications
- Use smaller models (llama3.2 instead of llama3.1)
- Restart your computer if memory is very low

### 5. **Model Loading Issues**
**Problem**: Specific model won't load
**Solution**:
```bash
# Try a different model
ollama pull llama3.2
ollama pull phi3

# Remove problematic model and reinstall
ollama rm problematic-model
ollama pull problematic-model
```

## ⚡ Performance Optimization

### Model Speed Comparison
| Model | Speed | Quality | Memory | Best For |
|-------|-------|---------|---------|----------|
| `phi3` | ⚡⚡⚡ | ⭐⭐⭐ | 2GB | Quick insights |
| `llama3.2` | ⚡⚡ | ⭐⭐⭐⭐ | 3GB | **Recommended** |
| `llama3.1` | ⚡ | ⭐⭐⭐⭐⭐ | 5GB | High quality |
| `mistral` | ⚡⚡ | ⭐⭐⭐⭐ | 4GB | Good balance |

### Timeout Settings
If you need longer timeouts, modify these files:

**In `ollama_local.py`:**
```python
timeout: int = 180  # 3 minutes instead of 2
```

**In `streamlit_ui.py`:**
```python
timeout=180  # Extended timeout
```

## 🔧 Advanced Troubleshooting

### Check Ollama Status
```bash
# Check if Ollama is responding
curl http://localhost:11434/api/tags

# Check system resources
python -c "import psutil; print(f'Memory: {psutil.virtual_memory().available/1024**3:.1f}GB available')"
```

### Reset Ollama
```bash
# Complete reset (removes all models)
ollama rm $(ollama list | grep -v NAME | awk '{print $1}')
ollama pull llama3.2
```

### Alternative Port
If port 11434 is busy:
```bash
# Start on different port
OLLAMA_HOST=0.0.0.0:11435 ollama serve

# Update config in ollama_local.py
base_url: str = "http://localhost:11435"
```

## 📊 System Requirements

### Minimum Requirements
- **RAM**: 4GB available
- **Storage**: 2GB free space
- **CPU**: Any modern processor

### Recommended Requirements
- **RAM**: 8GB+ available
- **Storage**: 10GB+ free space
- **CPU**: Multi-core processor

## 🆘 Still Having Issues?

### 1. Check Logs
```bash
# Check Ollama logs (varies by system)
# macOS/Linux:
tail -f ~/.ollama/logs/server.log

# Windows:
# Check Event Viewer or Ollama application logs
```

### 2. Restart Everything
```bash
# Kill all Ollama processes
pkill ollama

# Restart Ollama
ollama serve

# Restart Streamlit
streamlit run streamlit_ui.py
```

### 3. Use Alternative AI Methods
If Ollama continues to have issues:
- Use **Gemini API** (requires API key)
- Use **Transformers** (if LLM API is running)
- Use **Rule-based insights** (always available)

### 4. Get Help
1. Run full diagnosis: `python ollama_troubleshoot.py`
2. Check system resources
3. Try different models
4. Consider system upgrade if resources are insufficient

## 💡 Prevention Tips

1. **Keep Ollama Updated**: `ollama --version` and update if needed
2. **Monitor Resources**: Don't run too many heavy applications simultaneously
3. **Use Appropriate Models**: Match model size to your system capabilities
4. **Regular Maintenance**: Restart Ollama service periodically

---

**Quick Commands Summary:**
```bash
# Diagnosis
python ollama_troubleshoot.py quick

# Reset and reinstall
ollama pull llama3.2

# Start service
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```