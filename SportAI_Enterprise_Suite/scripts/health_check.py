#!/usr/bin/env python3
"""SportAI Health Check Script"""

import requests
import time
from datetime import datetime

def check_health():
    """Check application health"""
    print(f"🏥 SportAI Health Check - {datetime.now().isoformat()}")
    print("=" * 40)
    
    services = {
        "FastAPI": "http://localhost:8000/health",
        "Streamlit": "http://localhost:8501"
    }
    
    all_healthy = True
    
    for service, url in services.items():
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                print(f"✅ {service}: Healthy ({response_time:.0f}ms)")
            else:
                print(f"❌ {service}: Unhealthy (HTTP {response.status_code})")
                all_healthy = False
        except Exception as e:
            print(f"❌ {service}: Unreachable ({str(e)})")
            all_healthy = False
    
    return 0 if all_healthy else 1

if __name__ == "__main__":
    exit(check_health())
