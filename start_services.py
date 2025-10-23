import subprocess
import time
import sys
import os
from threading import Thread
import argparse

def run_service(command, name, port):
    """Run a service in a separate process"""
    print(f"Starting {name} on port {port}...")
    try:
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Monitor the process
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"[{name}] {output.strip()}")
                
    except Exception as e:
        print(f"Error starting {name}: {e}")

def main():
    """Start all services"""
    parser = argparse.ArgumentParser(description='Start Fintech Churn Prediction System')
    parser.add_argument('--ui', choices=['taipy', 'streamlit'], default='taipy',
                       help='Choose UI framework (default: taipy)')
    args = parser.parse_args()
    
    print("🚀 Starting Fintech Churn Prediction System")
    print(f"🎨 UI Framework: {args.ui.title()}")
    print("=" * 50)
    
    # Check if model files exist
    if not os.path.exists('churn_model.pkl'):
        print("❌ Model files not found!")
        print("Please run: python train_model.py")
        return
    
    # Define services based on UI choice
    if args.ui == 'streamlit':
        ui_command = "streamlit run streamlit_ui.py --server.port=8501"
        ui_name = "Streamlit Dashboard"
        ui_port = 8501
        ui_url = "http://localhost:8501"
    else:
        ui_command = "python churn_ui.py"
        ui_name = "Taipy Dashboard"
        ui_port = 5000
        ui_url = "http://localhost:5000"
    
    services = [
        ("python api.py", "Churn Prediction API", 8000),
        ("python llm_api.py", "LLM Insights API", 8001),
        (ui_command, ui_name, ui_port)
    ]
    
    threads = []
    
    for command, name, port in services:
        thread = Thread(target=run_service, args=(command, name, port))
        thread.daemon = True
        thread.start()
        threads.append(thread)
        time.sleep(2)  # Stagger startup
    
    print("\n🎉 All services started!")
    print(f"📊 Dashboard: {ui_url}")
    print("🤖 Churn API: http://localhost:8000")
    print("💡 LLM API: http://localhost:8001")
    print("\nPress Ctrl+C to stop all services")
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping all services...")
        sys.exit(0)

if __name__ == "__main__":
    main()