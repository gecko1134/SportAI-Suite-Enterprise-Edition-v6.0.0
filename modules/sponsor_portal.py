"""
SportAI Sponsor Portal Module
Self-service portal for sponsors to view performance and assets
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any

def run(context: Dict[str, Any]):
    """Main sponsor portal execution"""

    st.markdown('<div class="main-header">🎯 Sponsor Portal</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">Welcome, {context["user_ctx"]["name"]}</div>', unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Performance Dashboard",
        "🏷️ My Assets",
        "📈 Analytics",
        "📄 Documents & Invoices"
    ])

    with tab1:
        show_sponsor_dashboard(context)

    with tab2:
        show_sponsor_assets(context)

    with tab3:
        show_sponsor_analytics(context)

    with tab4:
        show_sponsor_documents(context)

def show_sponsor_dashboard(context: Dict[str, Any]):
    """Sponsor performance dashboard"""

    st.markdown("### 📊 Your Sponsorship Overview")

    # Get sponsor data (in production, would query by authenticated user)
    sponsor_data = get_sponsor_data(context)

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Contract Value",
            f"${sponsor_data['annual_value']:,}",
            f"{sponsor_data['term_remaining']} months remaining"
        )

    with col2:
        st.metric(
            "Impressions (YTD)",
            f"{sponsor_data['impressions_ytd']:,}",
            f"+{sponsor_data['impressions_growth']}%"
        )

    with col3:
        st.metric(
            "Events Activated",
            sponsor_data['events_activated'],
            f"{sponsor_data['events_remaining']} remaining"
        )

    with col4:
        st.metric(
            "ROI Estimate",
            f"{sponsor_data['roi_multiplier']}x",
            "vs market average"
        )

    st.divider()

    # Contract summary
    st.markdown("### 📋 Contract Summary")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"""
        **Contract Period:** {sponsor_data['contract_start']} to {sponsor_data['contract_end']}
        **Assets Included:** {sponsor_data['asset_count']} sponsorship assets
        **Annual Investment:** ${sponsor_data['annual_value']:,}
        **Total Contract Value:** ${sponsor_data['total_value']:,}
        **Renewal Date:** {sponsor_data['renewal_date']}
        """)

    with col2:
        # Contract status
        months_elapsed = 6  # Would calculate from actual dates
        total_months = sponsor_data['term_remaining'] + months_elapsed
        progress = months_elapsed / total_months

        st.progress(progress, f"Contract Progress: {int(progress * 100)}%")

        st.markdown(f"""
        **Status:** Active
        **Auto-Renewal:** {sponsor_data['auto_renewal']}
        **Satisfaction Score:** {'⭐' * sponsor_data['satisfaction']}
        """)

    # Performance highlights
    st.divider()
    st.markdown("### 🎯 Performance Highlights")

    highlights = [
        {
            "icon": "📈",
            "title": "Exceeding Impression Goals",
            "description": f"Delivered {sponsor_data['impressions_ytd']:,} impressions (112% of target)"
        },
        {
            "icon": "🎪",
            "title": "Event Activations",
            "description": f"Successfully activated {sponsor_data['events_activated']} events this year"
        },
        {
            "icon": "💰",
            "title": "Strong ROI",
            "description": f"Estimated {sponsor_data['roi_multiplier']}x return on investment"
        },
        {
            "icon": "🤝",
            "title": "Community Impact",
            "description": "Reached 15,000+ local community members"
        }
    ]

    for highlight in highlights:
        st.markdown(f"""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 0.5rem; margin-bottom: 0.5rem; border-left: 4px solid #3b82f6;">
        <strong>{highlight['icon']} {highlight['title']}</strong><br>
        {highlight['description']}
        </div>
        """, unsafe_allow_html=True)

    # Quick actions
    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📧 Contact Account Manager", use_container_width=True):
            st.success("Email sent to your account manager")

    with col2:
        if st.button("🎟️ Request Event Tickets", use_container_width=True):
            st.info("Ticket request form opened")

    with col3:
        if st.button("📊 Download Report", use_container_width=True):
            st.success("Performance report downloading...")

    with col4:
        if st.button("🔄 Renewal Discussion", use_container_width=True):
            st.info("Scheduling renewal meeting...")

def show_sponsor_assets(context: Dict[str, Any]):
    """Show sponsor's assets"""

    st.markdown("### 🏷️ Your Sponsorship Assets")

    sponsor_data = get_sponsor_data(context)

    # Asset categories
    assets = get_sponsor_assets(sponsor_data['id'])

    # Display assets by category
    asset_categories = {}
    for asset in assets:
        category = asset['category']
        if category not in asset_categories:
            asset_categories[category] = []
        asset_categories[category].append(asset)

    for category, category_assets in asset_categories.items():
        with st.expander(f"📁 {category} ({len(category_assets)} assets)", expanded=True):

            for asset in category_assets:
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"**{asset['name']}**")
                    st.caption(asset['description'])

                    # Impression progress
                    impression_pct = (asset['impressions_delivered'] / asset['impressions_target']) * 100
                    st.progress(
                        min(impression_pct / 100, 1.0),
                        f"Impressions: {asset['impressions_delivered']:,} / {asset['impressions_target']:,} ({impression_pct:.0f}%)"
                    )

                with col2:
                    if asset['photo_url']:
                        if st.button(f"📸 View Photo", key=f"photo_{asset['id']}"):
                            st.info("Opening asset photo...")

                    if asset['category'] == 'Digital':
                        if st.button(f"📊 View Analytics", key=f"analytics_{asset['id']}"):
                            st.info("Opening digital analytics...")

                st.divider()

    # Asset summary
    st.markdown("### 📊 Asset Performance Summary")

    asset_summary = []
    for asset in assets:
        asset_summary.append({
            'Asset': asset['name'],
            'Category': asset['category'],
            'Target Impressions': f"{asset['impressions_target']:,}",
            'Delivered': f"{asset['impressions_delivered']:,}",
            'Performance': f"{(asset['impressions_delivered'] / asset['impressions_target'] * 100):.0f}%"
        })

    df_summary = pd.DataFrame(asset_summary)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)

