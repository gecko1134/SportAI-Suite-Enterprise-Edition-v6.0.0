"""
SportAI Bookings Module
Simple booking interface for facility reservations
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any

def run(context: Dict[str, Any]):
    """Main bookings execution"""

    st.markdown('<div class="main-header">📅 Facility Bookings</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Book and manage your facility reservations</div>', unsafe_allow_html=True)

    # Tabs
    tab1, tab2 = st.tabs([
        "📅 Make a Booking",
        "📋 My Reservations"
    ])

    with tab1:
        show_booking_interface(context)

    with tab2:
        show_my_reservations(context)

def show_booking_interface(context: Dict[str, Any]):
    """Main booking interface"""

    st.markdown("### 🏟️ Book a Facility")

    # Step 1: Select facility
    st.markdown("#### 1️⃣ Select Facility")

    facility_categories = {
        "🏟️ Turf Fields": [
            "Turf Field - Full",
            "Turf Field - Half A",
            "Turf Field - Half B"
        ],
        "🏀 Courts": [
            "Court 1",
            "Court 2",
            "Court 3",
            "Court 4"
        ],
        "⛳ Golf Bays": [
            "Golf Bay 1",
            "Golf Bay 2"
        ],
        "🎮 Other Spaces": [
            "Suite A",
            "Suite B",
            "Esports Arena"
        ]
    }

    col1, col2 = st.columns([1, 2])

    with col1:
        selected_category = st.radio(
            "Category",
            list(facility_categories.keys()),
            label_visibility="collapsed"
        )

    with col2:
        selected_facility = st.selectbox(
            "Choose Facility",
            facility_categories[selected_category]
        )

        # Facility info
        facility_info = get_facility_info(selected_facility)

        st.markdown(f"""
        **Capacity:** {facility_info['capacity']} people
        **Rate:** ${facility_info['base_rate']}/hour
        **Available:** {facility_info['hours']}
        """)

    st.divider()

    # Step 2: Select date and time
    st.markdown("#### 2️⃣ Select Date & Time")

    col1, col2, col3 = st.columns(3)

    with col1:
        booking_date = st.date_input(
            "Date",
            min_value=datetime.now().date(),
            value=datetime.now().date() + timedelta(days=1)
        )

    with col2:
        # Show available time slots for selected date
        available_slots = get_available_slots(selected_facility, booking_date)

        booking_time = st.selectbox(
            "Start Time",
            available_slots
        )

    with col3:
        duration = st.selectbox(
            "Duration (hours)",
            [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
        )

    # Show availability calendar
    st.markdown("##### 📅 Weekly Availability View")

    fig = create_availability_calendar(selected_facility, booking_date)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Step 3: Booking details
    st.markdown("#### 3️⃣ Booking Details")

    col1, col2 = st.columns(2)

    with col1:
        booking_name = st.text_input("Name/Organization", value=context['user_ctx'].get('name', ''))
        booking_email = st.text_input("Email", value=context['user_ctx'].get('email', ''))
        booking_phone = st.text_input("Phone")

    with col2:
        booking_type = st.selectbox("Booking Type", [
            "Regular",
            "Youth",
            "Non-Profit",
            "Corporate",
            "Tournament"
        ])

        participants = st.number_input(
            "Expected Participants",
            min_value=1,
            value=10,
            max_value=facility_info['capacity']
        )

        special_requests = st.text_area("Special Requests (optional)")

    st.divider()

    # Step 4: Pricing and confirmation
    st.markdown("#### 4️⃣ Review & Confirm")

    # Calculate price
    pricing = calculate_booking_price(
        facility=selected_facility,
        date=booking_date,
        time=booking_time,
        duration=duration,
        booking_type=booking_type,
        context=context
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("##### 📋 Booking Summary")
        st.markdown(f"""
        **Facility:** {selected_facility}
        **Date:** {booking_date.strftime('%A, %B %d, %Y')}
        **Time:** {booking_time} ({duration} hours)
        **Participants:** {participants}
        **Type:** {booking_type}
        """)

        if special_requests:
            st.markdown(f"**Special Requests:** {special_requests}")

    with col2:
        st.markdown("##### 💰 Pricing")

        st.metric("Base Rate", f"${pricing['base_total']:.2f}")

        if pricing['discount'] > 0:
            st.metric("Discount", f"-${pricing['discount']:.2f}", f"{pricing['discount_pct']}%")

        st.markdown("---")
        st.metric("Total Price", f"${pricing['final_total']:.2f}", label_visibility="visible")

        # Show if member with credits
        user_role = context['user_ctx'].get('role', 'guest')
        if user_role == 'member':
            credits_needed = int(duration * 2)
            st.info(f"💳 Or use {credits_needed} credits")

    # Terms and conditions
    st.divider()

    terms_accepted = st.checkbox(
        "I agree to the facility booking terms and cancellation policy",
        help="Cancellations must be made 24 hours in advance for full refund"
    )

    # Book button
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("✅ Confirm Booking", type="primary", use_container_width=True, disabled=not terms_accepted):
            if booking_name and booking_email and booking_phone:
                # Create booking
                create_booking(
                    facility=selected_facility,
                    date=booking_date,
                    time=booking_time,
                    duration=duration,
                    customer=booking_name,
                    email=booking_email,
                    phone=booking_phone,
                    booking_type=booking_type,
                    participants=participants,
                    price=pricing['final_total'],
                    context=context
                )

                st.success(f"""
                ✅ Booking Confirmed!

                **Confirmation #:** BK-{datetime.now().strftime('%Y%m%d')}-{booking_name[:4].upper()}

                A confirmation email has been sent to {booking_email}.
                """)

                st.balloons()

                context['audit_log']('booking_created', {
                    'facility': selected_facility,
                    'date': str(booking_date),
                    'customer': booking_name
                })
            else:
                st.error("Please fill in all required fields (Name, Email, Phone)")

def show_my_reservations(context: Dict[str, Any]):
    """Show user's reservations"""

    st.markdown("### 📋 My Reservations")

    # Filter options
    col1, col2 = st.columns(2)

    with col1:
        time_filter = st.radio("Show", ["Upcoming", "Past", "All"], horizontal=True)

    with col2:
        sort_by = st.selectbox("Sort by", ["Date (Newest)", "Date (Oldest)", "Facility"])

    st.divider()

    # Get reservations
    reservations = get_user_reservations(context, time_filter)

    if reservations:
        for reservation in reservations:
            with st.expander(
                f"📍 {reservation['facility']} - {reservation['date']} at {reservation['time']}",
                expanded=(reservation['status'] == 'Upcoming')
            ):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"""
                    **Facility:** {reservation['facility']}
                    **Date:** {reservation['date']}
                    **Time:** {reservation['time']}
                    **Duration:** {reservation['duration']} hours
                    **Participants:** {reservation['participants']}
                    **Total Paid:** ${reservation['price']:.2f}
                    **Status:** {reservation['status']}
                    **Confirmation #:** {reservation['confirmation']}
                    """)

                with col2:
                    if reservation['status'] == 'Upcoming':
                        st.markdown("#### Actions")

                        if st.button("✏️ Modify", key=f"mod_{reservation['id']}"):
                            st.info("Modification options:\n- Change time\n- Add participants\n- Add equipment")

                        if st.button("❌ Cancel", key=f"cancel_{reservation['id']}"):
                            if reservation['cancellable']:
                                st.warning("⚠️ Cancel with full refund? (24+ hours notice)")
                                if st.button("Confirm Cancellation", key=f"confirm_cancel_{reservation['id']}"):
                                    st.success("Booking cancelled. Refund processed.")
                            else:
                                st.error("Cannot cancel within 24 hours of booking")

                        if st.button("📄 View Receipt", key=f"receipt_{reservation['id']}"):
                            st.info("Receipt sent to email")

                    elif reservation['status'] == 'Completed':
                        if st.button("🔁 Book Again", key=f"rebook_{reservation['id']}"):
                            st.success("Rebooking with same details...")

    else:
        st.info("No reservations found.")

        if st.button("📅 Make a Booking", type="primary"):
            st.info("Switch to the 'Make a Booking' tab to create a reservation")

