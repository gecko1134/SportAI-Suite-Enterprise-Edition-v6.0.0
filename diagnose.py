"""
Diagnostic script to identify why modules aren't loading in Streamlit
Run this to see what's happening
"""

import sys
import os
from pathlib import Path

print("=" * 70)
print("SportAI Module Loading Diagnostic")
print("=" * 70)
print()

# 1. Check working directory
print("1. Working Directory:")
print(f"   Current: {os.getcwd()}")
print(f"   Expected: .../SportAI-Suite-Enterprise-Edition-v6.0.0")
print()

# 2. Check if modules directory exists
print("2. Modules Directory:")
modules_path = Path("modules")
if modules_path.exists():
    print(f"   ✅ modules/ exists")
    module_files = list(modules_path.glob("*.py"))
    print(f"   ✅ Found {len(module_files)} Python files")

    # List all modules
    for f in sorted(module_files):
        if f.name != '__init__.py':
            print(f"      • {f.name}")
else:
    print(f"   ❌ modules/ directory NOT FOUND")
    print(f"   🔍 Looking in: {modules_path.absolute()}")
print()

# 3. Check Python path
print("3. Python Path:")
print(f"   sys.path[0]: {sys.path[0]}")
current_dir = str(Path.cwd())
if current_dir in sys.path:
    print(f"   ✅ Current directory is in sys.path")
else:
    print(f"   ⚠️  Current directory NOT in sys.path")
    print(f"   Adding it now...")
    sys.path.insert(0, current_dir)
print()

# 4. Try importing modules (like sportai_main.py does)
print("4. Testing Module Imports (as sportai_main.py does):")
test_modules = ['dashboard', 'facility_ops', 'ai_scheduling']

for module_name in test_modules:
    try:
        import importlib
        module_path = f"modules.{module_name}"
        module = importlib.import_module(module_path)

        # Check for run function
        if hasattr(module, 'run'):
            print(f"   ✅ {module_name}: Successfully imported with run() function")
        else:
            print(f"   ⚠️  {module_name}: Imported but missing run() function")

    except ModuleNotFoundError as e:
        print(f"   ❌ {module_name}: ModuleNotFoundError - {e}")
    except ImportError as e:
        print(f"   ❌ {module_name}: ImportError - {e}")
    except Exception as e:
        print(f"   ❌ {module_name}: {type(e).__name__} - {e}")

print()

# 5. Check for __pycache__
print("5. Cache Status:")
pycache = Path("modules/__pycache__")
if pycache.exists():
    cache_files = list(pycache.glob("*.pyc"))
    print(f"   Found {len(cache_files)} cached files")
    print(f"   💡 Try: rm -rf modules/__pycache__")
else:
    print(f"   No __pycache__ found")
print()

# 6. Check Streamlit cache
print("6. Streamlit Cache:")
streamlit_cache = Path.home() / ".streamlit" / "cache"
if streamlit_cache.exists():
    print(f"   ⚠️  Streamlit cache exists at: {streamlit_cache}")
    print(f"   💡 Try: rm -rf ~/.streamlit/cache")
else:
    print(f"   ✅ No Streamlit cache found")
print()

# 7. Check if sportai_main.py exists
print("7. Main Application File:")
main_file = Path("sportai_main.py")
if main_file.exists():
    print(f"   ✅ sportai_main.py exists")
    # Check if it has the load_module function
    content = main_file.read_text()
    if 'def load_module' in content:
        print(f"   ✅ load_module function found")
        if 'modules.' in content:
            print(f"   ✅ Uses 'modules.' prefix for imports")
        else:
            print(f"   ⚠️  May not be using 'modules.' prefix")
    else:
        print(f"   ❌ load_module function NOT found")
else:
    print(f"   ❌ sportai_main.py NOT FOUND")
print()

# 8. Git status
print("8. Git Status:")
try:
    import subprocess
    result = subprocess.run(['git', 'branch', '--show-current'],
                          capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        branch = result.stdout.strip()
        print(f"   Current branch: {branch}")
        if 'claude/implement-module' in branch:
            print(f"   ✅ On the correct branch")
        else:
            print(f"   ⚠️  Expected branch: claude/implement-module-011CUMYTUfkqzBSdKHCsuMfy")
    else:
        print(f"   ⚠️  Could not determine git branch")
except:
    print(f"   ⚠️  Git command failed")

print()
print("=" * 70)
print("RECOMMENDATIONS:")
print("=" * 70)

# Provide specific recommendations
recommendations = []

if not modules_path.exists():
    recommendations.append("❌ CRITICAL: modules/ directory not found! Run: git pull")

if pycache.exists():
    recommendations.append("🔧 Clear Python cache: rm -rf modules/__pycache__")

if streamlit_cache.exists():
    recommendations.append("🔧 Clear Streamlit cache: rm -rf ~/.streamlit/cache")

recommendations.append("🔧 Kill all Streamlit processes: pkill -f streamlit")
recommendations.append("🚀 Restart app: streamlit run sportai_main.py")

for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")

print()
print("Or simply run: ./restart_app.sh")
print("=" * 70)
