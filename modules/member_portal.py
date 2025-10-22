"""
SportAI Member Portal Module
Self-service portal for members to manage their membership
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any

def run(context: Dict[str, Any]):
    """Main member portal execution"""

    st.markdown('<div class="main-header">🎫 Member Portal</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-header">Welcome back, {context["user_ctx"]["name"]}!</div>', unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 My Dashboard",
        "🎟️ My Credits & Tier",
        "📅 My Bookings",
        "👤 Account Settings"
    ])

    with tab1:
        show_member_dashboard(context)

    with tab2:
        show_credits_tier(context)

    with tab3:
        show_member_bookings(context)

    with tab4:
        show_account_settings(context)

def show_member_dashboard(context: Dict[str, Any]):
    """Member dashboard overview"""

    st.markdown("### 📊 Your Membership Overview")

    member_data = get_member_data(context)

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Membership Tier",
            member_data['tier'],
            "Active"
        )

    with col2:
        st.metric(
            "Available Credits",
            member_data['credits_available'],
            f"+{member_data['credits_earned_month']} this month"
        )

    with col3:
        st.metric(
            "Next Billing",
            member_data['next_billing'],
            f"${member_data['monthly_fee']}"
        )

    with col4:
        st.metric(
            "Member Since",
            member_data['join_date'],
            f"{member_data['months_member']} months"
        )

    st.divider()

    # Upcoming bookings
    st.markdown("### 📅 Upcoming Bookings")

    upcoming = get_upcoming_bookings(member_data['id'])

    if upcoming:
        for booking in upcoming:
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                st.markdown(f"**{booking['asset']}**")
                st.caption(f"{booking['date']} at {booking['time']}")

            with col2:
                st.markdown(f"**Duration:** {booking['duration']} hours")
                st.caption(f"Credits used: {booking['credits']}")

            with col3:
                if st.button("Cancel", key=f"cancel_{booking['id']}"):
                    st.warning("Cancellation requires confirmation")

            st.divider()
    else:
        st.info("You have no upcoming bookings. Book a facility below!")

    # Quick booking
    st.markdown("### ⚡ Quick Booking")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        asset = st.selectbox("Select Facility", [
            "Turf Field - Full",
            "Turf Field - Half",
            "Court 1", "Court 2", "Court 3", "Court 4",
            "Golf Bay 1", "Golf Bay 2",
            "Suite A", "Suite B"
        ])

    with col2:
        booking_date = st.date_input("Date", min_value=datetime.now())

    with col3:
        booking_time = st.time_input("Start Time")

    with col4:
        duration = st.selectbox("Duration", [1, 1.5, 2, 2.5, 3])

    col1, col2 = st.columns([3, 1])

    with col1:
        estimated_credits = int(duration * 2)  # Simplified calculation
        st.info(f"💳 Estimated credits needed: {estimated_credits} | You have: {member_data['credits_available']}")

    with col2:
        if st.button("📅 Book Now", type="primary", use_container_width=True):
            if member_data['credits_available'] >= estimated_credits:
                st.success(f"✅ {asset} booked for {booking_date}!")
                context['audit_log']('booking_created', {
                    'member': member_data['name'],
                    'asset': asset,
                    'date': str(booking_date)
                })
            else:
                st.error("Insufficient credits. Please purchase more credits below.")

    # Recent activity
    st.divider()
    st.markdown("### 📊 Your Activity")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📈 Bookings This Year")
        fig = create_booking_history_chart()
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### 💰 Credits Usage")
        fig = create_credits_usage_chart()
        st.plotly_chart(fig, use_container_width=True)

def show_credits_tier(context: Dict[str, Any]):
    """Credits and tier management"""

    st.markdown("### 🎟️ Credits & Membership Tier")

    member_data = get_member_data(context)

    # Current tier info
    st.markdown(f"#### Your Current Tier: {member_data['tier']}")

    tier_benefits = get_tier_benefits(member_data['tier'])

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown(f"""
        **Monthly Fee:** ${member_data['monthly_fee']}
        **Monthly Credits:** {tier_benefits['credits_included']}
        **Booking Discount:** {tier_benefits['booking_discount']}%
        **Priority Booking:** {'✓' if tier_benefits['priority_booking'] else '✗'}
        **Suite Access:** {'✓' if tier_benefits['suite_access'] else '✗'}
        **Guest Passes/Month:** {tier_benefits['guest_passes']}
        """)

    with col2:
        # Credits progress
        credits_used_month = 12  # Would calculate from actual data
        credits_total = tier_benefits['credits_included']
        credits_remaining = member_data['credits_available']

        st.metric("Credits This Month", f"{credits_used_month} / {credits_total} used")
        st.progress(credits_used_month / credits_total)

    # Tier comparison
    st.divider()
    st.markdown("#### 🏆 Upgrade Your Tier")

    tiers = ['Bronze', 'Silver', 'Gold', 'Platinum']
    tier_data = []

    for tier in tiers:
        benefits = get_tier_benefits(tier)
        tier_data.append({
            'Tier': tier + (' (Current)' if tier == member_data['tier'] else ''),
            'Monthly Fee': f"${benefits['monthly_fee']}",
            'Credits': benefits['credits_included'],
            'Discount': f"{benefits['booking_discount']}%",
            'Priority': '✓' if benefits['priority_booking'] else '✗',
            'Suite Access': '✓' if benefits['suite_access'] else '✗'
        })

    df_tiers = pd.DataFrame(tier_data)
    st.dataframe(df_tiers, use_container_width=True, hide_index=True)

    # Upgrade options
    if member_data['tier'] != 'Platinum':
        st.info("💎 Upgrade your membership to get more credits, better discounts, and exclusive perks!")

        col1, col2, col3 = st.columns(3)

        current_tier_idx = tiers.index(member_data['tier'])

        for i in range(current_tier_idx + 1, len(tiers)):
            tier = tiers[i]
            benefits = get_tier_benefits(tier)

            with [col1, col2, col3][i - current_tier_idx - 1]:
                if st.button(f"Upgrade to {tier}", use_container_width=True, type="primary" if i == current_tier_idx + 1 else "secondary"):
                    st.success(f"Upgrade to {tier} will take effect on next billing cycle")
                    context['audit_log']('tier_upgrade_requested', {'from': member_data['tier'], 'to': tier})

    # Purchase credits
    st.divider()
    st.markdown("#### 💳 Purchase Additional Credits")

    credit_packages = [
        {"Credits": 5, "Price": 55, "Per Credit": "$11.00", "Savings": "0%"},
        {"Credits": 10, "Price": 100, "Per Credit": "$10.00", "Savings": "9%"},
        {"Credits": 20, "Price": 180, "Per Credit": "$9.00", "Savings": "18%"},
        {"Credits": 50, "Price": 400, "Per Credit": "$8.00", "Savings": "27%"},
    ]

    cols = st.columns(4)

    for idx, package in enumerate(credit_packages):
        with cols[idx]:
            st.markdown(f"""
            <div style="background: #f0f9ff; padding: 1rem; border-radius: 0.5rem; text-align: center;">
            <h3>{package['Credits']} Credits</h3>
            <p style="font-size: 1.5rem; font-weight: bold; color: #3b82f6;">${package['Price']}</p>
            <p>{package['Per Credit']} per credit</p>
            <p style="color: #10b981;">{package['Savings']} savings</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Buy {package['Credits']}", key=f"buy_{package['Credits']}", use_container_width=True):
                st.success(f"✅ Purchased {package['Credits']} credits for ${package['Price']}")
                context['audit_log']('credits_purchased', {'credits': package['Credits'], 'amount': package['Price']})

