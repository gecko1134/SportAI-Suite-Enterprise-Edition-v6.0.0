#!/usr/bin/env python3
"""SportAI Enterprise Suite - FastAPI Application"""

import sqlite3
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict

try:
    from fastapi import FastAPI, HTTPException, Depends, Form, UploadFile, File
    from fastapi.responses import HTMLResponse, FileResponse
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    import uvicorn
    import pandas as pd
except ImportError:
    print("Installing required packages...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn[standard]", "pandas"])
    from fastapi import FastAPI, HTTPException, Depends, Form, UploadFile, File
    from fastapi.responses import HTMLResponse, FileResponse
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    import uvicorn
    import pandas as pd

# Ensure directories exist
for directory in ["data", "logs", "uploads", "exports"]:
    Path(directory).mkdir(exist_ok=True)

app = FastAPI(
    title="SportAI Enterprise Suite",
    description="Complete Sports Facility Management Platform",
    version="6.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify authentication token"""
    if credentials.credentials == "demo-token":
        return {"email": "admin@sportai.com", "role": "admin", "id": 1}
    raise HTTPException(status_code=401, detail="Invalid authentication")

def get_db_data(table: str) -> List[Dict]:
    """Get data from database table"""
    try:
        conn = sqlite3.connect("data/sportai.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(f"SELECT * FROM {table}")
        result = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return result
    except Exception as e:
        print(f"Database error: {e}")
        return []

@app.get("/", response_class=HTMLResponse)
def root():
    """Main application interface"""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>SportAI Enterprise Suite</title>
    <style>
        body { font-family: Arial; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .container { max-width: 800px; margin: 0 auto; padding: 50px 20px; text-align: center; }
        .card { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 20px 50px rgba(0,0,0,0.2); }
        .logo { font-size: 4em; margin-bottom: 20px; }
        .title { font-size: 2.5em; color: #333; margin-bottom: 10px; }
        .subtitle { color: #666; font-size: 1.2em; margin-bottom: 30px; }
        .btn { display: inline-block; padding: 15px 30px; margin: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-decoration: none; border-radius: 10px; font-weight: bold; }
        .btn:hover { transform: translateY(-2px); }
        .features { text-align: left; margin: 30px 0; }
        .feature { margin: 10px 0; color: #555; }
        .credentials { background: #f8f9fa; padding: 20px; border-radius: 10px; margin-top: 30px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="logo">🏟️</div>
            <h1 class="title">SportAI Enterprise Suite</h1>
            <p class="subtitle">Complete Sports Facility Management Platform</p>
            
            <div class="features">
                <div class="feature">✅ Facility & Equipment Management</div>
                <div class="feature">✅ Member & Sponsor Relations</div>
                <div class="feature">✅ Event & Booking System</div>
                <div class="feature">✅ AI-Powered Analytics</div>
                <div class="feature">✅ Financial Reporting</div>
            </div>
            
            <a href="http://localhost:8501" class="btn">Open Dashboard</a>
            <a href="/docs" class="btn">API Documentation</a>
            
            <div class="credentials">
                <strong>Login Credentials:</strong><br>
                Email: admin@sportai.com<br>
                Password: admin123
            </div>
        </div>
    </div>
    
    <script>
        setTimeout(() => {
            fetch('http://localhost:8501')
                .then(() => window.location.href = 'http://localhost:8501')
                .catch(() => console.log('Streamlit not ready'));
        }, 3000);
    </script>
</body>
</html>
    """

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "6.0.0", "timestamp": datetime.now().isoformat()}

@app.post("/api/auth/login")
def login(email: str = Form(), password: str = Form()):
    """User authentication"""
    try:
        conn = sqlite3.connect("data/sportai.db")
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor = conn.execute("SELECT * FROM users WHERE email=? AND password_hash=?", (email, password_hash))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                "user": {"id": user[0], "email": user[1], "role": user[3], "full_name": user[4]},
                "access_token": "demo-token",
                "token_type": "bearer"
            }
        raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/facilities")
def get_facilities(current_user: dict = Depends(verify_token)):
    """Get all facilities"""
    return get_db_data("facilities")

@app.get("/api/equipment")
def get_equipment(current_user: dict = Depends(verify_token)):
    """Get all equipment"""
    return get_db_data("equipment")

@app.get("/api/members")
def get_members(current_user: dict = Depends(verify_token)):
    """Get all members"""
    return get_db_data("members")

@app.get("/api/sponsors")
def get_sponsors(current_user: dict = Depends(verify_token)):
    """Get all sponsors"""
    return get_db_data("sponsors")

@app.get("/api/events")
def get_events(current_user: dict = Depends(verify_token)):
    """Get all events"""
    return get_db_data("events")

@app.get("/api/analytics/dashboard")
def get_dashboard_data(current_user: dict = Depends(verify_token)):
    """Get dashboard analytics"""
    facilities = get_db_data("facilities")
    members = get_db_data("members")
    equipment = get_db_data("equipment")
    sponsors = get_db_data("sponsors")
    events = get_db_data("events")
    
    return {
        "summary": {
            "total_revenue": sum(f.get('revenue', 0) for f in facilities),
            "active_facilities": len([f for f in facilities if f.get('status') == 'active']),
            "total_members": len(members),
            "active_members": len([m for m in members if m.get('status') == 'active']),
            "total_equipment": sum(e.get('available', 0) + e.get('rented', 0) for e in equipment),
            "sponsor_value": sum(s.get('annual_value', 0) for s in sponsors),
            "upcoming_events": len([e for e in events if e.get('status') == 'active']),
            "avg_utilization": sum(f.get('utilization', 0) for f in facilities) / len(facilities) if facilities else 0
        }
    }

@app.get("/api/analytics/insights")
def get_insights(current_user: dict = Depends(verify_token)):
    """Get AI insights"""
    facilities = get_db_data("facilities")
    avg_util = sum(f.get('utilization', 0) for f in facilities) / len(facilities) if facilities else 0
    
    insights = []
    if avg_util > 85:
        insights.append({
            "type": "optimization",
            "priority": "high",
            "title": "High Facility Utilization",
            "description": f"Average utilization at {avg_util:.1f}%. Consider dynamic pricing.",
            "impact": "Revenue opportunity: $15K-25K/month"
        })
    elif avg_util < 60:
        insights.append({
            "type": "opportunity", 
            "priority": "medium",
            "title": "Underutilized Facilities",
            "description": f"Average utilization only {avg_util:.1f}%. Marketing could help.",
            "impact": "Revenue opportunity: $8K-15K/month"
        })
    
    return insights

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...), current_user: dict = Depends(verify_token)):
    """Upload data file"""
    try:
        content = await file.read()
        file_path = f"uploads/{file.filename}"
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            df = pd.read_excel(file_path)
        
        return {
            "message": "File uploaded successfully",
            "filename": file.filename,
            "rows": len(df),
            "columns": list(df.columns)
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/export/{data_type}")
def export_data(data_type: str, current_user: dict = Depends(verify_token)):
    """Export data to Excel"""
    try:
        data = get_db_data(data_type)
        df = pd.DataFrame(data)
        filename = f"{data_type}_export.xlsx"
        export_path = f"exports/{filename}"
        df.to_excel(export_path, index=False)
        
        return FileResponse(
            export_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🏟️ SportAI Enterprise Suite - Starting FastAPI Server")
    print("🌐 Main App: http://localhost:8000")
    print("📊 API Docs: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
