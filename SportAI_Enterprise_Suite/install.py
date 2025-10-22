#!/usr/bin/env python3
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
