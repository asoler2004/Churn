#!/usr/bin/env python3
"""
Standalone script to run the Streamlit Churn Prediction Dashboard
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit dashboard"""
    print("🚀 Starting Streamlit Churn Prediction Dashboard")
    print("=" * 50)
    
    # Check if model files exist
    if not os.path.exists('Modelos/churn_model.pkl'):
        print("❌ Model files not found!")
        print("Please run: python train_model.py")
        print("Also make sure the APIs are running:")
        print("  - python api.py (port 8000)")
        print("  - python llm_api.py (port 8001)")
        return
    
    try:
        # Run Streamlit
        print("🎨 Starting Streamlit dashboard...")
        print("📊 Dashboard will be available at: http://localhost:8501")
        print("\nNote: Make sure the following APIs are running:")
        print("  - Churn Prediction API: http://localhost:8000")
        print("  - LLM Insights API: http://localhost:8001")
        print("\nPress Ctrl+C to stop the dashboard")
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_ui.py",
            "--server.port=8501",
            "--server.headless=false"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping Streamlit dashboard...")
    except Exception as e:
        print(f"❌ Error running Streamlit: {e}")

if __name__ == "__main__":
    main()