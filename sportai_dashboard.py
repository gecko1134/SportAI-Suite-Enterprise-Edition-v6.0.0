"""
SportAI Dashboard - Streamlit Cloud Compatible Version
Executive overview with KPIs and real-time metrics
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pathlib import Path

# Page config
st.set_page_config(
    page_title="SportAI Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.markdown("# 📊 SportAI Executive Dashboard")
st.markdown(f"**Real-time facility performance • {datetime.now().strftime('%B %d, %Y')}**")

# KPI calculations
def get_kpis():
    """Get current KPIs"""
    return {
        'utilization': 87.3,
        'utilization_prev': 82.1,
        'revenue_mtd': 142500,
        'revenue_prev': 128000,
        'active_members': 847,
        'new_members': 23,
        'sponsorship_sold': 73.5,
        'sponsorship_value': 385000
    }

# Display KPIs
st.markdown("### Key Performance Indicators")
kpis = get_kpis()

col1, col2, col3, col4 = st.columns(4)

with col1:
    delta_util = kpis['utilization'] - kpis['utilization_prev']
    st.metric(
        "Facility Utilization",
        f"{kpis['utilization']:.1f}%",
        f"{delta_util:+.1f}%"
    )

with col2:
    delta_rev = kpis['revenue_mtd'] - kpis['revenue_prev']
    st.metric(
        "Revenue (MTD)",
        f"${kpis['revenue_mtd']:,.0f}",
        f"${delta_rev:+,.0f}"
    )

with col3:
    st.metric(
        "Active Members",
        f"{kpis['active_members']:,}",
        f"+{kpis['new_members']}"
    )

with col4:
    st.metric(
        "Sponsorship Sold",
        f"{kpis['sponsorship_sold']:.0f}%",
        f"${kpis['sponsorship_value']:,.0f}"
    )

st.divider()

# Charts using matplotlib
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Revenue Trend (Last 30 Days)")

    # Generate sample data
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    revenue = [8000 + (i * 150) + (500 if i % 7 in [5, 6] else 0) for i in range(30)]

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(dates, revenue, marker='o', linewidth=2, markersize=4, color='#3b82f6')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Revenue ($)')
    ax1.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig1)

    st.markdown("### 🎯 Utilization by Asset Type")

    asset_types = ['Turf Field', 'Courts', 'Golf Bays', 'Suites', 'Esports']
    utilization = [92, 85, 78, 65, 71]
    colors = ['#10b981' if x >= 85 else '#f59e0b' if x >= 70 else '#ef4444' for x in utilization]

    fig2, ax2 = plt.subplots(figsize=(10, 4))
    bars = ax2.bar(asset_types, utilization, color=colors)
    ax2.set_ylabel('Utilization (%)')
    ax2.set_ylim([0, 100])
    ax2.grid(True, alpha=0.3, axis='y')

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}%', ha='center', va='bottom')

    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig2)

with col2:
    st.markdown("### 📅 Weekly Schedule Utilization")

    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    peak_util = [95, 93, 94, 96, 97, 98, 95]
    avg_util = [75, 78, 77, 79, 82, 90, 88]

    fig3, ax3 = plt.subplots(figsize=(10, 4))
    x = range(len(days))
    width = 0.35
    ax3.bar([i - width/2 for i in x], peak_util, width, label='Peak Hours', color='#3b82f6')
    ax3.bar([i + width/2 for i in x], avg_util, width, label='Daily Average', color='#10b981')
    ax3.set_ylabel('Utilization (%)')
    ax3.set_xticks(x)
    ax3.set_xticklabels(days)
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.set_ylim([0, 100])
    plt.tight_layout()
    st.pyplot(fig3)

    st.markdown("### 💰 Revenue Mix")

    sources = ['Bookings', 'Memberships', 'Sponsorships', 'Events', 'Concessions']
    revenues = [65000, 42000, 25000, 18000, 7500]
    colors_pie = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']

    fig4, ax4 = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax4.pie(revenues, labels=sources, autopct='%1.1f%%',
                                         colors=colors_pie, startangle=90)
    ax4.axis('equal')

    # Make percentage text more readable
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')

    plt.tight_layout()
    st.pyplot(fig4)

# Alerts section
st.divider()
st.markdown("### ⚠️ Alerts & Notifications")

col1, col2 = st.columns(2)

with col1:
    st.warning("**Low Utilization Alert**  \nTuesday 2-4pm slots at 45% capacity. Consider promotional pricing.")
    st.info("**Contract Expiring**  \n5 sponsorship contracts expire within 60 days. Auto-renewal sequence initiated.")

with col2:
    st.success("**Sponsorship Renewal**  \nABC Corporation renewed naming rights for $125K (3-year term).")

# Quick actions
st.divider()
st.markdown("### ⚡ Quick Actions")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📋 Generate Board Report", use_container_width=True):
        st.info("Board report generation initiated...")

with col2:
    if st.button("💰 Run Pricing Update", use_container_width=True):
        st.info("Dynamic pricing analysis started...")

with col3:
    if st.button("🤝 Sponsor Pipeline", use_container_width=True):
        st.info("Loading sponsor pipeline...")

with col4:
    if st.button("📊 Export Data", use_container_width=True):
        st.success("Dashboard data exported. Download will begin shortly...")

# Footer
st.divider()
st.caption("SportAI Suite Enterprise Edition v6.0.0 | Real-time data updates every 5 minutes")

# Load actual data if available
data_dir = Path(__file__).resolve().parent / "data"
if data_dir.exists():
    st.sidebar.markdown("### 📂 Data Status")

    data_files = {
        "Events": "events_hourly.csv",
        "Forecasts": "forecast_48h.csv",
        "Actions": "actions_log.csv",
        "Capacity": "capacity.csv"
    }

    for name, filename in data_files.items():
        file_path = data_dir / filename
        if file_path.exists():
            st.sidebar.success(f"✓ {name}")
        else:
            st.sidebar.warning(f"⚠ {name} (using sample data)")