# Helper functions

def get_facility_info(facility: str) -> Dict:
    """Get facility information"""
    facilities = {
        "Turf Field - Full": {"capacity": 100, "base_rate": 200, "hours": "6am-11pm"},
        "Turf Field - Half A": {"capacity": 50, "base_rate": 110, "hours": "6am-11pm"},
        "Turf Field - Half B": {"capacity": 50, "base_rate": 110, "hours": "6am-11pm"},
        "Court 1": {"capacity": 20, "base_rate": 35, "hours": "6am-11pm"},
        "Court 2": {"capacity": 20, "base_rate": 35, "hours": "6am-11pm"},
        "Court 3": {"capacity": 20, "base_rate": 35, "hours": "6am-11pm"},
        "Court 4": {"capacity": 20, "base_rate": 35, "hours": "6am-11pm"},
        "Golf Bay 1": {"capacity": 6, "base_rate": 45, "hours": "6am-11pm"},
        "Golf Bay 2": {"capacity": 6, "base_rate": 45, "hours": "6am-11pm"},
        "Suite A": {"capacity": 30, "base_rate": 150, "hours": "6am-11pm"},
        "Suite B": {"capacity": 30, "base_rate": 150, "hours": "6am-11pm"},
        "Esports Arena": {"capacity": 40, "base_rate": 100, "hours": "12pm-11pm"},
    }

    return facilities.get(facility, {"capacity": 20, "base_rate": 50, "hours": "6am-11pm"})

