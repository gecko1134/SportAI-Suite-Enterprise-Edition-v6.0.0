#!/usr/bin/env python3
"""
🔵 SportAI → BigQuery + Looker Studio Complete Setup
Step-by-step guide to upload SportAI data to BigQuery and create professional dashboards

This script will:
1. Create Google Cloud Project (if needed)
2. Set up BigQuery dataset
3. Upload all SportAI data
4. Create analytics views
5. Generate Looker Studio dashboard templates
6. Provide step-by-step connection instructions

Run: python bigquery_looker_setup.py
"""

import os
import sys
import pandas as pd
import json
from pathlib import Path

def main():
    print("🔵 SportAI → BigQuery + Looker Studio Setup")
    print("=" * 50)
    print("Complete setup for professional sports facility analytics")
    print()
    
    # Step-by-step setup
    setup_prerequisites()
    setup_bigquery_connection()
    upload_sportai_data()
    create_analytics_views()
    create_looker_templates()
    provide_connection_guide()
    
    print("\n🎉 SUCCESS! BigQuery + Looker Studio Setup Complete!")
    print("=" * 50)
    print("✅ Your SportAI data is now in BigQuery")
    print("✅ Analytics views created for insights")
    print("✅ Looker Studio templates ready")
    print("✅ Step-by-step connection guide provided")
    print()
    print("🚀 Next Steps:")
    print("   1. Open: https://lookerstudio.google.com")
    print("   2. Follow the connection guide below")
    print("   3. Create your professional dashboards!")

def setup_prerequisites():
    """Check and install prerequisites"""
    
    print("📋 Step 1: Prerequisites Setup")
    print("-" * 30)
    
    # Check for required packages
    required_packages = [
        "google-cloud-bigquery",
        "pandas-gbq",
        "google-auth"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package} already installed")
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"   📦 Installing missing packages: {', '.join(missing_packages)}")
        import subprocess
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"   ✅ Installed {package}")
            except:
                print(f"   ⚠️ Could not install {package} - you may need to install manually")
    
    print("\n💡 Google Cloud Account Requirements:")
    print("   • Google account (free Gmail account works)")
    print("   • Google Cloud Project with billing enabled")
    print("   • BigQuery API enabled")
    print()
    
    input("Press Enter when you have a Google Cloud account ready...")

def setup_bigquery_connection():
    """Set up BigQuery connection and authentication"""
    
    print("\n🔐 Step 2: BigQuery Connection Setup")
    print("-" * 35)
    
    print("Setting up Google Cloud authentication...")
    print()
    print("📋 You have 3 authentication options:")
    print("   1. Use your personal Google account (easiest)")
    print("   2. Use service account key file (recommended for production)")
    print("   3. Use Google Cloud CLI (gcloud)")
    print()
    
    auth_choice = input("Choose authentication method (1-3, default=1): ") or "1"
    
    if auth_choice == "1":
        setup_user_authentication()
    elif auth_choice == "2":
        setup_service_account()
    else:
        setup_gcloud_auth()

