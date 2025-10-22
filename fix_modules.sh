#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║        SportAI Module Fix - Complete Cache Clear & Restart        ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Function to print step
step() {
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  $1"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# 1. Kill all Streamlit processes
step "1. Stopping all Streamlit processes..."
pkill -9 -f "streamlit run" 2>/dev/null
pkill -9 streamlit 2>/dev/null
sleep 2
echo "   ✅ Streamlit processes stopped"
echo ""

# 2. Clear Python cache in modules
step "2. Clearing Python cache in modules/..."
if [ -d "modules/__pycache__" ]; then
    rm -rf modules/__pycache__
    echo "   ✅ Cleared modules/__pycache__"
else
    echo "   ℹ️  No modules/__pycache__ found (already clean)"
fi
echo ""

# 3. Clear all Python cache files
step "3. Clearing all .pyc files..."
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "   ✅ All .pyc files removed"
echo ""

# 4. Clear Streamlit cache
step "4. Clearing Streamlit cache..."
if [ -d "$HOME/.streamlit/cache" ]; then
    rm -rf "$HOME/.streamlit/cache"
    echo "   ✅ Streamlit cache cleared"
else
    echo "   ℹ️  No Streamlit cache found"
fi
echo ""

# 5. Verify modules exist
step "5. Verifying modules..."
module_count=$(ls -1 modules/*.py 2>/dev/null | wc -l)
if [ "$module_count" -eq 14 ]; then
    echo "   ✅ All 14 module files found"
    echo ""
    echo "   Modules available:"
    ls -1 modules/*.py | sed 's/modules\//   • /' | grep -v __init__
else
    echo "   ❌ ERROR: Expected 14 modules, found $module_count"
    echo "   ⚠️  You may need to run: git pull"
    exit 1
fi
echo ""

# 6. Check sportai_main.py
step "6. Verifying main application..."
if [ -f "sportai_main.py" ]; then
    echo "   ✅ sportai_main.py found"
else
    echo "   ❌ ERROR: sportai_main.py not found!"
    exit 1
fi
echo ""

# 7. Final verification
step "7. Running final verification..."
python3 diagnose.py | grep -E "(✅|❌|Current branch)" | head -10
echo ""

# 8. Start Streamlit
step "8. Starting Streamlit..."
echo ""
echo "   🚀 Launching SportAI application..."
echo ""
echo "   📍 The app will open in your browser"
echo "   🔑 Login with: admin / admin123"
echo "   ✨ All 14 modules should now work!"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Give user a moment to read
sleep 2

# Start Streamlit
exec streamlit run sportai_main.py
