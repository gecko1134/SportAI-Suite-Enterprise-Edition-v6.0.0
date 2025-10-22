"""
SportAI Grant Builder Module
Grant opportunity tracking, proposal builder, and compliance management
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, Any, List

def run(context: Dict[str, Any]):
    """Main grant builder execution"""

    st.markdown('<div class="main-header">📄 Grant Builder</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Grant opportunities, proposals, and compliance tracking</div>', unsafe_allow_html=True)

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Opportunities",
        "📝 Proposal Builder",
        "📊 Active Grants",
        "✅ Compliance"
    ])

    with tab1:
        show_grant_opportunities(context)

    with tab2:
        show_proposal_builder(context)

    with tab3:
        show_active_grants(context)

    with tab4:
        show_grant_compliance(context)

def show_grant_opportunities(context: Dict[str, Any]):
    """Grant opportunity discovery and tracking"""

    st.markdown("### 🔍 Grant Opportunities")

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Active Opportunities", 15)

    with col2:
        st.metric("Total Potential", "$2.4M")

    with col3:
        st.metric("Deadlines (30 days)", 4)

    with col4:
        st.metric("Match Rate", "87%")

    st.divider()

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        grant_type_filter = st.multiselect(
            "Grant Type",
            ["Federal", "State", "Foundation", "Corporate", "Municipal"],
            default=["Federal", "State", "Foundation"]
        )

    with col2:
        focus_area_filter = st.multiselect(
            "Focus Area",
            ["Youth Sports", "Community Access", "Facility Upgrade", "Equipment", "Programming"],
            default=["Youth Sports", "Community Access"]
        )

    with col3:
        deadline_filter = st.selectbox(
            "Deadline",
            ["All", "Next 30 Days", "Next 60 Days", "Next 90 Days"]
        )

    # Grant opportunities list
    st.divider()
    st.markdown("#### 📋 Available Grants")

    opportunities = [
        {
            "Grant Name": "Youth Sports Access Initiative",
            "Grantor": "State Sports Commission",
            "Type": "State",
            "Amount": "$50,000 - $150,000",
            "Deadline": "2025-11-15",
            "Match": "95%",
            "Focus": "Youth Sports, Community Access",
            "Status": "Deadline Approaching"
        },
        {
            "Grant Name": "Community Facility Enhancement",
            "Grantor": "National Recreation Foundation",
            "Type": "Foundation",
            "Amount": "$100,000 - $500,000",
            "Deadline": "2025-12-01",
            "Match": "92%",
            "Focus": "Facility Upgrade",
            "Status": "Good Fit"
        },
        {
            "Grant Name": "Equipment Modernization Fund",
            "Grantor": "Tech for Sports Foundation",
            "Type": "Foundation",
            "Amount": "$25,000 - $75,000",
            "Deadline": "2025-10-30",
            "Match": "88%",
            "Focus": "Equipment",
            "Status": "Urgent"
        },
        {
            "Grant Name": "Healthy Communities Initiative",
            "Grantor": "HealthCare Partners",
            "Type": "Corporate",
            "Amount": "$30,000 - $100,000",
            "Deadline": "2025-12-15",
            "Match": "85%",
            "Focus": "Community Access, Programming",
            "Status": "Good Fit"
        },
    ]

    df_opps = pd.DataFrame(opportunities)

    st.dataframe(
        df_opps,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Match": st.column_config.ProgressColumn(
                "Match Score",
                format="%s",
                min_value=0,
                max_value=100
            )
        }
    )

    # Grant details
    st.divider()

    selected_grant = st.selectbox(
        "View Grant Details",
        [opp["Grant Name"] for opp in opportunities]
    )

    if selected_grant:
        grant = next((g for g in opportunities if g["Grant Name"] == selected_grant), None)

        if grant:
            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"""
                ### {grant['Grant Name']}

                **Grantor:** {grant['Grantor']}
                **Grant Type:** {grant['Type']}
                **Award Range:** {grant['Amount']}
                **Application Deadline:** {grant['Deadline']}

                **Eligibility Requirements:**
                - 501(c)(3) non-profit organization
                - Serves youth ages 5-18
                - Demonstrates community need
                - Matching funds or in-kind contribution

                **Focus Areas:** {grant['Focus']}

                **Application Requirements:**
                - Project narrative (5 pages max)
                - Detailed budget with justification
                - Board resolution of support
                - 3 years of financial statements
                - Letters of community support (minimum 3)
                - Impact measurement plan
                """)

            with col2:
                st.markdown("#### Quick Actions")

                if st.button("💾 Save Opportunity", use_container_width=True):
                    st.success("Opportunity saved to tracker")

                if st.button("📝 Start Application", use_container_width=True, type="primary"):
                    st.info("Opening proposal builder...")

                if st.button("📧 Email Grant Details", use_container_width=True):
                    st.success("Grant details emailed")

                if st.button("🗓️ Add to Calendar", use_container_width=True):
                    st.success("Deadline added to calendar")

def show_proposal_builder(context: Dict[str, Any]):
    """Interactive grant proposal builder"""

    st.markdown("### 📝 Grant Proposal Builder")

    st.info("""
    This guided tool helps you build competitive grant proposals with AI-powered suggestions.
    Save your progress at any time and return later to continue.
    """)

    # Proposal selection or creation
    col1, col2 = st.columns([3, 1])

    with col1:
        existing_proposals = [
            "New Proposal",
            "Youth Sports Access Initiative (Draft)",
            "Equipment Modernization Fund (In Progress)"
        ]
        proposal = st.selectbox("Select or Create Proposal", existing_proposals)

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ Delete", use_container_width=True):
            st.warning("Delete confirmation required")

    st.divider()

    # Proposal sections
    st.markdown("#### 📋 Proposal Sections")

    with st.expander("1️⃣ Organization Information", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            org_name = st.text_input("Organization Name", value="Skill Shot Sports Complex")
            org_ein = st.text_input("EIN", value="12-3456789")
            org_address = st.text_area("Address", value="123 Main Street\nCity, State 12345")

        with col2:
            contact_name = st.text_input("Primary Contact", value="John Smith")
            contact_email = st.text_input("Email", value="john.smith@skillshot.com")
            contact_phone = st.text_input("Phone", value="(555) 123-4567")

    with st.expander("2️⃣ Project Narrative"):
        st.markdown("**Problem Statement**")
        problem = st.text_area(
            "Describe the community need or problem this project addresses (500 words max)",
            height=150,
            help="Focus on data-driven evidence of need in your community"
        )

        st.markdown("**Project Description**")
        project_desc = st.text_area(
            "Describe your proposed project in detail (750 words max)",
            height=200,
            help="Include goals, activities, timeline, and expected outcomes"
        )

        st.markdown("**Impact & Outcomes**")
        impact = st.text_area(
            "Describe the expected impact and how you will measure success (500 words max)",
            height=150,
            help="Include specific, measurable outcomes and evaluation methods"
        )

    with st.expander("3️⃣ Budget Details"):
        st.markdown("**Project Budget**")

        budget_items = [
            {"Category": "Personnel", "Grant Funds": 45000, "Match": 15000, "Total": 60000},
            {"Category": "Equipment", "Grant Funds": 75000, "Match": 25000, "Total": 100000},
            {"Category": "Facility Improvements", "Grant Funds": 20000, "Match": 10000, "Total": 30000},
            {"Category": "Programming", "Grant Funds": 10000, "Match": 5000, "Total": 15000},
        ]

        df_budget = pd.DataFrame(budget_items)

        edited_budget = st.data_editor(
            df_budget,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic"
        )

        total_grant = edited_budget["Grant Funds"].sum()
        total_match = edited_budget["Match"].sum()
        total_project = edited_budget["Total"].sum()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Grant Request", f"${total_grant:,.0f}")
        with col2:
            st.metric("Match Contribution", f"${total_match:,.0f}")
        with col3:
            st.metric("Total Project Budget", f"${total_project:,.0f}")

    with st.expander("4️⃣ Supporting Documents"):
        st.markdown("**Required Attachments**")

        required_docs = [
            {"Document": "IRS 501(c)(3) Determination Letter", "Status": "✅ Uploaded"},
            {"Document": "Board Resolution", "Status": "✅ Uploaded"},
            {"Document": "Financial Statements (3 years)", "Status": "⏳ Pending"},
            {"Document": "Letters of Support", "Status": "📝 2 of 3"},
            {"Document": "Project Timeline", "Status": "❌ Not Started"},
        ]

        st.dataframe(pd.DataFrame(required_docs), use_container_width=True, hide_index=True)

        uploaded_file = st.file_uploader("Upload Document", type=['pdf', 'docx', 'xlsx'])

        if uploaded_file:
            st.success(f"✅ '{uploaded_file.name}' uploaded successfully")

    with st.expander("5️⃣ AI Writing Assistant"):
        st.markdown("**Get AI-Powered Suggestions**")

        section_to_improve = st.selectbox(
            "Select Section for AI Assistance",
            ["Problem Statement", "Project Description", "Impact & Outcomes", "Budget Narrative"]
        )

        if st.button("✨ Get AI Suggestions"):
            with st.spinner("Generating suggestions..."):
                st.markdown("""
                **AI Suggestions for Problem Statement:**

                Your statement effectively describes the need. Consider adding:
                - Specific demographic data about underserved youth in your area
                - Comparison to state/national averages for youth sports participation
                - Quote from a community stakeholder to add personal impact
                - Reference to recent studies on youth sports access barriers
                """)

    # Save and submit
    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("💾 Save Draft", use_container_width=True):
            st.success("Proposal draft saved")
            context['audit_log']('grant_proposal_saved', {'grant': proposal})

    with col2:
        if st.button("📊 Check Completeness", use_container_width=True):
            st.info("Proposal is 68% complete")

    with col3:
        if st.button("📄 Generate PDF", use_container_width=True):
            st.success("PDF generated for review")

    with col4:
        if st.button("📧 Submit Application", type="primary", use_container_width=True):
            st.warning("Please review all sections before submitting")

def show_active_grants(context: Dict[str, Any]):
    """Track active grant awards"""

    st.markdown("### 📊 Active Grants")

    # Summary
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Active Grants", 5)

    with col2:
        st.metric("Total Awarded", "$487,000")

    with col3:
        st.metric("Funds Expended", "$312,000", "64%")

    with col4:
        st.metric("Reports Due", 2)

    st.divider()

    # Grant list
    st.markdown("#### 📋 Grant Portfolio")

    active_grants = [
        {
            "Grant": "Youth Access Initiative 2024",
            "Grantor": "State Sports Commission",
            "Award": 150000,
            "Expended": 98000,
            "Remaining": 52000,
            "End Date": "2025-06-30",
            "Next Report": "2025-01-15",
            "Status": "On Track"
        },
        {
            "Grant": "Equipment Modernization",
            "Grantor": "Tech Foundation",
            "Award": 75000,
            "Expended": 72000,
            "Remaining": 3000,
            "End Date": "2024-12-31",
            "Next Report": "2024-11-01",
            "Status": "Report Due Soon"
        },
        {
            "Grant": "Community Programming",
            "Grantor": "Health Partners",
            "Award": 100000,
            "Expended": 58000,
            "Remaining": 42000,
            "End Date": "2025-09-30",
            "Next Report": "2025-03-01",
            "Status": "On Track"
        },
    ]

    df_grants = pd.DataFrame(active_grants)

    st.dataframe(
        df_grants,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Award": st.column_config.NumberColumn("Award", format="$%d"),
            "Expended": st.column_config.NumberColumn("Expended", format="$%d"),
            "Remaining": st.column_config.NumberColumn("Remaining", format="$%d"),
        }
    )

    # Grant details
    st.divider()
    st.markdown("#### 📈 Grant Performance Tracking")

    selected_grant_detail = st.selectbox(
        "View Grant Details",
        [g["Grant"] for g in active_grants]
    )

    if selected_grant_detail:
        grant_detail = next((g for g in active_grants if g["Grant"] == selected_grant_detail), None)

        if grant_detail:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"""
                **Grant:** {grant_detail['Grant']}
                **Grantor:** {grant_detail['Grantor']}
                **Award Amount:** ${grant_detail['Award']:,}
                **Grant Period:** Through {grant_detail['End Date']}
                **Next Report Due:** {grant_detail['Next Report']}
                """)

                # Spending progress
                pct_spent = (grant_detail['Expended'] / grant_detail['Award']) * 100
                st.progress(pct_spent / 100, f"Budget Utilized: {pct_spent:.1f}%")

            with col2:
                # Simple bar chart
                fig = go.Figure(data=[
                    go.Bar(
                        x=['Expended', 'Remaining'],
                        y=[grant_detail['Expended'], grant_detail['Remaining']],
                        marker_color=['#3b82f6', '#e5e7eb'],
                        text=[f"${grant_detail['Expended']:,}", f"${grant_detail['Remaining']:,}"],
                        textposition='outside'
                    )
                ])

                fig.update_layout(
                    height=250,
                    title="Budget Status",
                    yaxis_title="Amount ($)",
                    showlegend=False
                )

                st.plotly_chart(fig, use_container_width=True)

def show_grant_compliance(context: Dict[str, Any]):
    """Grant compliance and reporting"""

    st.markdown("### ✅ Grant Compliance & Reporting")

    # Compliance checklist
    st.markdown("#### 📋 Compliance Checklist")

    compliance_items = [
        {"Requirement": "Annual Financial Audit", "Status": "Complete", "Due Date": "Annually", "Last Completed": "2024-03-15"},
        {"Requirement": "Grant Expenditure Reports", "Status": "2 Due Soon", "Due Date": "Quarterly", "Last Completed": "2024-07-15"},
        {"Requirement": "Program Outcome Reporting", "Status": "On Track", "Due Date": "Semi-Annual", "Last Completed": "2024-06-30"},
        {"Requirement": "Site Visits Coordination", "Status": "Scheduled", "Due Date": "As Requested", "Last Completed": "2024-05-10"},
        {"Requirement": "Budget Modification Requests", "Status": "Up to Date", "Due Date": "As Needed", "Last Completed": "2024-08-01"},
    ]

    df_compliance = pd.DataFrame(compliance_items)
    st.dataframe(df_compliance, use_container_width=True, hide_index=True)

    # Upcoming reports
    st.divider()
    st.markdown("#### 📅 Upcoming Reports")

    upcoming_reports = [
        {"Grant": "Equipment Modernization", "Report Type": "Final Report", "Due Date": "2024-11-01", "Status": "In Progress"},
        {"Grant": "Youth Access Initiative", "Report Type": "Quarterly Report", "Due Date": "2025-01-15", "Status": "Not Started"},
    ]

    df_reports = pd.DataFrame(upcoming_reports)
    st.dataframe(df_reports, use_container_width=True, hide_index=True)

    # Quick actions
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📝 Start Report", use_container_width=True, type="primary"):
            st.info("Opening report builder...")

    with col2:
        if st.button("📊 Compliance Dashboard", use_container_width=True):
            st.success("Loading full compliance view...")

    with col3:
        if st.button("📧 Contact Program Officer", use_container_width=True):
            st.success("Email template opened")

# Helper functions would go here
