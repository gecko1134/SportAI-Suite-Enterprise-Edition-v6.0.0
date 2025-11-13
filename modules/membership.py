"""
Membership Segmenter Module
Analyzes and segments members based on behavior, revenue, and engagement
"""

import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def run():
    """Main entry point for membership segmenter tool"""

    st.markdown("### 👥 Membership Segmenter")
    st.markdown("Analyze and segment members based on behavior patterns, revenue, and engagement metrics")

    # Try to load membership data
    data_dir = Path(__file__).parent.parent / "data"
    membership_file = data_dir / "Membership.csv"

    # Sample data if file doesn't exist
    if membership_file.exists():
        try:
            df = pd.read_csv(membership_file)
            st.success(f"✓ Loaded {len(df)} member records")
            using_real_data = True
        except Exception as e:
            st.warning(f"Could not load membership data: {e}")
            df = create_sample_data()
            using_real_data = False
    else:
        df = create_sample_data()
        using_real_data = False
        st.info("Using sample data. Upload Membership.csv to data/ folder for real analysis.")

    # Segmentation options
    st.divider()
    st.markdown("#### Segmentation Settings")

    col1, col2 = st.columns(2)

    with col1:
        segment_method = st.selectbox(
            "Segmentation Method",
            ["RFM Analysis", "Behavioral Clustering", "Tier-Based", "Custom"]
        )

    with col2:
        num_segments = st.slider("Number of Segments", 3, 10, 5)

    # Run segmentation
    if st.button("🔍 Run Segmentation Analysis", use_container_width=True):
        with st.spinner("Analyzing membership data..."):
            segments = perform_segmentation(df, segment_method, num_segments)

            st.success(f"✅ Segmented {len(df)} members into {len(segments)} groups")

            # Display results
            display_segment_results(segments, df)

    # Show current data preview
    st.divider()
    st.markdown("#### Current Member Data")

    if st.checkbox("Show raw data"):
        st.dataframe(df, use_container_width=True)

    # Export options
    st.divider()
    st.markdown("#### Export Options")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📥 Export Segments (CSV)", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"member_segments_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

    with col2:
        if st.button("📊 Generate Report", use_container_width=True):
            st.info("Membership analysis report will be generated")

    with col3:
        if st.button("📧 Email Segments", use_container_width=True):
            st.info("Segment email campaigns feature coming soon")


def create_sample_data():
    """Create sample membership data for demonstration"""
    import numpy as np

    np.random.seed(42)
    n_members = 100

    data = {
        'member_id': [f'M{i:04d}' for i in range(1, n_members + 1)],
        'name': [f'Member {i}' for i in range(1, n_members + 1)],
        'tier': np.random.choice(['Basic', 'Premium', 'Elite'], n_members, p=[0.5, 0.35, 0.15]),
        'join_date': [(datetime.now() - timedelta(days=np.random.randint(30, 730))).strftime('%Y-%m-%d')
                      for _ in range(n_members)],
        'monthly_spend': np.random.gamma(2, 50, n_members).astype(int),
        'visits_per_month': np.random.poisson(8, n_members),
        'last_visit_days': np.random.randint(1, 90, n_members),
        'lifetime_value': np.random.gamma(3, 500, n_members).astype(int),
        'satisfaction_score': np.random.uniform(3.0, 5.0, n_members).round(1)
    }

    return pd.DataFrame(data)


def perform_segmentation(df, method, num_segments):
    """Perform membership segmentation based on selected method"""

    if method == "RFM Analysis":
        # Recency, Frequency, Monetary segmentation
        segments = rfm_segmentation(df, num_segments)
    elif method == "Behavioral Clustering":
        segments = behavioral_clustering(df, num_segments)
    elif method == "Tier-Based":
        segments = tier_based_segmentation(df)
    else:
        segments = custom_segmentation(df, num_segments)

    return segments


def rfm_segmentation(df, num_segments):
    """RFM (Recency, Frequency, Monetary) Analysis"""

    # Calculate RFM scores
    segments = []

    # Simple quintile-based segmentation
    df['recency_score'] = pd.qcut(df.get('last_visit_days', range(len(df))),
                                    min(5, num_segments), labels=False, duplicates='drop')
    df['frequency_score'] = pd.qcut(df.get('visits_per_month', range(len(df))),
                                      min(5, num_segments), labels=False, duplicates='drop')
    df['monetary_score'] = pd.qcut(df.get('monthly_spend', range(len(df))),
                                     min(5, num_segments), labels=False, duplicates='drop')

    # Combine scores
    df['rfm_segment'] = (df['recency_score'] + df['frequency_score'] + df['monetary_score']) // 3

    # Create segment names
    segment_names = {
        0: "At Risk",
        1: "Needs Attention",
        2: "Average",
        3: "Loyal",
        4: "Champions"
    }

    for seg_id, seg_name in segment_names.items():
        if seg_id in df['rfm_segment'].values:
            segment_data = df[df['rfm_segment'] == seg_id]
            segments.append({
                'name': seg_name,
                'count': len(segment_data),
                'avg_spend': segment_data.get('monthly_spend', [0]).mean(),
                'avg_visits': segment_data.get('visits_per_month', [0]).mean()
            })

    return segments


