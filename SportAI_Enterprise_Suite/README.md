# SportAI Enterprise Suite

Complete Sports Facility Management Platform

## Quick Start

1. Install and run:
```bash
python install.py
python run.py
```

2. Access the application:
- Main App: http://localhost:8000
- Dashboard: http://localhost:8501
- API Docs: http://localhost:8000/docs

3. Login with:
- Email: admin@sportai.com
- Password: admin123

## Features

- 🏢 Facility Management
- 👥 Member Management  
- 🔧 Equipment Tracking
- 🤝 Sponsor Relations
- 📅 Event Management
- 💰 Financial Analytics
- 🤖 AI Insights
- 📊 Interactive Dashboards

## CLI Usage

```bash
# Show dashboard
python cli/manager.py dashboard

# List data
python cli/manager.py list facilities
python cli/manager.py list members

# Export data
python cli/manager.py export facilities
```

## API Usage

```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login', 
                        data={'email': 'admin@sportai.com', 'password': 'admin123'})
token = response.json()['access_token']

# Get data
headers = {'Authorization': f'Bearer {token}'}
facilities = requests.get('http://localhost:8000/api/facilities', headers=headers)
```

© 2024 SportAI Solutions, LLC. All Rights Reserved.
