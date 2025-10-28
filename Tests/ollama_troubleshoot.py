#!/usr/bin/env python3
"""
Ollama Troubleshooting and Diagnostic Tool

This script helps diagnose and fix common Ollama issues.
"""

import requests
import time
import subprocess
import sys
from typing import Dict, Any, List, Tuple

def check_ollama_service() -> Dict[str, Any]:
    """Check if Ollama service is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            return {
                'running': True,
                'status': 'healthy',
                'message': 'Ollama service is running normally'
            }
        else:
            return {
                'running': False,
                'status': 'error',
                'message': f'Ollama service responded with status {response.status_code}'
            }
    except requests.exceptions.ConnectionError:
        return {
            'running': False,
            'status': 'not_running',
            'message': 'Ollama service is not running or not accessible'
        }
    except requests.exceptions.Timeout:
        return {
            'running': True,
            'status': 'slow',
            'message': 'Ollama service is running but responding slowly'
        }
    except Exception as e:
        return {
            'running': False,
            'status': 'error',
            'message': f'Error checking Ollama service: {str(e)}'
        }

def get_installed_models() -> List[str]:
    """Get list of installed Ollama models"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        return []
    except:
        return []

def test_model_loading(model_name: str) -> Dict[str, Any]:
    """Test if a specific model can be loaded"""
    try:
        # Simple test prompt
        payload = {
            "model": model_name,
            "prompt": "Test",
            "stream": False,
            "options": {
                "max_tokens": 10
            }
        }
        
        print(f"Testing model {model_name}... (this may take 30-60 seconds)")
        start_time = time.time()
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=90
        )
        
        load_time = time.time() - start_time
        
        if response.status_code == 200:
            return {
                'success': True,
                'load_time': load_time,
                'message': f'Model {model_name} loaded successfully in {load_time:.1f} seconds'
            }
        else:
            return {
                'success': False,
                'load_time': load_time,
                'message': f'Model {model_name} failed to load: {response.status_code}'
            }
            
    except requests.exceptions.Timeout:
        return {
            'success': False,
            'load_time': 90,
            'message': f'Model {model_name} timed out during loading (>90s)'
        }
    except Exception as e:
        return {
            'success': False,
            'load_time': 0,
            'message': f'Error testing model {model_name}: {str(e)}'
        }

def get_system_resources() -> Dict[str, Any]:
    """Get system resource information"""
    try:
        import psutil
        
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'memory_total_gb': memory.total / (1024**3),
            'memory_available_gb': memory.available / (1024**3),
            'memory_percent': memory.percent,
            'disk_free_gb': disk.free / (1024**3),
            'cpu_count': psutil.cpu_count()
        }
    except ImportError:
        return {
            'error': 'psutil not available - install with: pip install psutil'
        }
    except Exception as e:
        return {
            'error': f'Error getting system info: {str(e)}'
        }

def suggest_solutions(service_status: Dict, models: List[str], resources: Dict) -> List[str]:
    """Suggest solutions based on diagnostic results"""
    suggestions = []
    
    # Service issues
    if not service_status['running']:
        if service_status['status'] == 'not_running':
            suggestions.append("🔧 Start Ollama service:")
            suggestions.append("   • Run: ollama serve")
            suggestions.append("   • Or restart Ollama application")
        elif service_status['status'] == 'error':
            suggestions.append("🔧 Restart Ollama service:")
            suggestions.append("   • Kill existing processes: pkill ollama")
            suggestions.append("   • Start fresh: ollama serve")
    
    # Model issues
    if not models:
        suggestions.append("📦 Install a model:")
        suggestions.append("   • Fast model: ollama pull llama3.2")
        suggestions.append("   • Quality model: ollama pull llama3.1")
        suggestions.append("   • Lightweight: ollama pull phi3")
    
    # Resource issues
    if 'memory_available_gb' in resources:
        if resources['memory_available_gb'] < 4:
            suggestions.append("💾 Low memory detected:")
            suggestions.append("   • Close other applications")
            suggestions.append("   • Use smaller models (llama3.2, phi3)")
            suggestions.append("   • Consider upgrading RAM")
        
        if resources['memory_available_gb'] < 2:
            suggestions.append("⚠️ Critical memory shortage:")
            suggestions.append("   • System may be too low on memory for Ollama")
            suggestions.append("   • Try restarting your computer")
    
    # Performance suggestions
    if service_status.get('status') == 'slow':
        suggestions.append("🐌 Performance optimization:")
        suggestions.append("   • Use faster models: llama3.2 instead of llama3.1")
        suggestions.append("   • Reduce max_tokens in requests")
        suggestions.append("   • Close other heavy applications")
    
    # Timeout-specific suggestions
    suggestions.append("⏱️ For timeout issues:")
    suggestions.append("   • First model load takes longer (1-2 minutes)")
    suggestions.append("   • Subsequent requests are much faster")
    suggestions.append("   • Try smaller models first: ollama pull llama3.2")
    suggestions.append("   • Increase timeout in application settings")
    
    return suggestions

