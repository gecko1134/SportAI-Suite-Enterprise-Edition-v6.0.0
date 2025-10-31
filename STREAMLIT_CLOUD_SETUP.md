# Streamlit Cloud Deployment Configuration

## Issue Resolved
The `ModuleNotFoundError: No module named 'plotly'` error has been fixed by adding all required dependencies to `requirements.txt`.

## Important: Branch Configuration

All fixes are on the branch: **`claude/rerun-and-verify-fu-011CUeRakzieYZiuH3wQZsnY`**

### To Fix Streamlit Cloud Deployment:

You need to configure Streamlit Cloud to deploy from the correct branch:

1. **Go to your Streamlit Cloud dashboard**
   - Visit https://share.streamlit.io/

2. **Click on your app settings** (three dots menu → Settings)

3. **Update the Branch setting:**
   - Change from: `main`
   - Change to: `claude/rerun-and-verify-fu-011CUeRakzieYZiuH3wQZsnY`

4. **Save and Reboot** the app

### What's Included:

✅ **Complete requirements.txt** with all dependencies:
- python-dotenv>=1.0.1
- pandas>=2.0.0
- numpy>=1.24.0
- scikit-learn>=1.3.0
- streamlit>=1.28.0
- matplotlib>=3.7.0
- **plotly>=5.14.0** ← This fixes your error
- reportlab>=4.0.0
- requests>=2.31.0
- pytz>=2023.3

✅ **Reorganized codebase:**
- `modules/` - All backend Python modules
- `dashboard/` - Streamlit dashboard
- `data/` - All data files and schemas
- `docs/` - Generated reports

✅ **All components tested and working:**
- Data validation
- Forecast generation
- Action suggestions
- PDF report generation
- Streamlit dashboards

## Alternative: Merge to Main (Requires Repo Admin)

If you have admin access to merge branches, you can:

```bash
# The changes are ready to merge from the feature branch
# A repository admin needs to merge:
#   claude/rerun-and-verify-fu-011CUeRakzieYZiuH3wQZsnY → main
```

Then Streamlit Cloud will automatically pick up the changes from the main branch.

## Running Locally

To test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the full pipeline
python3 modules/run_all.py

# Start the dashboard
streamlit run dashboard/app.py
# OR
streamlit run sportai_dashboard.py
```

## Support

All code has been tested and verified working. If you continue to see errors after updating the branch in Streamlit Cloud, please check:
1. The branch name is exactly: `claude/rerun-and-verify-fu-011CUeRakzieYZiuH3wQZsnY`
2. Streamlit Cloud has rebooted after the change
3. Check the Streamlit Cloud logs to verify requirements.txt is being read
