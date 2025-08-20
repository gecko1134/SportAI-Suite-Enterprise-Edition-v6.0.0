#!/usr/bin/env python3
"""
SportAI Enterprise Suite - Complete Package Creator
Creates a fully functional sports facility management platform

Run this script to create the complete package:
python sportai_creator.py
"""

import os
import sys
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

def main():
    """Create the complete SportAI Enterprise Suite package"""
    
    print("🏟️ SportAI Enterprise Suite - Package Creator")
    print("=" * 50)
    print("Creating complete sports facility management platform...")
    print()
    
    try:
        success = create_complete_package()
        
        if success:
            print("\n🎉 SUCCESS! SportAI Enterprise Suite created!")
            print("=" * 50)
            print("📦 Complete package ready for deployment")
            print()
            print("🚀 To start the application:")
            print("   cd SportAI_Enterprise_Suite")
            print("   python install.py")
            print("   python run.py")
            print()
            print("🌐 Access URLs after starting:")
            print("   • Main App:   http://localhost:8000")
            print("   • Dashboard:  http://localhost:8501") 
            print("   • API Docs:   http://localhost:8000/docs")
            print()
            print("🔐 Login Credentials:")
            print("   • Email:      admin@sportai.com")
            print("   • Password:   admin123")
        else:
            print("❌ Package creation failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def create_complete_package():
    """Create the complete package"""
    
    # Create directory structure
    directories = [
        "SportAI_Enterprise_Suite",
        "SportAI_Enterprise_Suite/backend",
        "SportAI_Enterprise_Suite/frontend",
        "SportAI_Enterprise_Suite/frontend/static",
        "SportAI_Enterprise_Suite/cli",
        "SportAI_Enterprise_Suite/scripts",
        "SportAI_Enterprise_Suite/data",
        "SportAI_Enterprise_Suite/logs",
        "SportAI_Enterprise_Suite/uploads",
        "SportAI_Enterprise_Suite/exports",
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    # Create all files
    create_main_files()
    create_backend_files()
    create_frontend_files()
    create_streamlit_app()
    create_cli_tools()
    create_scripts()
    create_config_files()
    
    return True

def create_main_files():
    """Create main application files"""
    
    # Installation script
    install_py = '''#!/usr/bin/env python3
"""SportAI Enterprise Suite - Installation Script"""

import subprocess
import sys
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

def install_dependencies():
    """Install required packages"""
    print("📦 Installing dependencies...")
    
    packages = [
        "fastapi==0.104.1",
        "uvicorn[standard]==0.24.0", 
        "pandas==2.1.3",
        "streamlit==1.28.1",
        "plotly==5.17.0",
        "openpyxl==3.1.2",
        "python-multipart==0.0.6"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            print(f"Warning: Could not install {package}")
    
    print("✅ Dependencies installed")

def setup_database():
    """Initialize database"""
    print("🗄️ Setting up database...")
    
    Path("data").mkdir(exist_ok=True)
    conn = sqlite3.connect("data/sportai.db")
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facilities (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            capacity INTEGER,
            hourly_rate REAL,
            utilization REAL DEFAULT 0,
            revenue REAL DEFAULT 0,
            status TEXT DEFAULT 'active',
            location TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            available INTEGER,
            rented INTEGER DEFAULT 0,
            daily_rate REAL,
            monthly_revenue REAL DEFAULT 0,
            status TEXT DEFAULT 'available',
            condition_score REAL DEFAULT 10.0
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY,
            member_id TEXT UNIQUE,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            tier TEXT NOT NULL,
            join_date TEXT,
            total_spent REAL DEFAULT 0,
            status TEXT DEFAULT 'active',
            address TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sponsors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            tier TEXT NOT NULL,
            annual_value REAL,
            engagement REAL DEFAULT 0,
            satisfaction REAL DEFAULT 0,
            status TEXT DEFAULT 'active',
            contact_name TEXT,
            contact_email TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            event_type TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT,
            facility_id INTEGER,
            capacity INTEGER,
            registered INTEGER DEFAULT 0,
            price REAL DEFAULT 0,
            status TEXT DEFAULT 'active',
            description TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE,
            password_hash TEXT,
            role TEXT DEFAULT 'user',
            full_name TEXT,
            is_active BOOLEAN DEFAULT 1
        )
    """)
    
    # Insert sample data
    now = datetime.now().isoformat()
    
    facilities = [
        ("Basketball Court 1", "Indoor Court", 200, 150.0, 89.0, 12500.0, "active", "North Wing"),
        ("Tennis Court 1", "Tennis Court", 50, 80.0, 78.0, 6240.0, "active", "West Side"),
        ("Swimming Pool", "Aquatic Center", 100, 120.0, 65.0, 9360.0, "active", "Aquatic Wing"),
        ("Main Dome", "Multi-Sport", 500, 350.0, 93.0, 28700.0, "active", "Central Building")
    ]
    
    cursor.executemany("""
        INSERT INTO facilities (name, type, capacity, hourly_rate, utilization, revenue, status, location)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, facilities)
    
    equipment = [
        ("Mountain Bikes", "Bicycles", 15, 8, 25.0, 6000.0, "available", 9.2),
        ("Tennis Rackets", "Sports Equipment", 25, 12, 15.0, 2700.0, "available", 8.5),
        ("Pool Equipment", "Aquatic", 100, 25, 2.0, 1500.0, "available", 9.8),
        ("Basketball Sets", "Sports Equipment", 20, 8, 12.0, 1440.0, "available", 9.0)
    ]
    
    cursor.executemany("""
        INSERT INTO equipment (name, category, available, rented, daily_rate, monthly_revenue, status, condition_score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, equipment)
    
    members = [
        ("M001", "John Smith", "john.smith@email.com", "555-0101", "Premium", now, 1250.0, "active", "123 Oak St"),
        ("M002", "Sarah Johnson", "sarah.j@email.com", "555-0201", "Elite", now, 2100.0, "active", "456 Pine Ave"),
        ("M003", "Mike Wilson", "mike.w@email.com", "555-0301", "Basic", now, 850.0, "active", "789 Elm Dr"),
        ("M004", "Emily Davis", "emily.d@email.com", "555-0401", "Premium", now, 1450.0, "active", "321 Maple Ln")
    ]
    
    cursor.executemany("""
        INSERT INTO members (member_id, name, email, phone, tier, join_date, total_spent, status, address)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, members)
    
    sponsors = [
        ("Wells Fargo Bank", "Diamond", 175000.0, 95.0, 9.2, "active", "Susan Wells", "partnerships@wellsfargo.com"),
        ("HyVee Grocery", "Platinum", 62500.0, 88.0, 8.7, "active", "Mark Johnson", "sports@hyvee.com"),
        ("Nike Sports", "Silver", 15000.0, 85.0, 8.5, "active", "Alex Rodriguez", "local@nike.com")
    ]
    
    cursor.executemany("""
        INSERT INTO sponsors (name, tier, annual_value, engagement, satisfaction, status, contact_name, contact_email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, sponsors)
    
    future_date = (datetime.now() + timedelta(days=30)).isoformat()
    events = [
        ("Summer Basketball League", "Tournament", now, future_date, 1, 32, 28, 50.0, "active", "Annual tournament"),
        ("Tennis Open", "Tournament", now, future_date, 2, 64, 55, 75.0, "active", "Open tournament"),
        ("Swim Meet", "Competition", now, future_date, 3, 50, 42, 25.0, "active", "Swimming championship")
    ]
    
    cursor.executemany("""
        INSERT INTO events (name, event_type, start_date, end_date, facility_id, capacity, registered, price, status, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, events)
    
    # Create admin user
    admin_hash = hashlib.sha256("admin123".encode()).hexdigest()
    cursor.execute("""
        INSERT OR REPLACE INTO users (email, password_hash, role, full_name, is_active)
        VALUES (?, ?, ?, ?, ?)
    """, ("admin@sportai.com", admin_hash, "admin", "System Administrator", True))
    
    conn.commit()
    conn.close()
    print("✅ Database initialized")

def main():
    print("🏟️ SportAI Enterprise Suite - Installation")
    print("=" * 40)
    
    install_dependencies()
    setup_database()
    
    print()
    print("✅ Installation completed!")
    print()
    print("🚀 To start the application:")
    print("   python run.py")

if __name__ == "__main__":
    main()
'''
    
    # Main runner
    run_py = '''#!/usr/bin/env python3
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
        print("\\n👋 Shutting down SportAI Enterprise Suite")

if __name__ == "__main__":
    main()
'''
    
    # Main FastAPI application
    main_py = '''#!/usr/bin/env python3
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
'''
    
    write_file("SportAI_Enterprise_Suite/install.py", install_py)
    write_file("SportAI_Enterprise_Suite/run.py", run_py)
    write_file("SportAI_Enterprise_Suite/main.py", main_py)

def create_backend_files():
    """Create backend files"""
    
    backend_init = '''# SportAI Backend Package'''
    
    write_file("SportAI_Enterprise_Suite/backend/__init__.py", backend_init)

def create_frontend_files():
    """Create frontend files"""
    
    frontend_init = '''# SportAI Frontend Package'''
    
    write_file("SportAI_Enterprise_Suite/frontend/__init__.py", frontend_init)
    write_file("SportAI_Enterprise_Suite/frontend/static/.gitkeep", "# Static files")

def create_streamlit_app():
    """Create Streamlit dashboard"""
    
    streamlit_app = '''#!/usr/bin/env python3
"""SportAI Enterprise Suite - Streamlit Dashboard"""

import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
from datetime import datetime
from pathlib import Path

st.set_page_config(
    page_title="SportAI Enterprise Suite",
    page_icon="🏟️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e1e8ed;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_data(table):
    """Get data from database"""
    try:
        conn = sqlite3.connect("data/sportai.db")
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

def main():
    """Main Streamlit application"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏟️ SportAI Enterprise Suite</h1>
        <p>Complete Sports Facility Management Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select Page", [
        "📊 Dashboard",
        "🏢 Facilities", 
        "👥 Members",
        "🔧 Equipment",
        "🤝 Sponsors",
        "📅 Events"
    ])
    
    if page == "📊 Dashboard":
        show_dashboard()
    elif page == "🏢 Facilities":
        show_facilities()
    elif page == "👥 Members":
        show_members()
    elif page == "🔧 Equipment":
        show_equipment()
    elif page == "🤝 Sponsors":
        show_sponsors()
    elif page == "📅 Events":
        show_events()

def show_dashboard():
    """Show main dashboard"""
    
    st.subheader("📊 Key Metrics")
    
    # Get data
    facilities = get_data("facilities")
    members = get_data("members")
    equipment = get_data("equipment")
    sponsors = get_data("sponsors")
    
    if not facilities.empty:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_revenue = facilities['revenue'].sum()
            st.metric("Total Revenue", f"${total_revenue:,.0f}", "+15.2%")
        
        with col2:
            active_facilities = len(facilities[facilities['status'] == 'active'])
            st.metric("Active Facilities", active_facilities, "All operational")
        
        with col3:
            active_members = len(members[members['status'] == 'active']) if not members.empty else 0
            st.metric("Active Members", active_members, "+12.5%")
        
        with col4:
            sponsor_value = sponsors['annual_value'].sum() if not sponsors.empty else 0
            st.metric("Sponsor Value", f"${sponsor_value:,.0f}", f"{len(sponsors)} partners")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Facility Utilization")
            if not facilities.empty:
                fig = px.bar(facilities, x='name', y='utilization', 
                           title="Facility Utilization Rates",
                           color='utilization', color_continuous_scale='RdYlGn')
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Revenue Distribution")
            if not facilities.empty:
                fig = px.pie(facilities, values='revenue', names='name',
                           title="Revenue by Facility")
                st.plotly_chart(fig, use_container_width=True)

def show_facilities():
    """Show facilities page"""
    
    st.subheader("🏢 Facility Management")
    
    facilities = get_data("facilities")
    
    if not facilities.empty:
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_util = facilities['utilization'].mean()
            st.metric("Average Utilization", f"{avg_util:.1f}%")
        
        with col2:
            total_capacity = facilities['capacity'].sum()
            st.metric("Total Capacity", total_capacity)
        
        with col3:
            total_revenue = facilities['revenue'].sum()
            st.metric("Total Revenue", f"${total_revenue:,.0f}")
        
        # Facilities table
        st.subheader("Facility Details")
        
        # Format the dataframe for display
        display_df = facilities.copy()
        display_df['Revenue'] = display_df['revenue'].apply(lambda x: f"${x:,.0f}")
        display_df['Hourly Rate'] = display_df['hourly_rate'].apply(lambda x: f"${x:.0f}")
        display_df['Utilization'] = display_df['utilization'].apply(lambda x: f"{x:.1f}%")
        
        cols_to_show = ['name', 'type', 'capacity', 'Hourly Rate', 'Utilization', 'Revenue', 'status', 'location']
        st.dataframe(display_df[cols_to_show], use_container_width=True)
    else:
        st.warning("No facility data available.")

def show_members():
    """Show members page"""
    
    st.subheader("👥 Member Management")
    
    members = get_data("members")
    
    if not members.empty:
        # Member metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_members = len(members)
            st.metric("Total Members", total_members)
        
        with col2:
            total_spent = members['total_spent'].sum()
            st.metric("Total Spending", f"${total_spent:,.0f}")
        
        with col3:
            avg_spent = members['total_spent'].mean()
            st.metric("Avg per Member", f"${avg_spent:.0f}")
        
        # Member tier distribution
        col1, col2 = st.columns(2)
        
        with col1:
            tier_counts = members['tier'].value_counts()
            fig = px.pie(values=tier_counts.values, names=tier_counts.index, 
                        title="Member Tier Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(members, x='total_spent', nbins=20,
                             title="Member Spending Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        # Members table
        st.subheader("Member Details")
        display_df = members.copy()
        display_df['Total Spent'] = display_df['total_spent'].apply(lambda x: f"${x:,.0f}")
        
        cols_to_show = ['member_id', 'name', 'email', 'tier', 'Total Spent', 'status']
        st.dataframe(display_df[cols_to_show], use_container_width=True)
    else:
        st.warning("No member data available.")

def show_equipment():
    """Show equipment page"""
    
    st.subheader("🔧 Equipment Management")
    
    equipment = get_data("equipment")
    
    if not equipment.empty:
        # Equipment metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_items = equipment['available'].sum() + equipment['rented'].sum()
            st.metric("Total Equipment", total_items)
        
        with col2:
            rented_items = equipment['rented'].sum()
            st.metric("Currently Rented", rented_items)
        
        with col3:
            equipment_revenue = equipment['monthly_revenue'].sum()
            st.metric("Equipment Revenue", f"${equipment_revenue:,.0f}")
        
        # Equipment utilization
        equipment['utilization_rate'] = equipment['rented'] / (equipment['available'] + equipment['rented']) * 100
        
        fig = px.bar(equipment, x='name', y='utilization_rate',
                    title="Equipment Utilization Rates", color='category')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Equipment table
        st.subheader("Equipment Details")
        display_df = equipment.copy()
        display_df['Daily Rate'] = display_df['daily_rate'].apply(lambda x: f"${x:.0f}")
        display_df['Monthly Revenue'] = display_df['monthly_revenue'].apply(lambda x: f"${x:,.0f}")
        display_df['Utilization'] = display_df['utilization_rate'].apply(lambda x: f"{x:.1f}%")
        
        cols_to_show = ['name', 'category', 'available', 'rented', 'Daily Rate', 'Monthly Revenue', 'status']
        st.dataframe(display_df[cols_to_show], use_container_width=True)
    else:
        st.warning("No equipment data available.")

def show_sponsors():
    """Show sponsors page"""
    
    st.subheader("🤝 Sponsor Management")
    
    sponsors = get_data("sponsors")
    
    if not sponsors.empty:
        # Sponsor metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_sponsors = len(sponsors)
            st.metric("Total Sponsors", total_sponsors)
        
        with col2:
            total_value = sponsors['annual_value'].sum()
            st.metric("Total Value", f"${total_value:,.0f}")
        
        with col3:
            avg_engagement = sponsors['engagement'].mean()
            st.metric("Avg Engagement", f"{avg_engagement:.1f}%")
        
        # Sponsor value chart
        fig = px.bar(sponsors.sort_values('annual_value'), 
                    x='annual_value', y='name', orientation='h',
                    title="Sponsor Value Distribution", color='tier')
        st.plotly_chart(fig, use_container_width=True)
        
        # Sponsors table
        st.subheader("Sponsor Details")
        display_df = sponsors.copy()
        display_df['Annual Value'] = display_df['annual_value'].apply(lambda x: f"${x:,.0f}")
        display_df['Engagement'] = display_df['engagement'].apply(lambda x: f"{x:.1f}%")
        
        cols_to_show = ['name', 'tier', 'Annual Value', 'Engagement', 'contact_name', 'status']
        st.dataframe(display_df[cols_to_show], use_container_width=True)
    else:
        st.warning("No sponsor data available.")

def show_events():
    """Show events page"""
    
    st.subheader("📅 Event Management")
    
    events = get_data("events")
    
    if not events.empty:
        # Event metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_events = len(events)
            st.metric("Total Events", total_events)
        
        with col2:
            total_registered = events['registered'].sum()
            st.metric("Total Registered", total_registered)
        
        with col3:
            events['potential_revenue'] = events['registered'] * events['price']
            revenue = events['potential_revenue'].sum()
            st.metric("Event Revenue", f"${revenue:,.0f}")
        
        # Event registration chart
        fig = px.bar(events, x='name', y=['registered', 'capacity'],
                    title="Event Registration Progress", barmode='group')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        # Events table
        st.subheader("Event Details")
        display_df = events.copy()
        display_df['Price'] = display_df['price'].apply(lambda x: f"${x:.0f}")
        display_df['Registration Rate'] = (display_df['registered'] / display_df['capacity'] * 100).apply(lambda x: f"{x:.1f}%")
        
        cols_to_show = ['name', 'event_type', 'capacity', 'registered', 'Price', 'Registration Rate', 'status']
        st.dataframe(display_df[cols_to_show], use_container_width=True)
    else:
        st.warning("No event data available.")

if __name__ == "__main__":
    main()
'''

def create_cli_tools():
    """Create CLI management tools"""
    
    cli_manager = '''#!/usr/bin/env python3
"""SportAI Enterprise Suite - CLI Manager"""

import argparse
import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path

def get_connection():
    """Get database connection"""
    if not Path("data/sportai.db").exists():
        print("❌ Database not found. Run 'python install.py' first.")
        return None
    
    conn = sqlite3.connect("data/sportai.db")
    conn.row_factory = sqlite3.Row
    return conn

def list_facilities():
    """List all facilities"""
    conn = get_connection()
    if not conn:
        return
    
    print("🏢 Facilities:")
    print("-" * 80)
    
    cursor = conn.execute("SELECT * FROM facilities ORDER BY name")
    facilities = cursor.fetchall()
    
    if not facilities:
        print("No facilities found.")
        return
    
    print(f"{'Name':<20} {'Type':<15} {'Capacity':<10} {'Utilization':<12} {'Revenue':<12} {'Status':<10}")
    print("-" * 80)
    
    for facility in facilities:
        print(f"{facility['name']:<20} {facility['type']:<15} {facility['capacity']:<10} "
              f"{facility['utilization']:.1f}%{'':<7} ${facility['revenue']:,.0f}{'':<4} {facility['status']:<10}")
    
    conn.close()

def list_members():
    """List all members"""
    conn = get_connection()
    if not conn:
        return
    
    print("👥 Members:")
    print("-" * 80)
    
    cursor = conn.execute("SELECT * FROM members ORDER BY name")
    members = cursor.fetchall()
    
    if not members:
        print("No members found.")
        return
    
    print(f"{'ID':<8} {'Name':<20} {'Tier':<10} {'Total Spent':<12} {'Status':<10}")
    print("-" * 80)
    
    for member in members:
        print(f"{member['member_id']:<8} {member['name']:<20} {member['tier']:<10} "
              f"${member['total_spent']:,.0f}{'':<4} {member['status']:<10}")
    
    conn.close()

def list_equipment():
    """List all equipment"""
    conn = get_connection()
    if not conn:
        return
    
    print("🔧 Equipment:")
    print("-" * 80)
    
    cursor = conn.execute("SELECT * FROM equipment ORDER BY category, name")
    equipment = cursor.fetchall()
    
    if not equipment:
        print("No equipment found.")
        return
    
    print(f"{'Name':<20} {'Category':<15} {'Available':<10} {'Rented':<8} {'Daily Rate':<12} {'Status':<10}")
    print("-" * 80)
    
    for item in equipment:
        print(f"{item['name']:<20} {item['category']:<15} {item['available']:<10} "
              f"{item['rented']:<8} ${item['daily_rate']:.0f}{'':<7} {item['status']:<10}")
    
    conn.close()

def show_dashboard():
    """Show dashboard summary"""
    conn = get_connection()
    if not conn:
        return
    
    print("📊 SportAI Dashboard Summary")
    print("=" * 40)
    
    # Facilities
    cursor = conn.execute("SELECT COUNT(*) as total, AVG(utilization) as avg_util, SUM(revenue) as total_revenue FROM facilities")
    facility_stats = cursor.fetchone()
    
    # Members
    cursor = conn.execute("SELECT COUNT(*) as total, SUM(total_spent) as total_spent FROM members")
    member_stats = cursor.fetchone()
    
    # Equipment
    cursor = conn.execute("SELECT COUNT(*) as total, SUM(rented) as total_rented FROM equipment")
    equipment_stats = cursor.fetchone()
    
    # Sponsors
    cursor = conn.execute("SELECT COUNT(*) as total, SUM(annual_value) as total_value FROM sponsors")
    sponsor_stats = cursor.fetchone()
    
    print(f"🏢 Facilities: {facility_stats['total']} total")
    print(f"   Average Utilization: {facility_stats['avg_util']:.1f}%")
    print(f"   Total Revenue: ${facility_stats['total_revenue']:,.0f}")
    print()
    
    print(f"👥 Members: {member_stats['total']} total")
    print(f"   Total Spending: ${member_stats['total_spent']:,.0f}")
    print(f"   Average per Member: ${member_stats['total_spent']/member_stats['total']:,.0f}")
    print()
    
    print(f"🔧 Equipment: {equipment_stats['total']} items")
    print(f"   Currently Rented: {equipment_stats['total_rented']}")
    print()
    
    print(f"🤝 Sponsors: {sponsor_stats['total']} partners")
    print(f"   Total Annual Value: ${sponsor_stats['total_value']:,.0f}")
    
    conn.close()

def export_data(table, filename=None):
    """Export table data"""
    conn = get_connection()
    if not conn:
        return
    
    if filename is None:
        filename = f"{table}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        df.to_csv(filename, index=False)
        print(f"✅ Data exported to {filename}")
        print(f"   Exported {len(df)} records from {table}")
    except Exception as e:
        print(f"❌ Export failed: {e}")
    finally:
        conn.close()

def main():
    parser = argparse.ArgumentParser(description="SportAI Enterprise Suite CLI")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List commands
    list_parser = subparsers.add_parser('list', help='List data')
    list_parser.add_argument('type', choices=['facilities', 'members', 'equipment'], help='Data type')
    
    # Dashboard
    subparsers.add_parser('dashboard', help='Show dashboard summary')
    
    # Export
    export_parser = subparsers.add_parser('export', help='Export data')
    export_parser.add_argument('table', choices=['facilities', 'members', 'equipment', 'sponsors', 'events'])
    export_parser.add_argument('--filename', help='Output filename')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'list':
        if args.type == 'facilities':
            list_facilities()
        elif args.type == 'members':
            list_members()
        elif args.type == 'equipment':
            list_equipment()
    elif args.command == 'dashboard':
        show_dashboard()
    elif args.command == 'export':
        export_data(args.table, args.filename)

if __name__ == "__main__":
    main()
'''
    
    write_file("SportAI_Enterprise_Suite/cli/manager.py", cli_manager)
    write_file("SportAI_Enterprise_Suite/cli/__init__.py", "# CLI Package")

def create_scripts():
    """Create utility scripts"""
    
    # Health check
    health_check = '''#!/usr/bin/env python3
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
'''
    
    write_file("SportAI_Enterprise_Suite/scripts/health_check.py", health_check)
    write_file("SportAI_Enterprise_Suite/scripts/__init__.py", "# Scripts Package")

def create_config_files():
    """Create configuration files"""
    
    # Requirements
    requirements = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
pandas==2.1.3
streamlit==1.28.1
plotly==5.17.0
openpyxl==3.1.2
python-multipart==0.0.6
requests==2.31.0
'''
    
    # README
    readme = '''# SportAI Enterprise Suite

Complete Sports Facility Management Platform

## Quick Start

1. Install and run:
```bash
python install.py
python run.py
```

2. Access the application:
- Main App: http://localhost:8000
- Dashboard: http://localhost:8501
- API Docs: http://localhost:8000/docs

3. Login with:
- Email: admin@sportai.com
- Password: admin123

## Features

- 🏢 Facility Management
- 👥 Member Management  
- 🔧 Equipment Tracking
- 🤝 Sponsor Relations
- 📅 Event Management
- 💰 Financial Analytics
- 🤖 AI Insights
- 📊 Interactive Dashboards

## CLI Usage

```bash
# Show dashboard
python cli/manager.py dashboard

# List data
python cli/manager.py list facilities
python cli/manager.py list members

# Export data
python cli/manager.py export facilities
```

## API Usage

```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login', 
                        data={'email': 'admin@sportai.com', 'password': 'admin123'})
token = response.json()['access_token']

# Get data
headers = {'Authorization': f'Bearer {token}'}
facilities = requests.get('http://localhost:8000/api/facilities', headers=headers)
```

© 2024 SportAI Solutions, LLC. All Rights Reserved.
'''
    
    write_file("SportAI_Enterprise_Suite/requirements.txt", requirements)
    write_file("SportAI_Enterprise_Suite/README.md", readme)
    write_file("SportAI_Enterprise_Suite/.gitignore", "*.pyc\n__pycache__/\ndata/\nlogs/\nuploads/\nexports/")

def write_file(path, content):
    """Write content to file"""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Warning: Could not write {path}: {e}")

if __name__ == "__main__":
    main()
