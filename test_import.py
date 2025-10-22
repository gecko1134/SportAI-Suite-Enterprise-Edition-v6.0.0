"""
Simple test without Streamlit dependency
Tests the actual import mechanism that sportai_main.py uses
"""

import sys
import os
from pathlib import Path

# Ensure we're in the right directory
os.chdir('/home/user/SportAI-Suite-Enterprise-Edition-v6.0.0')
sys.path.insert(0, '/home/user/SportAI-Suite-Enterprise-Edition-v6.0.0')

print("Testing module imports WITHOUT Streamlit...")
print("=" * 70)

# Test 1: Can we import the modules package?
try:
    import modules
    print("✅ Step 1: 'import modules' succeeded")
except Exception as e:
    print(f"❌ Step 1 FAILED: {e}")
    sys.exit(1)

# Test 2: Try importing facility_ops specifically
try:
    from modules import facility_ops
    print("✅ Step 2: 'from modules import facility_ops' succeeded")
except Exception as e:
    print(f"❌ Step 2 FAILED: {e}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Check if run function exists
try:
    if hasattr(facility_ops, 'run'):
        print("✅ Step 3: facility_ops.run function exists")
    else:
        print("❌ Step 3 FAILED: No run() function in facility_ops")
        print(f"   Available attributes: {dir(facility_ops)}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Step 3 FAILED: {e}")
    sys.exit(1)

# Test 4: Try the exact import method sportai_main.py uses
try:
    import importlib
    module_path = "modules.facility_ops"
    module = importlib.import_module(module_path)
    print("✅ Step 4: importlib.import_module('modules.facility_ops') succeeded")

    if hasattr(module, 'run'):
        print("✅ Step 5: Module has run() function")
    else:
        print("❌ Step 5 FAILED: No run() function")
        sys.exit(1)

except Exception as e:
    print(f"❌ Step 4 FAILED: {e}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 70)
print("✅ ALL TESTS PASSED!")
print()
print("The modules CAN be imported successfully.")
print()
print("If you're still seeing 'not yet implemented', the issue is:")
print("1. Streamlit is caching the old version")
print("2. You need to COMPLETELY stop and restart Streamlit")
print()
print("Try this:")
print("  1. Find the terminal running Streamlit")
print("  2. Press Ctrl+C to stop it")
print("  3. Wait 3-5 seconds")
print("  4. Run: streamlit run sportai_main.py")
print("  5. In browser: Ctrl+Shift+R (hard refresh)")