def show_member_bookings(context: Dict[str, Any]):
    """Member booking history and management"""

    st.markdown("### 📅 My Bookings")

    member_data = get_member_data(context)

    # Booking filters
    col1, col2 = st.columns(2)

    with col1:
        booking_filter = st.radio("Show", ["Upcoming", "Past", "All"], horizontal=True)

    with col2:
        date_range = st.selectbox("Time Range", ["Next 30 Days", "Next 60 Days", "Last 30 Days", "Last 90 Days", "All Time"])

    st.divider()

    # Booking list
    bookings = get_member_booking_history(member_data['id'], booking_filter)

    if bookings:
        for booking in bookings:
            with st.expander(f"📍 {booking['asset']} - {booking['date']} at {booking['time']}"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"""
                    **Facility:** {booking['asset']}
                    **Date:** {booking['date']}
                    **Time:** {booking['time']} - {booking['end_time']}
                    **Duration:** {booking['duration']} hours
                    **Credits Used:** {booking['credits']}
                    **Status:** {booking['status']}
                    """)

                with col2:
                    if booking['status'] == 'Upcoming':
                        if st.button("✏️ Modify", key=f"modify_{booking['id']}"):
                            st.info("Modification form opened")

                        if st.button("❌ Cancel", key=f"cancel_booking_{booking['id']}"):
                            st.warning("Cancellation requires confirmation")

                    if booking['status'] == 'Completed':
                        if st.button("🔁 Book Again", key=f"rebook_{booking['id']}"):
                            st.success("Rebooking form opened")
    else:
        st.info("No bookings found for selected filter.")

    # Booking stats
    st.divider()
    st.markdown("#### 📊 Your Booking Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Bookings", 47)

    with col2:
        st.metric("Favorite Facility", "Court 2")

    with col3:
        st.metric("Favorite Day", "Tuesday")

    with col4:
        st.metric("Favorite Time", "6:00 PM")