def run_comprehensive_diagnosis():
    """Run complete Ollama diagnosis"""
    print("🔍 OLLAMA COMPREHENSIVE DIAGNOSIS")
    print("=" * 50)
    
    # Check service
    print("\n1. Checking Ollama service...")
    service_status = check_ollama_service()
    print(f"   Status: {service_status['status']}")
    print(f"   Message: {service_status['message']}")
    
    # Check models
    print("\n2. Checking installed models...")
    models = get_installed_models()
    if models:
        print(f"   Found {len(models)} models:")
        for model in models:
            print(f"   • {model}")
    else:
        print("   No models found")
    
    # Check resources
    print("\n3. Checking system resources...")
    resources = get_system_resources()
    if 'error' in resources:
        print(f"   {resources['error']}")
    else:
        print(f"   Memory: {resources['memory_available_gb']:.1f}GB available / {resources['memory_total_gb']:.1f}GB total")
        print(f"   Memory usage: {resources['memory_percent']:.1f}%")
        print(f"   CPU cores: {resources['cpu_count']}")
        print(f"   Disk free: {resources['disk_free_gb']:.1f}GB")
    
    # Test model loading if service is running
    if service_status['running'] and models:
        print(f"\n4. Testing model loading...")
        test_model = models[0]  # Test first model
        result = test_model_loading(test_model)
        print(f"   {result['message']}")
        
        if result['success'] and result['load_time'] > 30:
            print(f"   ⚠️ Model took {result['load_time']:.1f}s to load (normal for first load)")
    
    # Provide suggestions
    print("\n5. Recommendations:")
    suggestions = suggest_solutions(service_status, models, resources)
    for suggestion in suggestions:
        print(f"   {suggestion}")
    
    # Final assessment
    print("\n" + "=" * 50)
    if service_status['running'] and models:
        if 'memory_available_gb' in resources and resources['memory_available_gb'] > 4:
            print("✅ DIAGNOSIS: Ollama should work normally")
            print("   If you're still getting timeouts, try:")
            print("   • Wait for first model load (1-2 minutes)")
            print("   • Use smaller models (llama3.2)")
            print("   • Increase timeout settings")
        else:
            print("⚠️ DIAGNOSIS: Ollama may work but with performance issues")
            print("   Consider upgrading system resources")
    else:
        print("❌ DIAGNOSIS: Ollama setup needs attention")
        print("   Follow the recommendations above")

def quick_fix():
    """Quick fix for common Ollama issues"""
    print("🚀 OLLAMA QUICK FIX")
    print("=" * 30)
    
    # Check if Ollama is running
    service_status = check_ollama_service()
    
    if not service_status['running']:
        print("❌ Ollama not running")
        print("💡 Quick fix: Start Ollama")
        
        try:
            # Try to start Ollama (this may vary by system)
            print("   Attempting to start Ollama...")
            subprocess.run(["ollama", "serve"], check=False, timeout=5)
        except:
            print("   Manual start required:")
            print("   • Run: ollama serve")
            print("   • Or start Ollama application")
        return
    
    # Check models
    models = get_installed_models()
    if not models:
        print("❌ No models installed")
        print("💡 Quick fix: Install a fast model")
        print("   Run: ollama pull llama3.2")
        return
    
    print("✅ Ollama appears to be set up correctly")
    print(f"   Service: Running")
    print(f"   Models: {len(models)} installed")
    print("   If you're still having issues, run full diagnosis")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        quick_fix()
    else:
        run_comprehensive_diagnosis()