def setup_user_authentication():
    """Set up user authentication"""
    
    print("\n🔑 Setting up user authentication...")
    print("This will open a browser window for Google authentication.")
    print()
    
    try:
        from google.auth import default
        from google.auth.transport.requests import Request
        from google_auth_oauthlib.flow import InstalledAppFlow
        
        # This will prompt for authentication
        print("✅ Authentication method: User account")
        print("💡 When browser opens, sign in with your Google account")
        print("💡 Grant BigQuery permissions when prompted")
        
    except ImportError:
        print("📦 Installing additional auth packages...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "google-auth-oauthlib"])

def setup_service_account():
    """Set up service account authentication"""
    
    print("\n🔑 Setting up service account...")
    print("💡 To create a service account:")
    print("   1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts")
    print("   2. Click 'Create Service Account'")
    print("   3. Grant 'BigQuery Admin' role")
    print("   4. Create and download JSON key file")
    print()
    
    key_file = input("Enter path to service account JSON file (or press Enter to skip): ")
    
    if key_file and Path(key_file).exists():
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = key_file
        print(f"✅ Service account configured: {key_file}")
    else:
        print("⚠️ Service account not configured - will try default authentication")

def setup_gcloud_auth():
    """Set up gcloud CLI authentication"""
    
    print("\n🔑 Setting up gcloud authentication...")
    print("💡 Make sure you have Google Cloud CLI installed")
    print("💡 Run these commands in your terminal:")
    print()
    print("   gcloud auth login")
    print("   gcloud auth application-default login")
    print()
    
    input("Press Enter after running gcloud authentication commands...")

def upload_sportai_data():
    """Upload SportAI data to BigQuery"""
    
    print("\n📤 Step 3: Uploading SportAI Data to BigQuery")
    print("-" * 45)
    
    # Get project configuration
    project_id = input("🔵 Enter your Google Cloud Project ID: ")
    dataset_id = input("📊 Enter BigQuery dataset name (default: sportai): ") or "sportai"
    location = input("🌍 Enter data location (default: US): ") or "US"
    
    print(f"\n🔧 Configuration:")
    print(f"   Project ID: {project_id}")
    print(f"   Dataset: {dataset_id}")
    print(f"   Location: {location}")
    print()
    
    try:
        # Import BigQuery client
        from google.cloud import bigquery
        import pandas_gbq
        
        print("🔌 Connecting to BigQuery...")
        client = bigquery.Client(project=project_id)
        
        # Create dataset
        dataset_ref = client.dataset(dataset_id)
        try:
            dataset = client.get_dataset(dataset_ref)
            print(f"✅ Using existing dataset: {dataset_id}")
        except:
            print(f"🆕 Creating new dataset: {dataset_id}")
            dataset = bigquery.Dataset(dataset_ref)
            dataset.location = location
            dataset = client.create_dataset(dataset)
            print(f"✅ Created dataset: {dataset_id}")
        
        # Prepare sample data if not exists
        create_sample_data_if_needed()
        
        # Upload tables
        tables_to_upload = {
            "facilities": "Facility information and performance metrics",
            "members": "Member profiles and spending data", 
            "equipment": "Equipment inventory and utilization",
            "sponsors": "Sponsor relationships and values",
            "events": "Events and registration data"
        }
        
        print(f"\n📊 Uploading {len(tables_to_upload)} tables to BigQuery...")
        
        for table_name, description in tables_to_upload.items():
            csv_file = f"data/{table_name}.csv"
            
            if Path(csv_file).exists():
                print(f"\n📤 Uploading {table_name}...")
                print(f"   Description: {description}")
                
                # Read CSV data
                df = pd.read_csv(csv_file)
                print(f"   Records: {len(df):,}")
                print(f"   Columns: {', '.join(df.columns[:5])}{'...' if len(df.columns) > 5 else ''}")
                
                # Upload to BigQuery
                table_id = f"sportai_{table_name}"
                destination_table = f"{dataset_id}.{table_id}"
                
                try:
                    pandas_gbq.to_gbq(
                        df,
                        destination_table=destination_table,
                        project_id=project_id,
                        if_exists='replace',
                        progress_bar=False
                    )
                    print(f"   ✅ Successfully uploaded to {table_id}")
                    
                    # Verify upload
                    query = f"SELECT COUNT(*) as row_count FROM `{project_id}.{destination_table}`"
                    result = pandas_gbq.read_gbq(query, project_id=project_id)
                    uploaded_rows = result.iloc[0]['row_count']
                    print(f"   ✅ Verified: {uploaded_rows:,} rows in BigQuery")
                    
                except Exception as e:
                    print(f"   ❌ Upload failed: {e}")
            else:
                print(f"   ⚠️ File not found: {csv_file}")
        
        # Save configuration for later use
        config = {
            "project_id": project_id,
            "dataset_id": dataset_id,
            "location": location,
            "tables": list(tables_to_upload.keys())
        }
        
        with open("bigquery_config.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print(f"\n🎉 Data upload completed!")
        print(f"✅ Configuration saved to: bigquery_config.json")
        
        return config
        
    except Exception as e:
        print(f"❌ Error uploading data: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check your Google Cloud authentication")
        print("   2. Ensure BigQuery API is enabled")
        print("   3. Verify billing is enabled on your project")
        print("   4. Check you have BigQuery Admin permissions")
        return None

def create_sample_data_if_needed():
    """Create sample data files if they don't exist"""
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Check if data files exist
    required_files = ["facilities.csv", "members.csv", "equipment.csv", "sponsors.csv", "events.csv"]
    missing_files = [f for f in required_files if not (data_dir / f).exists()]
    
    if missing_files:
        print(f"📝 Creating sample data files: {', '.join(missing_files)}")
        
        # Create sample facilities data
        if "facilities.csv" in missing_files:
            facilities_data = {
                'id': [1, 2, 3, 4, 5],
                'name': ['Basketball Court 1', 'Tennis Court 1', 'Swimming Pool', 'Main Dome', 'Fitness Center'],
                'type': ['Indoor Court', 'Tennis Court', 'Aquatic Center', 'Multi-Sport', 'Gym'],
                'capacity': [200, 50, 100, 500, 80],
                'hourly_rate': [150.0, 80.0, 120.0, 350.0, 60.0],
                'utilization': [89.2, 78.3, 65.8, 93.1, 91.2],
                'revenue': [18750.0, 8640.0, 11840.0, 45250.0, 8760.0],
                'status': ['active'] * 5,
                'location': ['North Wing', 'West Complex', 'Aquatic Wing', 'Central Building', 'Fitness Wing']
            }
            pd.DataFrame(facilities_data).to_csv(data_dir / "facilities.csv", index=False)
        
        # Create sample members data
        if "members.csv" in missing_files:
            members_data = {
                'id': list(range(1, 11)),
                'member_id': [f'M{i:03d}' for i in range(1, 11)],
                'name': ['John Smith', 'Sarah Johnson', 'Mike Wilson', 'Emily Davis', 'David Brown',
                        'Lisa Anderson', 'Chris Taylor', 'Amanda Miller', 'Robert Garcia', 'Jennifer Lee'],
                'email': [f'member{i}@email.com' for i in range(1, 11)],
                'tier': ['Premium', 'Elite', 'Basic', 'Premium', 'Elite', 'Premium', 'Basic', 'Elite', 'Premium', 'Basic'],
                'join_date': ['2024-01-15'] * 10,
                'total_spent': [1250.0, 2100.0, 850.0, 1450.0, 2800.0, 1750.0, 650.0, 3200.0, 1680.0, 920.0],
                'status': ['active'] * 10
            }
            pd.DataFrame(members_data).to_csv(data_dir / "members.csv", index=False)
        
        # Create sample equipment data
        if "equipment.csv" in missing_files:
            equipment_data = {
                'id': [1, 2, 3, 4, 5],
                'name': ['Mountain Bikes', 'Tennis Rackets', 'Pool Equipment', 'Basketball Sets', 'Golf Carts'],
                'category': ['Bicycles', 'Sports Equipment', 'Aquatic', 'Sports Equipment', 'Vehicles'],
                'available': [15, 25, 100, 20, 6],
                'rented': [8, 12, 25, 8, 4],
                'daily_rate': [25.0, 15.0, 2.0, 12.0, 50.0],
                'monthly_revenue': [6000.0, 2700.0, 1500.0, 1440.0, 9000.0]
            }
            pd.DataFrame(equipment_data).to_csv(data_dir / "equipment.csv", index=False)
        
        # Create sample sponsors data
        if "sponsors.csv" in missing_files:
            sponsors_data = {
                'id': [1, 2, 3, 4],
                'name': ['Wells Fargo Bank', 'HyVee Grocery', 'Nike Sports', 'TD Ameritrade'],
                'tier': ['Diamond', 'Platinum', 'Silver', 'Gold'],
                'annual_value': [175000.0, 62500.0, 15000.0, 32000.0],
                'engagement': [95.0, 88.0, 85.0, 92.0],
                'satisfaction': [9.2, 8.7, 8.5, 8.9]
            }
            pd.DataFrame(sponsors_data).to_csv(data_dir / "sponsors.csv", index=False)
        
        # Create sample events data
        if "events.csv" in missing_files:
            events_data = {
                'id': [1, 2, 3],
                'name': ['Summer Basketball League', 'Tennis Open', 'Swim Meet Championship'],
                'event_type': ['Tournament', 'Tournament', 'Competition'],
                'start_date': ['2024-06-01', '2024-07-01', '2024-08-01'],
                'capacity': [32, 64, 50],
                'registered': [28, 55, 42],
                'price': [50.0, 75.0, 25.0]
            }
            pd.DataFrame(events_data).to_csv(data_dir / "events.csv", index=False)
        
        print("✅ Sample data files created")

def create_analytics_views():
    """Create BigQuery views for analytics"""
    
    print("\n📊 Step 4: Creating Analytics Views")
    print("-" * 35)
    
    # Load configuration
    try:
        with open("bigquery_config.json", "r") as f:
            config = json.load(f)
    except:
        print("⚠️ Configuration file not found - skipping view creation")
        return
    
    project_id = config["project_id"]
    dataset_id = config["dataset_id"]
    
    try:
        from google.cloud import bigquery
        client = bigquery.Client(project=project_id)
        
        print("Creating analytics views for professional dashboards...")
        
        # Executive Dashboard View
        executive_view = f"""
        CREATE OR REPLACE VIEW `{project_id}.{dataset_id}.executive_dashboard` AS
        SELECT
            -- Key Performance Indicators
            (SELECT SUM(revenue) FROM `{project_id}.{dataset_id}.sportai_facilities`) as total_revenue,
            (SELECT AVG(utilization) FROM `{project_id}.{dataset_id}.sportai_facilities`) as avg_utilization,
            (SELECT COUNT(*) FROM `{project_id}.{dataset_id}.sportai_members` WHERE status = 'active') as active_members,
            (SELECT COUNT(*) FROM `{project_id}.{dataset_id}.sportai_facilities` WHERE status = 'active') as active_facilities,
            (SELECT SUM(annual_value) FROM `{project_id}.{dataset_id}.sportai_sponsors`) as total_sponsor_value,
            CURRENT_DATE() as report_date
        """
        
        # Facility Performance View
        facility_performance = f"""
        CREATE OR REPLACE VIEW `{project_id}.{dataset_id}.facility_performance` AS
        SELECT
            name as facility_name,
            type as facility_type,
            capacity,
            utilization,
            revenue,
            ROUND(revenue / capacity, 2) as revenue_per_seat,
            CASE 
                WHEN utilization >= 90 THEN 'High'
                WHEN utilization >= 70 THEN 'Medium'
                ELSE 'Low'
            END as utilization_category,
            location,
            status
        FROM `{project_id}.{dataset_id}.sportai_facilities`
        ORDER BY revenue DESC
        """
        
        # Member Analytics View
        member_analytics = f"""
        CREATE OR REPLACE VIEW `{project_id}.{dataset_id}.member_analytics` AS
        SELECT
            tier,
            COUNT(*) as member_count,
            ROUND(AVG(total_spent), 2) as avg_spending,
            SUM(total_spent) as total_revenue,
            MIN(total_spent) as min_spending,
            MAX(total_spent) as max_spending,
            ROUND(SUM(total_spent) / (SELECT SUM(total_spent) FROM `{project_id}.{dataset_id}.sportai_members`) * 100, 1) as revenue_percentage
        FROM `{project_id}.{dataset_id}.sportai_members`
        WHERE status = 'active'
        GROUP BY tier
        ORDER BY total_revenue DESC
        """
        
        # Equipment Utilization View
        equipment_utilization = f"""
        CREATE OR REPLACE VIEW `{project_id}.{dataset_id}.equipment_utilization` AS
        SELECT
            name as equipment_name,
            category,
            available,
            rented,
            available + rented as total_units,
            ROUND(SAFE_DIVIDE(rented, available + rented) * 100, 1) as utilization_percentage,
            daily_rate,
            monthly_revenue,
            ROUND(monthly_revenue / (available + rented), 2) as revenue_per_unit
        FROM `{project_id}.{dataset_id}.sportai_equipment`
        ORDER BY utilization_percentage DESC
        """
        
        # Revenue Trends View
        revenue_trends = f"""
        CREATE OR REPLACE VIEW `{project_id}.{dataset_id}.revenue_trends` AS
        SELECT
            type as facility_type,
            COUNT(*) as facility_count,
            SUM(revenue) as total_revenue,
            AVG(revenue) as avg_revenue,
            AVG(utilization) as avg_utilization,
            SUM(capacity) as total_capacity,
            ROUND(SUM(revenue) / SUM(capacity), 2) as revenue_per_seat
        FROM `{project_id}.{dataset_id}.sportai_facilities`
        WHERE status = 'active'
        GROUP BY type
        ORDER BY total_revenue DESC
        """
        
        # Sponsor ROI View
        sponsor_roi = f"""
        CREATE OR REPLACE VIEW `{project_id}.{dataset_id}.sponsor_roi` AS
        SELECT
            name as sponsor_name,
            tier,
            annual_value,
            engagement,
            satisfaction,
            ROUND(annual_value / 12, 2) as monthly_value,
            CASE tier
                WHEN 'Diamond' THEN 1
                WHEN 'Platinum' THEN 2
                WHEN 'Gold' THEN 3
                WHEN 'Silver' THEN 4
                WHEN 'Bronze' THEN 5
                ELSE 6
            END as tier_rank
        FROM `{project_id}.{dataset_id}.sportai_sponsors`
        ORDER BY annual_value DESC
        """
        
        # Execute view creation
        views = {
            "executive_dashboard": executive_view,
            "facility_performance": facility_performance,
            "member_analytics": member_analytics,
            "equipment_utilization": equipment_utilization,
            "revenue_trends": revenue_trends,
            "sponsor_roi": sponsor_roi
        }
        
        for view_name, view_sql in views.items():
            try:
                query_job = client.query(view_sql)
                query_job.result()  # Wait for completion
                print(f"   ✅ Created view: {view_name}")
            except Exception as e:
                print(f"   ❌ Failed to create {view_name}: {e}")
        
        print(f"\n🎉 Analytics views created successfully!")
        print(f"📊 Available views in BigQuery:")
        for view_name in views.keys():
            print(f"   • {dataset_id}.{view_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating views: {e}")
        return False

def create_looker_templates():
    """Create Looker Studio dashboard templates"""
    
    print("\n📋 Step 5: Creating Looker Studio Templates")
    print("-" * 45)
    
    # Load configuration
    try:
        with open("bigquery_config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("⚠️ Configuration file not found - using environment variables")
        import os
        config = {
            "project_id": os.getenv("GCP_PROJECT_ID", "sportai-production"),
            "dataset_id": os.getenv("BIGQUERY_DATASET_ID", "sportai")
        }
    
    project_id = config["project_id"]
    dataset_id = config["dataset_id"]
    
    # Create dashboard configuration
    dashboard_config = {
        "dashboards": [
            {
                "name": "SportAI Executive Dashboard",
                "description": "High-level KPIs and performance metrics for executives",
                "bigquery_connection": {
                    "project_id": project_id,
                    "dataset_id": dataset_id
                },
                "pages": [
                    {
                        "name": "Executive Overview",
                        "components": [
                            {
                                "type": "scorecard",
                                "title": "Total Revenue",
                                "data_source": "executive_dashboard",
                                "metric": "total_revenue",
                                "format": "currency"
                            },
                            {
                                "type": "scorecard", 
                                "title": "Average Utilization",
                                "data_source": "executive_dashboard",
                                "metric": "avg_utilization",
                                "format": "percentage"
                            },
                            {
                                "type": "column_chart",
                                "title": "Facility Revenue",
                                "data_source": "facility_performance",
                                "dimension": "facility_name",
                                "metric": "revenue"
                            },
                            {
                                "type": "pie_chart",
                                "title": "Member Tier Distribution",
                                "data_source": "member_analytics", 
                                "dimension": "tier",
                                "metric": "member_count"
                            }
                        ]
                    }
                ]
            },
            {
                "name": "SportAI Operational Dashboard", 
                "description": "Detailed operational metrics for facility managers",
                "pages": [
                    {
                        "name": "Facility Operations",
                        "components": [
                            {
                                "type": "table",
                                "title": "Facility Performance",
                                "data_source": "facility_performance",
                                "columns": ["facility_name", "utilization", "revenue", "revenue_per_seat"]
                            },
                            {
                                "type": "bar_chart",
                                "title": "Equipment Utilization",
                                "data_source": "equipment_utilization",
                                "dimension": "equipment_name", 
                                "metric": "utilization_percentage"
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    # Save dashboard configuration
    with open("looker_dashboard_config.json", "w") as f:
        json.dump(dashboard_config, f, indent=2)
    
    # Create step-by-step setup instructions
    setup_instructions = f"""
# 📊 Looker Studio Setup Instructions

## Quick Setup Links
- **Looker Studio**: https://lookerstudio.google.com
- **Your BigQuery Project**: https://console.cloud.google.com/bigquery?project={project_id}

## Step-by-Step Dashboard Creation

### 1. Create New Report
1. Go to: https://lookerstudio.google.com
2. Click "Create" → "Report"
3. Choose "BigQuery" as data source

### 2. Connect to Your SportAI Data
**BigQuery Connection Details:**
- Project ID: `{project_id}`
- Dataset: `{dataset_id}`
- Tables/Views to use:
  - `executive_dashboard` (KPIs)
  - `facility_performance` (facility metrics)
  - `member_analytics` (member insights)
  - `equipment_utilization` (equipment data)
  - `revenue_trends` (trend analysis)
  - `sponsor_roi` (sponsor data)

### 3. Build Your Executive Dashboard

#### Page 1: Executive Overview
**Add these components:**

**A. KPI Scorecards (Top Row)**
1. **Total Revenue Card**
   - Data source: `executive_dashboard`
   - Metric: `total_revenue`
   - Format: Currency ($)
   
2. **Average Utilization Card**
   - Data source: `executive_dashboard`
   - Metric: `avg_utilization`
   - Format: Percentage (%)
   
3. **Active Members Card**
   - Data source: `executive_dashboard`
   - Metric: `active_members`
   - Format: Number

4. **Active Facilities Card**
   - Data source: `executive_dashboard`
   - Metric: `active_facilities`
   - Format: Number

**B. Revenue Analysis (Middle Section)**
1. **Facility Revenue Bar Chart**
   - Data source: `facility_performance`
   - Dimension: `facility_name`
   - Metric: `revenue`
   - Sort: Descending by revenue
   - Color: By `utilization_category`

2. **Revenue per Seat Analysis**
   - Data source: `facility_performance`
   - Dimension: `facility_type`
   - Metric: `revenue_per_seat`
   - Chart type: Horizontal bar

**C. Member Insights (Right Section)**
1. **Member Tier Pie Chart**
   - Data source: `member_analytics`
   - Dimension: `tier`
   - Metric: `member_count`
   - Show percentages: Yes

2. **Member Spending Table**
   - Data source: `member_analytics`
   - Columns: `tier`, `member_count`, `avg_spending`, `total_revenue`
   - Sort: By total_revenue descending

### 4. Build Operational Dashboard

#### Page 2: Facility Operations
**Add these components:**

1. **Facility Performance Table**
   - Data source: `facility_performance`
   - Columns: `facility_name`, `facility_type`, `utilization`, `revenue`, `revenue_per_seat`
   - Sort: By revenue descending
   - Conditional formatting: Color utilization by ranges

2. **Utilization Heatmap**
   - Data source: `facility_performance`
   - Rows: `facility_type`
   - Metrics: `utilization`
   - Color scale: Red to Green

3. **Equipment Utilization Chart**
   - Data source: `equipment_utilization`
   - Dimension: `equipment_name`
   - Metric: `utilization_percentage`
   - Chart type: Column chart

### 5. Advanced Features

#### Filters (Add to all pages)
1. **Date Range Filter**
   - Apply to all charts
   - Default: Last 30 days

2. **Facility Type Filter**
   - Field: `facility_type`
   - Type: Dropdown
   - Allow multiple selections

#### Interactive Features
1. **Drill-down capability**
   - Click facility → see detailed metrics
   - Click member tier → see individual members

2. **Cross-filtering**
   - Select facility type → update all charts
   - Select date range → refresh data

### 6. Styling and Branding

#### Theme Colors
- Primary: #667eea (SportAI Blue)
- Secondary: #764ba2 (SportAI Purple)
- Success: #28a745 (Green for positive metrics)
- Warning: #ffc107 (Yellow for attention items)

#### Fonts
- Headers: Google Sans, Bold
- Body text: Google Sans, Regular
- Numbers: Google Sans, Medium

### 7. Sharing and Collaboration

#### Report Sharing
1. Click "Share" button
2. Set permissions:
   - View: All stakeholders
   - Edit: Dashboard administrators
3. Generate shareable link

#### Scheduled Delivery
1. Click "Schedule delivery"
2. Set frequency: Daily/Weekly/Monthly
3. Add recipient email addresses
4. Choose format: PDF/Link

## Sample SQL Queries for Custom Analysis

### Top Performing Facilities
```sql
SELECT 
    facility_name,
    revenue,
    utilization,
    revenue_per_seat
FROM `{project_id}.{dataset_id}.facility_performance`
WHERE utilization > 80
ORDER BY revenue DESC
LIMIT 5;
```

### Member Tier Revenue Analysis
```sql
SELECT 
    tier,
    member_count,
    total_revenue,
    revenue_percentage
FROM `{project_id}.{dataset_id}.member_analytics`
ORDER BY total_revenue DESC;
```

### Equipment ROI Analysis
```sql
SELECT 
    equipment_name,
    utilization_percentage,
    monthly_revenue,
    revenue_per_unit
FROM `{project_id}.