def show_account_settings(context: Dict[str, Any]):
    """Account settings and profile management"""

    st.markdown("### 👤 Account Settings")

    member_data = get_member_data(context)

    # Profile information
    st.markdown("#### 📋 Profile Information")

    with st.form("profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name", value=member_data['name'])
            email = st.text_input("Email", value=member_data['email'])
            phone = st.text_input("Phone", value=member_data['phone'])

        with col2:
            address = st.text_area("Address", value=member_data['address'])
            emergency_contact = st.text_input("Emergency Contact", value=member_data['emergency_contact'])
            emergency_phone = st.text_input("Emergency Phone", value=member_data['emergency_phone'])

        if st.form_submit_button("💾 Save Profile"):
            st.success("Profile updated successfully!")
            context['audit_log']('profile_updated', {'member': member_data['id']})

    # Payment methods
    st.divider()
    st.markdown("#### 💳 Payment Methods")

    payment_methods = [
        {"Type": "Visa", "Last 4": "4242", "Expires": "12/25", "Default": True},
    ]

    for pm in payment_methods:
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            default_text = " (Default)" if pm['Default'] else ""
            st.markdown(f"**{pm['Type']} ending in {pm['Last 4']}{default_text}**")

        with col2:
            st.caption(f"Expires: {pm['Expires']}")

        with col3:
            if st.button("Remove", key=f"remove_{pm['Last 4']}"):
                st.warning("Removal requires confirmation")

    if st.button("➕ Add Payment Method"):
        st.info("Payment method form opened")

    # Membership settings
    st.divider()
    st.markdown("#### ⚙️ Membership Settings")

    col1, col2 = st.columns(2)

    with col1:
        auto_renew = st.checkbox("Auto-renew membership", value=True)
        email_notifications = st.checkbox("Email notifications", value=True)
        sms_notifications = st.checkbox("SMS notifications", value=False)

    with col2:
        booking_reminders = st.checkbox("Booking reminders", value=True)
        promotional_emails = st.checkbox("Promotional emails", value=True)
        monthly_statement = st.checkbox("Monthly statement", value=True)

    if st.button("💾 Save Settings"):
        st.success("Settings saved successfully!")

    # Account actions
    st.divider()
    st.markdown("#### 🔒 Account Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔑 Change Password", use_container_width=True):
            st.info("Password change form opened")

    with col2:
        if st.button("📥 Download My Data", use_container_width=True):
            st.success("Data export started")

    with col3:
        if st.button("⏸️ Pause Membership", use_container_width=True):
            st.warning("Pause membership form opened")

# Helper functions

