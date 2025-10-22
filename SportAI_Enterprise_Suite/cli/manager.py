#!/usr/bin/env python3
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
