#!/usr/bin/env python3
"""SportAI Enterprise Suite - Main Runner"""

import subprocess
import sys
import time
import threading
import webbrowser

def start_fastapi():
    """Start FastAPI server"""
    subprocess.run([sys.executable, "main.py"])

def start_streamlit():
    """Start Streamlit dashboard"""
    time.sleep(3)
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port", "8501"])

def main():
    print("🏟️ SportAI Enterprise Suite - Starting Services")
    print("=" * 45)
    
    # Start FastAPI in background
    fastapi_thread = threading.Thread(target=start_fastapi, daemon=True)
    fastapi_thread.start()
    
    # Start Streamlit in background
    streamlit_thread = threading.Thread(target=start_streamlit, daemon=True)
    streamlit_thread.start()
    
    time.sleep(5)
    
    print("✅ Services started!")
    print()
    print("🌐 Access URLs:")
    print("   • Main App:  http://localhost:8000")
    print("   • Dashboard: http://localhost:8501")
    print("   • API Docs:  http://localhost:8000/docs")
    print()
    print("🔐 Login: admin@sportai.com / admin123")
    print()
    print("Press Ctrl+C to stop")
    
    try:
        webbrowser.open("http://localhost:8000")
    except:
        pass
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down SportAI Enterprise Suite")

if __name__ == "__main__":
    main()