def get_member_data(context: Dict[str, Any]) -> Dict:
    """Get member data"""
    return {
        'id': 1,
        'name': context['user_ctx'].get('name', 'Member'),
        'email': 'member@example.com',
        'phone': '(555) 123-4567',
        'address': '123 Main St\nCity, State 12345',
        'emergency_contact': 'Jane Doe',
        'emergency_phone': '(555) 987-6543',
        'tier': 'Gold',
        'monthly_fee': 75,
        'credits_available': 15,
        'credits_earned_month': 20,
        'join_date': '2024-03-15',
        'months_member': 7,
        'next_billing': 'Nov 1'
    }

def get_tier_benefits(tier: str) -> Dict:
    """Get benefits for a tier"""
    tiers = {
        'Bronze': {
            'monthly_fee': 29,
            'credits_included': 5,
            'booking_discount': 5,
            'priority_booking': False,
            'suite_access': False,
            'guest_passes': 0
        },
        'Silver': {
            'monthly_fee': 45,
            'credits_included': 10,
            'booking_discount': 10,
            'priority_booking': False,
            'suite_access': False,
            'guest_passes': 2
        },
        'Gold': {
            'monthly_fee': 75,
            'credits_included': 20,
            'booking_discount': 15,
            'priority_booking': True,
            'suite_access': True,
            'guest_passes': 4
        },
        'Platinum': {
            'monthly_fee': 125,
            'credits_included': 40,
            'booking_discount': 20,
            'priority_booking': True,
            'suite_access': True,
            'guest_passes': 8
        }
    }
    return tiers.get(tier, tiers['Bronze'])

def get_upcoming_bookings(member_id: int) -> list:
    """Get upcoming bookings"""
    return [
        {
            'id': 1,
            'asset': 'Court 2',
            'date': '2025-10-25',
            'time': '6:00 PM',
            'end_time': '8:00 PM',
            'duration': 2,
            'credits': 4,
            'status': 'Confirmed'
        },
        {
            'id': 2,
            'asset': 'Turf Field - Half',
            'date': '2025-10-28',
            'time': '7:00 PM',
            'end_time': '8:30 PM',
            'duration': 1.5,
            'credits': 3,
            'status': 'Confirmed'
        }
    ]

def get_member_booking_history(member_id: int, filter: str) -> list:
    """Get booking history"""
    all_bookings = [
        {
            'id': 1,
            'asset': 'Court 2',
            'date': '2025-10-25',
            'time': '6:00 PM',
            'end_time': '8:00 PM',
            'duration': 2,
            'credits': 4,
            'status': 'Upcoming'
        },
        {
            'id': 2,
            'asset': 'Turf Field - Half',
            'date': '2025-10-28',
            'time': '7:00 PM',
            'end_time': '8:30 PM',
            'duration': 1.5,
            'credits': 3,
            'status': 'Upcoming'
        },
        {
            'id': 3,
            'asset': 'Court 2',
            'date': '2024-10-18',
            'time': '6:00 PM',
            'end_time': '8:00 PM',
            'duration': 2,
            'credits': 4,
            'status': 'Completed'
        },
    ]

    if filter == "Upcoming":
        return [b for b in all_bookings if b['status'] == 'Upcoming']
    elif filter == "Past":
        return [b for b in all_bookings if b['status'] == 'Completed']
    else:
        return all_bookings

def create_booking_history_chart():
    """Create booking history chart"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
    bookings = [3, 4, 5, 6, 5, 7, 6, 8, 7, 9]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=months,
        y=bookings,
        marker_color='#3b82f6',
        text=bookings,
        textposition='outside'
    ))

    fig.update_layout(
        height=250,
        yaxis_title="Bookings",
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0)
    )

    return fig

def create_credits_usage_chart():
    """Create credits usage chart"""
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']
    earned = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
    used = [12, 16, 18, 22, 19, 24, 21, 26, 23, 28]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=months,
        y=earned,
        name='Earned',
        marker_color='#10b981'
    ))

    fig.add_trace(go.Bar(
        x=months,
        y=used,
        name='Used',
        marker_color='#3b82f6'
    ))

    fig.update_layout(
        height=250,
        yaxis_title="Credits",
        barmode='group',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig
