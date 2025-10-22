#!/bin/bash

echo "🔄 Restarting SportAI Application..."
echo ""

# Kill any running Streamlit processes
echo "1️⃣ Stopping any running Streamlit processes..."
pkill -f "streamlit run sportai_main.py" 2>/dev/null
sleep 2

# Clear Streamlit cache
echo "2️⃣ Clearing Streamlit cache..."
rm -rf ~/.streamlit/cache 2>/dev/null

# Clear Python cache
echo "3️⃣ Clearing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null

echo ""
echo "✅ Cache cleared!"
echo ""
echo "🚀 Starting Streamlit..."
echo ""
echo "The app will open in your browser. All modules should now be available!"
echo ""

# Start Streamlit
streamlit run sportai_main.py
