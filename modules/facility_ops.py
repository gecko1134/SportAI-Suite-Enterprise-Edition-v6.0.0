"""
SportAI Facility Operations Module
Maintenance, equipment, cleaning, and operations management
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any, List

def run(context: Dict[str, Any]):
    """Main facility operations execution"""

    st.markdown('<div class="main-header">🏢 Facility Operations</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Maintenance, equipment, and operations management</div>', unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Operations Dashboard",
        "🔧 Maintenance",
        "📦 Equipment & Inventory",
        "🧹 Cleaning Schedule"
    ])

    with tab1:
        show_operations_dashboard(context)

    with tab2:
        show_maintenance_management(context)

    with tab3:
        show_equipment_inventory(context)

    with tab4:
        show_cleaning_schedule(context)

def show_operations_dashboard(context: Dict[str, Any]):
    """Operations overview dashboard"""

    st.markdown("### 📊 Operations Overview")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Facility Uptime", "98.7%", "+0.3%")
        st.caption("Target: 95%+")

    with col2:
        st.metric("Open Work Orders", 7, "-3")
        st.caption("Avg resolution: 2.4 days")

    with col3:
        st.metric("Equipment Status", "92%", "+2%")
        st.caption("Operational condition")

    with col4:
        st.metric("Cleaning Score", "96/100", "+2")
        st.caption("Inspection average")

    st.divider()

    # Today's schedule
    st.markdown("### 📅 Today's Operations Schedule")

    today_schedule = [
        {"Time": "6:00 AM", "Task": "Facility Opening", "Assigned": "Operations Staff", "Status": "Complete"},
        {"Time": "7:00 AM", "Task": "Turf Field Inspection", "Assigned": "Maintenance", "Status": "Complete"},
        {"Time": "9:00 AM", "Task": "Equipment Check", "Assigned": "Ops Manager", "Status": "In Progress"},
        {"Time": "2:00 PM", "Task": "HVAC Filter Replacement", "Assigned": "Maintenance", "Status": "Scheduled"},
        {"Time": "6:00 PM", "Task": "Evening Cleaning Round", "Assigned": "Cleaning Crew", "Status": "Scheduled"},
        {"Time": "10:00 PM", "Task": "Facility Closing", "Assigned": "Operations Staff", "Status": "Scheduled"},
    ]

    df_schedule = pd.DataFrame(today_schedule)

    st.dataframe(df_schedule, use_container_width=True, hide_index=True)

    # Active alerts
    st.divider()
    st.markdown("### ⚠️ Active Alerts")

    alerts = [
        {"Priority": "Medium", "Issue": "Court 3 - Net replacement needed", "Reported": "2 hours ago"},
        {"Priority": "Low", "Issue": "Suite B - Light bulb out in bathroom", "Reported": "Yesterday"},
        {"Priority": "High", "Issue": "Golf Bay 2 - Projector calibration required", "Reported": "30 min ago"},
    ]

    for alert in alerts:
        priority_color = "#ef4444" if alert['Priority'] == "High" else "#f59e0b" if alert['Priority'] == "Medium" else "#10b981"
        st.markdown(f"""
        <div style="background: #f9fafb; padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem; border-left: 4px solid {priority_color};">
        <strong>{alert['Issue']}</strong><br>
        Priority: {alert['Priority']} | Reported: {alert['Reported']}
        </div>
        """, unsafe_allow_html=True)

def show_maintenance_management(context: Dict[str, Any]):
    """Maintenance tracking and work orders"""

    st.markdown("### 🔧 Maintenance Management")

    # Work order summary
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Open Work Orders", 7)

    with col2:
        st.metric("In Progress", 3)

    with col3:
        st.metric("Completed (30d)", 42)

    with col4:
        st.metric("Avg Resolution Time", "2.4 days", "-0.3 days")

    st.divider()

    # Work orders list
    st.markdown("#### 📋 Active Work Orders")

    work_orders = [
        {"WO#": "WO-1234", "Priority": "High", "Asset": "Golf Bay 2", "Issue": "Projector calibration", "Assigned": "Tech Team", "Status": "In Progress", "Days Open": 0},
        {"WO#": "WO-1233", "Priority": "Medium", "Asset": "Court 3", "Issue": "Net replacement", "Assigned": "Maintenance", "Status": "Parts Ordered", "Days Open": 1},
        {"WO#": "WO-1232", "Priority": "Low", "Asset": "Suite B", "Issue": "Light bulb replacement", "Assigned": "Maintenance", "Status": "Scheduled", "Days Open": 1},
        {"WO#": "WO-1231", "Priority": "Medium", "Asset": "HVAC Unit 2", "Issue": "Filter replacement", "Assigned": "HVAC Tech", "Status": "In Progress", "Days Open": 0},
        {"WO#": "WO-1230", "Priority": "High", "Asset": "Turf Field", "Issue": "Drainage inspection", "Assigned": "Maintenance", "Status": "In Progress", "Days Open": 2},
    ]

    df_wo = pd.DataFrame(work_orders)

    st.dataframe(df_wo, use_container_width=True, hide_index=True)

    # Create new work order
    st.divider()
    st.markdown("#### ➕ Create Work Order")

    col1, col2, col3 = st.columns(3)

    with col1:
        wo_asset = st.selectbox("Asset/Location", [
            "Turf Field", "Court 1", "Court 2", "Court 3", "Court 4",
            "Golf Bay 1", "Golf Bay 2", "Suite A", "Suite B",
            "HVAC System", "Lighting", "Plumbing", "Electrical", "Other"
        ])
        wo_priority = st.selectbox("Priority", ["High", "Medium", "Low"])

    with col2:
        wo_category = st.selectbox("Category", [
            "Repair", "Preventive Maintenance", "Inspection",
            "Cleaning", "Replacement", "Upgrade"
        ])
        wo_assigned = st.selectbox("Assign To", [
            "Maintenance Team", "HVAC Tech", "Electrical",
            "Plumbing", "Tech Team", "Cleaning Crew"
        ])

    with col3:
        wo_description = st.text_area("Description")
        wo_due_date = st.date_input("Due Date", datetime.now() + timedelta(days=3))

    if st.button("📝 Create Work Order", type="primary"):
        st.success(f"✅ Work order created for {wo_asset}")
        context['audit_log']('work_order_created', {
            'asset': wo_asset,
            'priority': wo_priority,
            'category': wo_category
        })

    # Preventive maintenance schedule
    st.divider()
    st.markdown("#### 🗓️ Preventive Maintenance Schedule")

    pm_schedule = [
        {"Task": "HVAC Filter Replacement", "Frequency": "Monthly", "Last Done": "2024-09-15", "Next Due": "2024-10-15", "Status": "Due Soon"},
        {"Task": "Turf Field Grooming", "Frequency": "Weekly", "Last Done": "2024-10-18", "Next Due": "2024-10-25", "Status": "Upcoming"},
        {"Task": "Fire Extinguisher Inspection", "Frequency": "Monthly", "Last Done": "2024-10-01", "Next Due": "2024-11-01", "Status": "On Track"},
        {"Task": "Emergency Lighting Test", "Frequency": "Quarterly", "Last Done": "2024-07-15", "Next Due": "2024-10-15", "Status": "Overdue"},
        {"Task": "Golf Simulator Calibration", "Frequency": "Bi-Weekly", "Last Done": "2024-10-10", "Next Due": "2024-10-24", "Status": "Upcoming"},
    ]

    df_pm = pd.DataFrame(pm_schedule)
    st.dataframe(df_pm, use_container_width=True, hide_index=True)

def show_equipment_inventory(context: Dict[str, Any]):
    """Equipment and inventory management"""

    st.markdown("### 📦 Equipment & Inventory")

    # Inventory summary
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Equipment Items", 487)

    with col2:
        st.metric("Needs Replacement", 12)

    with col3:
        st.metric("Low Stock Items", 5)

    with col4:
        st.metric("Inventory Value", "$128,500")

    st.divider()

    # Equipment categories
    st.markdown("#### 🏆 Equipment by Category")

    categories = {
        "Sports Equipment": {
            "items": [
                {"Item": "Soccer Balls", "Quantity": 45, "Condition": "Good", "Location": "Storage A"},
                {"Item": "Basketballs", "Quantity": 38, "Condition": "Good", "Location": "Storage A"},
                {"Item": "Court Nets", "Quantity": 12, "Condition": "Fair", "Location": "Storage B"},
                {"Item": "Training Cones", "Quantity": 120, "Condition": "Good", "Location": "Storage A"},
            ]
        },
        "Golf Simulators": {
            "items": [
                {"Item": "Projector - Bay 1", "Quantity": 1, "Condition": "Excellent", "Location": "Golf Bay 1"},
                {"Item": "Projector - Bay 2", "Quantity": 1, "Condition": "Needs Service", "Location": "Golf Bay 2"},
                {"Item": "Launch Monitor - Bay 1", "Quantity": 1, "Condition": "Good", "Location": "Golf Bay 1"},
                {"Item": "Launch Monitor - Bay 2", "Quantity": 1, "Condition": "Good", "Location": "Golf Bay 2"},
            ]
        },
        "Facility Equipment": {
            "items": [
                {"Item": "Cleaning Supplies", "Quantity": 1, "Condition": "Stock: Low", "Location": "Janitor Closet"},
                {"Item": "HVAC Filters", "Quantity": 24, "Condition": "Good", "Location": "Mechanical Room"},
                {"Item": "LED Light Bulbs", "Quantity": 156, "Condition": "Good", "Location": "Storage C"},
                {"Item": "First Aid Kits", "Quantity": 8, "Condition": "Good", "Location": "Various"},
            ]
        }
    }

    for category, data in categories.items():
        with st.expander(f"📁 {category}"):
            df = pd.DataFrame(data['items'])
            st.dataframe(df, use_container_width=True, hide_index=True)

    # Add inventory item
    st.divider()
    st.markdown("#### ➕ Add Inventory Item")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        item_name = st.text_input("Item Name")

    with col2:
        item_quantity = st.number_input("Quantity", min_value=1, value=1)

    with col3:
        item_condition = st.selectbox("Condition", ["Excellent", "Good", "Fair", "Poor", "Needs Replacement"])

    with col4:
        item_location = st.text_input("Location")

    if st.button("💾 Add Item"):
        st.success(f"✅ '{item_name}' added to inventory")
        context['audit_log']('inventory_added', {'item': item_name, 'quantity': item_quantity})

def show_cleaning_schedule(context: Dict[str, Any]):
    """Cleaning schedule and quality tracking"""

    st.markdown("### 🧹 Cleaning Schedule")

    # Cleaning metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Overall Cleanliness", "96/100", "+2")

    with col2:
        st.metric("Tasks Completed Today", "12/15")

    with col3:
        st.metric("Last Inspection", "Yesterday", "Score: 98")

    with col4:
        st.metric("Staff On Duty", "3/3")

    st.divider()

    # Daily cleaning schedule
    st.markdown("#### 📋 Daily Cleaning Schedule")

    cleaning_schedule = [
        {"Time": "6:00 AM", "Area": "All Restrooms", "Task": "Deep Clean", "Assigned": "Team A", "Status": "Complete"},
        {"Time": "7:00 AM", "Area": "Lobby & Entrance", "Task": "Sweep, Mop, Dust", "Assigned": "Team B", "Status": "Complete"},
        {"Time": "9:00 AM", "Area": "Turf Field", "Task": "Debris Removal", "Assigned": "Team A", "Status": "Complete"},
        {"Time": "12:00 PM", "Area": "All Restrooms", "Task": "Check & Restock", "Assigned": "Team C", "Status": "Complete"},
        {"Time": "2:00 PM", "Area": "Courts", "Task": "Sweep & Sanitize", "Assigned": "Team B", "Status": "In Progress"},
        {"Time": "4:00 PM", "Area": "Golf Bays", "Task": "Vacuum & Clean Screens", "Assigned": "Team A", "Status": "Pending"},
        {"Time": "6:00 PM", "Area": "Suites", "Task": "Full Clean & Setup", "Assigned": "Team C", "Status": "Pending"},
        {"Time": "8:00 PM", "Area": "All Restrooms", "Task": "Evening Check", "Assigned": "Team B", "Status": "Pending"},
        {"Time": "10:00 PM", "Area": "Entire Facility", "Task": "Final Walk-through", "Assigned": "Supervisor", "Status": "Pending"},
    ]

    df_cleaning = pd.DataFrame(cleaning_schedule)
    st.dataframe(df_cleaning, use_container_width=True, hide_index=True)

    # Inspection log
    st.divider()
    st.markdown("#### ✅ Recent Inspections")

    inspections = [
        {"Date": "2024-10-21", "Inspector": "Operations Manager", "Score": 98, "Notes": "Excellent condition throughout"},
        {"Date": "2024-10-20", "Inspector": "Health Inspector", "Score": 96, "Notes": "Minor issue in storage area - resolved"},
        {"Date": "2024-10-19", "Inspector": "Operations Manager", "Score": 97, "Notes": "All areas meeting standards"},
    ]

    df_inspections = pd.DataFrame(inspections)

    st.dataframe(
        df_inspections,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Score",
                format="%d/100",
                min_value=0,
                max_value=100
            )
        }
    )

    # Quick actions
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📝 Log New Inspection", use_container_width=True):
            st.info("Inspection form opened...")

    with col2:
        if st.button("📊 Cleaning Report", use_container_width=True):
            st.success("Generating cleaning performance report...")

    with col3:
        if st.button("⚠️ Report Issue", use_container_width=True):
            st.info("Opening issue report form...")

# Helper functions would go here