def show_sponsor_analytics(context: Dict[str, Any]):
    """Sponsor analytics and insights"""

    st.markdown("### 📈 Performance Analytics")

    sponsor_data = get_sponsor_data(context)

    # Impression trends
    st.markdown("#### 📊 Impression Trends (Last 12 Months)")

    fig = create_impression_trend_chart()
    st.plotly_chart(fig, use_container_width=True)

    # Breakdown by asset type
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 Impressions by Asset Type")
        fig = create_asset_breakdown_chart()
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 🎯 Audience Demographics")
        demographics = {
            'Age Group': ['13-17', '18-24', '25-34', '35-44', '45-54', '55+'],
            'Percentage': [15, 22, 28, 20, 10, 5]
        }

        fig = go.Figure(data=[go.Bar(
            x=demographics['Age Group'],
            y=demographics['Percentage'],
            marker_color='#3b82f6',
            text=[f"{p}%" for p in demographics['Percentage']],
            textposition='outside'
        )])

        fig.update_layout(
            height=300,
            yaxis_title="Percentage (%)",
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    # Event activation tracking
    st.divider()
    st.markdown("#### 🎪 Event Activations")

    event_activations = [
        {"Date": "2024-09-15", "Event": "Fall Soccer Tournament", "Attendees": 450, "Engagement": "High"},
        {"Date": "2024-08-20", "Event": "Community Open House", "Attendees": 680, "Engagement": "Very High"},
        {"Date": "2024-07-10", "Event": "Summer Basketball League", "Attendees": 320, "Engagement": "Medium"},
        {"Date": "2024-06-05", "Event": "Corporate Golf Day", "Attendees": 88, "Engagement": "High"},
    ]

    df_events = pd.DataFrame(event_activations)
    st.dataframe(df_events, use_container_width=True, hide_index=True)

    # Social media mentions
    st.divider()
    st.markdown("#### 📱 Social Media Impact")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Mentions", "847", "+125")

    with col2:
        st.metric("Reach", "45.2K", "+8.3K")

    with col3:
        st.metric("Engagement Rate", "4.7%", "+0.8%")

    with col4:
        st.metric("Sentiment", "92% Positive", "+3%")

def show_sponsor_documents(context: Dict[str, Any]):
    """Sponsor documents and invoices"""

    st.markdown("### 📄 Documents & Invoices")

    # Document categories
    doc_tabs = st.tabs(["📋 Contract Documents", "💰 Invoices", "📊 Reports"])

    with doc_tabs[0]:
        st.markdown("#### 📋 Contract Documents")

        contract_docs = [
            {"Document": "Sponsorship Agreement 2024-2026", "Date": "2024-01-01", "Type": "Contract"},
            {"Document": "Asset Inventory & Specifications", "Date": "2024-01-01", "Type": "Reference"},
            {"Document": "Brand Guidelines", "Date": "2024-01-15", "Type": "Reference"},
            {"Document": "Logo Usage Agreement", "Date": "2024-01-01", "Type": "Legal"},
        ]

        for doc in contract_docs:
            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.markdown(f"**{doc['Document']}**")

            with col2:
                st.caption(f"Type: {doc['Type']} | Date: {doc['Date']}")

            with col3:
                if st.button("📥 Download", key=f"doc_{doc['Document']}"):
                    st.success("Downloading...")

            st.divider()

    with doc_tabs[1]:
        st.markdown("#### 💰 Invoices & Payments")

        invoices = [
            {"Invoice #": "INV-2024-001", "Date": "2024-01-01", "Amount": 41667, "Status": "Paid", "Due Date": "2024-01-15"},
            {"Invoice #": "INV-2024-002", "Date": "2024-02-01", "Amount": 41667, "Status": "Paid", "Due Date": "2024-02-15"},
            {"Invoice #": "INV-2024-003", "Date": "2024-03-01", "Amount": 41667, "Status": "Paid", "Due Date": "2024-03-15"},
            {"Invoice #": "INV-2024-004", "Date": "2024-04-01", "Amount": 41667, "Status": "Paid", "Due Date": "2024-04-15"},
        ]

        df_invoices = pd.DataFrame(invoices)
        df_invoices['Amount'] = df_invoices['Amount'].apply(lambda x: f"${x:,}")

        st.dataframe(df_invoices, use_container_width=True, hide_index=True)

        # Payment summary
        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("YTD Paid", "$166,668")

        with col2:
            st.metric("Outstanding", "$0")

        with col3:
            st.metric("Next Payment", "Oct 1, 2024")

    with doc_tabs[2]:
        st.markdown("#### 📊 Performance Reports")

        reports = [
            {"Report": "Q3 2024 Performance Summary", "Date": "2024-10-01", "Period": "Jul-Sep 2024"},
            {"Report": "Q2 2024 Performance Summary", "Date": "2024-07-01", "Period": "Apr-Jun 2024"},
            {"Report": "Q1 2024 Performance Summary", "Date": "2024-04-01", "Period": "Jan-Mar 2024"},
        ]

        for report in reports:
            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.markdown(f"**{report['Report']}**")

            with col2:
                st.caption(f"Period: {report['Period']}")

            with col3:
                if st.button("📥 Download", key=f"report_{report['Date']}"):
                    st.success("Downloading report...")

            st.divider()

# Helper functions

def get_sponsor_data(context: Dict[str, Any]) -> Dict:
    """Get sponsor data based on logged-in user"""
    # In production, would query database based on authenticated user
    return {
        'id': 1,
        'name': context['user_ctx']['name'],
        'annual_value': 125000,
        'total_value': 375000,
        'contract_start': '2024-01-01',
        'contract_end': '2026-12-31',
        'renewal_date': '2026-09-01',
        'term_remaining': 26,
        'asset_count': 5,
        'impressions_ytd': 1850000,
        'impressions_target': 1650000,
        'impressions_growth': 12,
        'events_activated': 8,
        'events_remaining': 4,
        'roi_multiplier': 4.2,
        'satisfaction': 5,
        'auto_renewal': 'Enabled'
    }

def get_sponsor_assets(sponsor_id: int) -> list:
    """Get sponsor's assets"""
    return [
        {
            'id': 1,
            'name': 'Facility Naming Rights',
            'category': 'Naming Rights',
            'description': 'Primary naming rights for facility',
            'impressions_target': 1200000,
            'impressions_delivered': 1340000,
            'photo_url': True
        },
        {
            'id': 2,
            'name': 'Entry Banner (20x10ft)',
            'category': 'Physical Signage',
            'description': 'Large banner at main entrance',
            'impressions_target': 450000,
            'impressions_delivered': 480000,
            'photo_url': True
        },
        {
            'id': 3,
            'name': 'Website Homepage Banner',
            'category': 'Digital',
            'description': 'Rotating banner on website homepage',
            'impressions_target': 180000,
            'impressions_delivered': 195000,
            'photo_url': False
        },
        {
            'id': 4,
            'name': 'Social Media Package',
            'category': 'Digital',
            'description': 'Monthly social media posts and mentions',
            'impressions_target': 120000,
            'impressions_delivered': 135000,
            'photo_url': False
        },
        {
            'id': 5,
            'name': 'Suite Package (10 events)',
            'category': 'Activation',
            'description': 'Private suite access for 10 events per year',
            'impressions_target': 50000,
            'impressions_delivered': 38000,
            'photo_url': True
        },
    ]

def create_impression_trend_chart():
    """Create impression trend chart"""
    months = pd.date_range(start='2023-11-01', periods=12, freq='M')
    impressions = [120000, 125000, 135000, 145000, 155000, 160000,
                   165000, 170000, 175000, 180000, 185000, 190000]
    target = [137500] * 12

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=months,
        y=target,
        mode='lines',
        name='Target',
        line=dict(color='gray', dash='dash', width=2)
    ))

    fig.add_trace(go.Scatter(
        x=months,
        y=impressions,
        mode='lines+markers',
        name='Actual',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8),
        fill='tonexty'
    ))

    fig.update_layout(
        height=400,
        yaxis_title="Monthly Impressions",
        xaxis_title="Month",
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig

def create_asset_breakdown_chart():
    """Create asset breakdown pie chart"""
    data = {
        'Asset Type': ['Naming Rights', 'Physical Signage', 'Digital', 'Activation'],
        'Impressions': [1340000, 480000, 330000, 38000]
    }

    fig = go.Figure(data=[go.Pie(
        labels=data['Asset Type'],
        values=data['Impressions'],
        hole=0.4,
        marker_colors=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6']
    )])

    fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))

    return fig
