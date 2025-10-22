"""
SportAI Event Manager Module
Tournament, event, and program management
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any, List

def run(context: Dict[str, Any]):
    """Main event manager execution"""

    st.markdown('<div class="main-header">📅 Event Manager</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Tournaments, events, and program management</div>', unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Event Dashboard",
        "🏆 Tournaments",
        "🎉 Special Events",
        "📋 Programs & Leagues"
    ])

    with tab1:
        show_event_dashboard(context)

    with tab2:
        show_tournament_manager(context)

    with tab3:
        show_special_events(context)

    with tab4:
        show_programs_leagues(context)

def show_event_dashboard(context: Dict[str, Any]):
    """Event overview dashboard"""

    st.markdown("### 📊 Events Overview")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Upcoming Events", 12, "+3")

    with col2:
        st.metric("Events This Month", 8)

    with col3:
        st.metric("Total Participants", 1847, "+215")

    with col4:
        st.metric("Event Revenue (YTD)", "$124,500", "+18%")

    st.divider()

    # Calendar view
    st.markdown("### 📅 Event Calendar")

    # Upcoming events
    upcoming_events = [
        {
            "Date": "2025-10-25",
            "Event": "Youth Soccer Tournament",
            "Type": "Tournament",
            "Participants": 96,
            "Revenue": 4800,
            "Status": "Confirmed"
        },
        {
            "Date": "2025-10-28",
            "Event": "Corporate Team Building",
            "Type": "Corporate Event",
            "Participants": 45,
            "Revenue": 3200,
            "Status": "Confirmed"
        },
        {
            "Date": "2025-11-02",
            "Event": "3v3 Basketball League (Week 1)",
            "Type": "League",
            "Participants": 64,
            "Revenue": 1920,
            "Status": "Confirmed"
        },
        {
            "Date": "2025-11-05",
            "Event": "Community Open House",
            "Type": "Community Event",
            "Participants": 200,
            "Revenue": 0,
            "Status": "Planning"
        },
        {
            "Date": "2025-11-10",
            "Event": "Indoor Golf Championship",
            "Type": "Tournament",
            "Participants": 32,
            "Revenue": 6400,
            "Status": "Registration Open"
        },
    ]

    df_upcoming = pd.DataFrame(upcoming_events)

    st.dataframe(
        df_upcoming,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Revenue": st.column_config.NumberColumn("Revenue", format="$%d"),
            "Participants": st.column_config.NumberColumn("Participants", format="%d")
        }
    )

    # Event performance
    st.divider()
    st.markdown("### 📈 Event Performance")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Events by Type (Last 6 Months)")
        fig = create_events_by_type_chart()
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Monthly Revenue Trend")
        fig = create_event_revenue_trend()
        st.plotly_chart(fig, use_container_width=True)

    # Quick actions
    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("➕ Create Event", use_container_width=True, type="primary"):
            st.info("Opening event creation form...")

    with col2:
        if st.button("🏆 New Tournament", use_container_width=True):
            st.info("Opening tournament builder...")

    with col3:
        if st.button("📧 Email Participants", use_container_width=True):
            st.success("Email composer opened")

    with col4:
        if st.button("📊 Event Report", use_container_width=True):
            st.success("Generating event summary report...")

def show_tournament_manager(context: Dict[str, Any]):
    """Tournament planning and management"""

    st.markdown("### 🏆 Tournament Manager")

    # Tournament list
    st.markdown("#### 📋 Active Tournaments")

    tournaments = [
        {
            "Tournament": "Youth Soccer Tournament",
            "Date": "2025-10-25",
            "Sport": "Soccer",
            "Teams": 12,
            "Participants": 96,
            "Fee": "$50/team",
            "Status": "Registration Closed"
        },
        {
            "Tournament": "Indoor Golf Championship",
            "Date": "2025-11-10",
            "Sport": "Golf",
            "Teams": 0,
            "Participants": 32,
            "Fee": "$200/player",
            "Status": "Registration Open"
        },
        {
            "Tournament": "Holiday Basketball Classic",
            "Date": "2025-12-20",
            "Sport": "Basketball",
            "Teams": 16,
            "Participants": 128,
            "Fee": "$400/team",
            "Status": "Planning"
        },
    ]

    df_tournaments = pd.DataFrame(tournaments)
    st.dataframe(df_tournaments, use_container_width=True, hide_index=True)

    st.divider()

    # Tournament builder
    st.markdown("#### ➕ Create New Tournament")

    with st.form("tournament_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            tournament_name = st.text_input("Tournament Name")
            tournament_sport = st.selectbox("Sport", [
                "Soccer", "Basketball", "Volleyball", "Golf",
                "Esports", "Multi-Sport", "Other"
            ])
            tournament_date = st.date_input("Tournament Date")

        with col2:
            tournament_format = st.selectbox("Format", [
                "Single Elimination", "Double Elimination",
                "Round Robin", "Pool Play + Bracket", "Stroke Play"
            ])
            max_teams = st.number_input("Max Teams/Players", min_value=4, value=16)
            entry_fee = st.number_input("Entry Fee ($)", min_value=0, value=50)

        with col3:
            age_division = st.multiselect("Age Divisions", [
                "U8", "U10", "U12", "U14", "U16", "U18", "Adult", "Open"
            ])
            skill_level = st.selectbox("Skill Level", [
                "Recreational", "Competitive", "Elite", "Mixed"
            ])
            registration_deadline = st.date_input(
                "Registration Deadline",
                datetime.now() + timedelta(days=14)
            )

        tournament_description = st.text_area("Tournament Description")

        st.markdown("#### 🏅 Prizes & Awards")
        col1, col2 = st.columns(2)

        with col1:
            first_prize = st.text_input("1st Place Prize", "Trophy + $500")
            second_prize = st.text_input("2nd Place Prize", "Trophy + $250")

        with col2:
            third_prize = st.text_input("3rd Place Prize", "Trophy + $100")
            participation = st.checkbox("Participation Medals", value=True)

        submitted = st.form_submit_button("🏆 Create Tournament", type="primary")

        if submitted and tournament_name:
            st.success(f"✅ Tournament '{tournament_name}' created successfully!")
            st.info("Tournament page created. Registration is now open.")
            context['audit_log']('tournament_created', {
                'name': tournament_name,
                'sport': tournament_sport,
                'date': str(tournament_date)
            })

    # Tournament details view
    st.divider()
    st.markdown("#### 🔍 Tournament Details")

    selected_tournament = st.selectbox(
        "View Tournament",
        [t["Tournament"] for t in tournaments]
    )

    if selected_tournament:
        tournament = next((t for t in tournaments if t["Tournament"] == selected_tournament), None)

        if tournament:
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"""
                **Tournament:** {tournament['Tournament']}
                **Date:** {tournament['Date']}
                **Sport:** {tournament['Sport']}
                **Entry Fee:** {tournament['Fee']}
                **Status:** {tournament['Status']}
                """)

                st.markdown("**Registration Status:**")
                if tournament['Teams'] > 0:
                    st.progress(tournament['Teams'] / 16, f"{tournament['Teams']} / 16 Teams Registered")
                else:
                    st.progress(tournament['Participants'] / 32, f"{tournament['Participants']} / 32 Players Registered")

            with col2:
                st.markdown("#### Quick Actions")
                if st.button("📋 View Bracket", key="bracket"):
                    st.info("Opening bracket view...")
                if st.button("📧 Email Update", key="email_tournament"):
                    st.success("Email sent to all participants")
                if st.button("💰 Process Payments", key="payments"):
                    st.info("Payment processing opened")
                if st.button("📊 Tournament Report", key="t_report"):
                    st.success("Generating report...")

def show_special_events(context: Dict[str, Any]):
    """Special events and programs"""

    st.markdown("### 🎉 Special Events")

    # Event types
    event_types = ["Corporate Events", "Community Events", "Fundraisers", "Camps & Clinics"]
    selected_type = st.radio("Event Type", event_types, horizontal=True)

    st.divider()

    if selected_type == "Corporate Events":
        st.markdown("#### 💼 Corporate Events")

        corporate_events = [
            {
                "Company": "Tech Solutions Inc",
                "Event": "Team Building Day",
                "Date": "2025-10-28",
                "Attendees": 45,
                "Package": "Premium",
                "Revenue": 3200,
                "Status": "Confirmed"
            },
            {
                "Company": "Healthcare Partners",
                "Event": "Annual Retreat",
                "Date": "2025-11-15",
                "Attendees": 80,
                "Package": "Full Day",
                "Revenue": 6400,
                "Status": "Planning"
            },
        ]

        df_corporate = pd.DataFrame(corporate_events)
        st.dataframe(df_corporate, use_container_width=True, hide_index=True)

    elif selected_type == "Community Events":
        st.markdown("#### 🏘️ Community Events")

        community_events = [
            {
                "Event": "Community Open House",
                "Date": "2025-11-05",
                "Expected Attendance": 200,
                "Activities": "Tours, Demos, Free Play",
                "Cost": "Free",
                "Status": "Planning"
            },
            {
                "Event": "Youth Sports Expo",
                "Date": "2025-12-01",
                "Expected Attendance": 350,
                "Activities": "Clinics, Tryouts, Info Fair",
                "Cost": "Free",
                "Status": "Confirmed"
            },
        ]

        df_community = pd.DataFrame(community_events)
        st.dataframe(df_community, use_container_width=True, hide_index=True)

    elif selected_type == "Fundraisers":
        st.markdown("#### 💰 Fundraising Events")

        fundraisers = [
            {
                "Event": "Charity Golf Tournament",
                "Date": "2025-11-20",
                "Beneficiary": "Youth Sports Scholarship Fund",
                "Goal": 15000,
                "Raised": 8500,
                "Participants": 48,
                "Status": "Registration Open"
            },
        ]

        df_fundraisers = pd.DataFrame(fundraisers)
        st.dataframe(df_fundraisers, use_container_width=True, hide_index=True)

    else:  # Camps & Clinics
        st.markdown("#### ⚽ Camps & Clinics")

        camps = [
            {
                "Program": "Winter Break Soccer Camp",
                "Dates": "Dec 26-30, 2025",
                "Ages": "8-14",
                "Capacity": 30,
                "Enrolled": 22,
                "Fee": "$250",
                "Status": "Registration Open"
            },
            {
                "Program": "Basketball Skills Clinic",
                "Dates": "Nov 15-17, 2025",
                "Ages": "10-16",
                "Capacity": 24,
                "Enrolled": 24,
                "Fee": "$175",
                "Status": "Full - Waitlist"
            },
        ]

        df_camps = pd.DataFrame(camps)
        st.dataframe(df_camps, use_container_width=True, hide_index=True)

    # Create new event
    st.divider()

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("#### ➕ Create New Special Event")

    with col2:
        if st.button("📝 Create Event Form", use_container_width=True, type="primary"):
            st.info("Opening event creation wizard...")

def show_programs_leagues(context: Dict[str, Any]):
    """League and program management"""

    st.markdown("### 📋 Programs & Leagues")

    # Active leagues
    st.markdown("#### 🏀 Active Leagues")

    leagues = [
        {
            "League": "3v3 Basketball League",
            "Season": "Fall 2024",
            "Teams": 8,
            "Games/Week": 4,
            "Weeks": 10,
            "Start": "2025-11-02",
            "Status": "Active"
        },
        {
            "League": "Indoor Soccer League",
            "Season": "Winter 2024-25",
            "Teams": 12,
            "Games/Week": 6,
            "Weeks": 12,
            "Start": "2025-12-01",
            "Status": "Registration Open"
        },
        {
            "League": "Adult Volleyball League",
            "Season": "Fall 2024",
            "Teams": 6,
            "Games/Week": 3,
            "Weeks": 8,
            "Start": "2025-10-15",
            "Status": "In Progress"
        },
    ]

    df_leagues = pd.DataFrame(leagues)
    st.dataframe(df_leagues, use_container_width=True, hide_index=True)

    # League details
    st.divider()

    selected_league = st.selectbox("View League Details", [l["League"] for l in leagues])

    if selected_league:
        league = next((l for l in leagues if l["League"] == selected_league), None)

        if league:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Registered Teams", league['Teams'])
                st.metric("Total Players", league['Teams'] * 8)

            with col2:
                st.metric("Games Played", 24)
                st.metric("Games Remaining", 16)

            with col3:
                st.metric("Revenue", f"${league['Teams'] * 400:,}")
                st.metric("Avg Attendance", 145)

            st.divider()

            # Standings
            st.markdown("#### 📊 League Standings")

            standings = [
                {"Rank": 1, "Team": "Thunder", "Wins": 6, "Losses": 0, "Points": 156},
                {"Rank": 2, "Team": "Lightning", "Wins": 5, "Losses": 1, "Points": 148},
                {"Rank": 3, "Team": "Storm", "Wins": 4, "Losses": 2, "Points": 142},
                {"Rank": 4, "Team": "Blitz", "Wins": 3, "Losses": 3, "Points": 138},
                {"Rank": 5, "Team": "Flash", "Wins": 2, "Losses": 4, "Points": 132},
                {"Rank": 6, "Team": "Spark", "Wins": 1, "Losses": 5, "Points": 125},
                {"Rank": 7, "Team": "Bolt", "Wins": 1, "Losses": 5, "Points": 122},
                {"Rank": 8, "Team": "Charge", "Wins": 0, "Losses": 6, "Points": 115},
            ]

            df_standings = pd.DataFrame(standings)
            st.dataframe(df_standings, use_container_width=True, hide_index=True)

    # Programs
    st.divider()
    st.markdown("#### 📚 Programs")

    programs = [
        {"Program": "Youth Development Academy", "Participants": 45, "Sessions/Week": 3, "Fee": "$150/month"},
        {"Program": "Adult Fitness Classes", "Participants": 28, "Sessions/Week": 4, "Fee": "$75/month"},
        {"Program": "Senior Walking Club", "Participants": 18, "Sessions/Week": 2, "Fee": "$25/month"},
    ]

    df_programs = pd.DataFrame(programs)
    st.dataframe(df_programs, use_container_width=True, hide_index=True)

# Helper functions

def create_events_by_type_chart():
    """Create events by type pie chart"""
    data = {
        'Type': ['Tournaments', 'Corporate Events', 'Community Events', 'Leagues', 'Camps/Clinics'],
        'Count': [8, 6, 4, 3, 5]
    }

    fig = go.Figure(data=[go.Pie(
        labels=data['Type'],
        values=data['Count'],
        hole=0.4,
        marker_colors=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899']
    )])

    fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))

    return fig

def create_event_revenue_trend():
    """Create event revenue trend chart"""
    months = pd.date_range(start='2024-05-01', periods=6, freq='M')
    revenue = [8500, 12000, 15500, 18000, 21500, 24000]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=months,
        y=revenue,
        mode='lines+markers',
        fill='tozeroy',
        line=dict(color='#10b981', width=3),
        marker=dict(size=8)
    ))

    fig.update_layout(
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis_title="Revenue ($)",
        xaxis_title="Month"
    )

    return fig