def get_available_slots(facility: str, date: datetime.date) -> list:
    """Get available time slots"""
    # Simplified - in production would check actual availability
    return [
        "6:00 AM", "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "11:00 AM",
        "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM",
        "6:00 PM", "7:00 PM", "8:00 PM", "9:00 PM", "10:00 PM"
    ]

def create_availability_calendar(facility: str, base_date: datetime.date):
    """Create weekly availability calendar"""
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = ['6am', '9am', '12pm', '3pm', '6pm', '9pm']

    # Sample availability (1 = available, 0 = booked)
    data = [
        [1, 1, 0, 1, 0, 1],  # Mon
        [1, 0, 1, 1, 0, 1],  # Tue
        [1, 1, 1, 0, 0, 1],  # Wed
        [1, 0, 1, 1, 1, 0],  # Thu
        [0, 1, 1, 0, 0, 0],  # Fri
        [0, 0, 0, 1, 0, 0],  # Sat
        [0, 1, 0, 1, 1, 1],  # Sun
    ]

    fig = go.Figure(data=go.Heatmap(
        z=data,
        x=hours,
        y=days,
        colorscale=[[0, '#ef4444'], [1, '#10b981']],
        showscale=False,
        text=[['Available' if v == 1 else 'Booked' for v in row] for row in data],
        texttemplate='%{text}',
        textfont={"size": 10}
    ))

    fig.update_layout(
        height=250,
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis_title="Time of Day",
        yaxis_title="Day of Week",
        title="This Week's Availability (Green = Available)"
    )

    return fig

def calculate_booking_price(facility: str, date: datetime.date, time: str,
                           duration: float, booking_type: str, context: Dict) -> Dict:
    """Calculate booking price with discounts"""
    facility_info = get_facility_info(facility)
    base_rate = facility_info['base_rate']

    # Calculate base total
    base_total = base_rate * duration

    # Apply discounts based on booking type
    discount_pct = 0
    if booking_type == "Youth":
        discount_pct = 20
    elif booking_type == "Non-Profit":
        discount_pct = 15
    elif booking_type == "Corporate":
        discount_pct = 0  # May have premium pricing
    elif booking_type == "Tournament":
        discount_pct = 10

    discount = base_total * (discount_pct / 100)
    final_total = base_total - discount

    return {
        'base_total': base_total,
        'discount': discount,
        'discount_pct': discount_pct,
        'final_total': final_total
    }

def create_booking(facility: str, date: datetime.date, time: str, duration: float,
                  customer: str, email: str, phone: str, booking_type: str,
                  participants: int, price: float, context: Dict):
    """Create a new booking"""
    # In production, would insert into database
    pass

def get_user_reservations(context: Dict, filter: str) -> list:
    """Get user reservations"""
    # Sample data - would query from database
    all_reservations = [
        {
            'id': 1,
            'facility': 'Court 2',
            'date': '2025-10-25',
            'time': '6:00 PM',
            'duration': 2,
            'participants': 12,
            'price': 63.00,
            'status': 'Upcoming',
            'confirmation': 'BK-20251022-JOHN',
            'cancellable': True
        },
        {
            'id': 2,
            'facility': 'Turf Field - Half A',
            'date': '2025-10-28',
            'time': '7:00 PM',
            'duration': 1.5,
            'participants': 22,
            'price': 148.50,
            'status': 'Upcoming',
            'confirmation': 'BK-20251022-JOHN',
            'cancellable': True
        },
        {
            'id': 3,
            'facility': 'Golf Bay 1',
            'date': '2024-10-18',
            'time': '2:00 PM',
            'duration': 1,
            'participants': 4,
            'price': 45.00,
            'status': 'Completed',
            'confirmation': 'BK-20241015-JOHN',
            'cancellable': False
        },
    ]

    if filter == "Upcoming":
        return [r for r in all_reservations if r['status'] == 'Upcoming']
    elif filter == "Past":
        return [r for r in all_reservations if r['status'] == 'Completed']
    else:
        return all_reservations