def behavioral_clustering(df, num_segments):
    """Cluster members based on behavioral patterns"""
    # Simplified clustering
    segments = []

    # Use spending and visit patterns
    if 'monthly_spend' in df.columns and 'visits_per_month' in df.columns:
        df['behavior_score'] = (df['monthly_spend'] / df['monthly_spend'].max() +
                                df['visits_per_month'] / df['visits_per_month'].max()) / 2

        df['cluster'] = pd.qcut(df['behavior_score'], num_segments, labels=False, duplicates='drop')

        for i in range(num_segments):
            cluster_data = df[df['cluster'] == i]
            if len(cluster_data) > 0:
                segments.append({
                    'name': f'Cluster {i+1}',
                    'count': len(cluster_data),
                    'avg_spend': cluster_data['monthly_spend'].mean(),
                    'avg_visits': cluster_data['visits_per_month'].mean()
                })

    return segments


def tier_based_segmentation(df):
    """Segment based on membership tier"""
    segments = []

    if 'tier' in df.columns:
        for tier in df['tier'].unique():
            tier_data = df[df['tier'] == tier]
            segments.append({
                'name': f'{tier} Members',
                'count': len(tier_data),
                'avg_spend': tier_data.get('monthly_spend', [0]).mean(),
                'avg_visits': tier_data.get('visits_per_month', [0]).mean()
            })

    return segments


def custom_segmentation(df, num_segments):
    """Custom segmentation logic"""
    # Placeholder for custom segmentation
    return rfm_segmentation(df, num_segments)


def display_segment_results(segments, df):
    """Display segmentation results with visualizations"""

    st.divider()
    st.markdown("#### 📊 Segmentation Results")

    # Summary metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Segments", len(segments))

    with col2:
        total_members = sum(s['count'] for s in segments)
        st.metric("Total Members", total_members)

    with col3:
        avg_segment_size = total_members / len(segments) if segments else 0
        st.metric("Avg Segment Size", f"{avg_segment_size:.0f}")

    # Segment breakdown table
    st.markdown("##### Segment Breakdown")
    segment_df = pd.DataFrame(segments)

    if not segment_df.empty and 'avg_spend' in segment_df.columns:
        segment_df['avg_spend'] = segment_df['avg_spend'].round(2)
        segment_df['avg_visits'] = segment_df['avg_visits'].round(1)

    st.dataframe(segment_df, use_container_width=True)

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Members per Segment")
        if segments:
            fig1, ax1 = plt.subplots(figsize=(8, 6))
            names = [s['name'] for s in segments]
            counts = [s['count'] for s in segments]
            ax1.bar(names, counts, color='#3b82f6')
            ax1.set_ylabel('Number of Members')
            ax1.set_xlabel('Segment')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig1)

    with col2:
        st.markdown("##### Average Spend by Segment")
        if segments and 'avg_spend' in segments[0]:
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            names = [s['name'] for s in segments]
            spends = [s['avg_spend'] for s in segments]
            ax2.bar(names, spends, color='#10b981')
            ax2.set_ylabel('Avg Monthly Spend ($)')
            ax2.set_xlabel('Segment')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig2)

    # Recommendations
    st.divider()
    st.markdown("#### 💡 Segment-Specific Recommendations")

    for segment in segments:
        with st.expander(f"📌 {segment['name']} ({segment['count']} members)"):
            st.markdown(f"**Average Monthly Spend:** ${segment.get('avg_spend', 0):.2f}")
            st.markdown(f"**Average Visits/Month:** {segment.get('avg_visits', 0):.1f}")
            st.markdown("**Recommended Actions:**")
            st.markdown(generate_recommendations(segment))


def generate_recommendations(segment):
    """Generate recommendations based on segment characteristics"""

    name = segment['name'].lower()
    avg_spend = segment.get('avg_spend', 0)

    if 'risk' in name or 'attention' in name:
        return """
        - 🎯 Send re-engagement campaign
        - 💰 Offer special comeback discount (10-15%)
        - 📧 Personalized outreach from account manager
        - 🎁 Complimentary session or upgrade trial
        """
    elif 'champion' in name or 'loyal' in name or 'elite' in name:
        return """
        - 🌟 VIP recognition program
        - 💎 Exclusive early access to new facilities
        - 🎖️ Referral rewards program
        - 📱 Priority booking and support
        """
    elif avg_spend > 150:
        return """
        - ⬆️ Upsell to premium tier
        - 🏆 Premium amenities access
        - 🎯 Targeted package deals
        - 👥 Group/family membership offers
        """
    else:
        return """
        - 📈 Engagement campaigns to increase visits
        - 🎉 Special event invitations
        - 💪 Intro to premium features/facilities
        - 🤝 Community building activities
        """


# Alias for the module
membership_segmenter = type('Module', (), {'run': run})()
