"""
Verify all SportAI modules can be loaded
This script mimics exactly how sportai_main.py loads modules
"""

import sys
import importlib
from pathlib import Path

# Add current directory to path (same as sportai_main.py does)
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("SportAI Module Verification")
print("=" * 70)
print()

# All modules that should be available
all_modules = {
    'dashboard': '📊 Dashboard',
    'ai_scheduling': '🤖 AI Scheduling',
    'dynamic_pricing': '💰 Dynamic Pricing',
    'sponsorship_optimizer': '🤝 Sponsorship',
    'membership_manager': '👥 Memberships',
    'facility_ops': '🏢 Facility Ops',
    'grant_builder': '📄 Grants',
    'board_governance': '⚖️ Governance',
    'event_manager': '📅 Events',
    'reports': '📈 Reports',
    'sponsor_portal': '🎯 Sponsor Portal',
    'member_portal': '🎫 Member Portal',
    'bookings': '📅 Bookings'
}

success_count = 0
fail_count = 0
errors = []

for module_name, display_name in all_modules.items():
    try:
        # This is EXACTLY how sportai_main.py loads modules
        module_path = f"modules.{module_name}"
        module = importlib.import_module(module_path)

        # Check if run function exists
        if not hasattr(module, 'run'):
            print(f"❌ {display_name}: Module loaded but missing run() function")
            fail_count += 1
            errors.append(f"{module_name}: Missing run() function")
        else:
            print(f"✅ {display_name}: OK")
            success_count += 1

    except ModuleNotFoundError as e:
        print(f"❌ {display_name}: Module not found")
        fail_count += 1
        errors.append(f"{module_name}: {str(e)}")

    except Exception as e:
        print(f"❌ {display_name}: Error - {str(e)}")
        fail_count += 1
        errors.append(f"{module_name}: {str(e)}")

print()
print("=" * 70)
print(f"Results: {success_count} ✅ | {fail_count} ❌")
print("=" * 70)

if fail_count > 0:
    print()
    print("ERRORS:")
    for error in errors:
        print(f"  • {error}")
    print()
    print("⚠️  Some modules failed to load!")
    print("💡 Try running: ./restart_app.sh")
    sys.exit(1)
else:
    print()
    print("🎉 All modules loaded successfully!")
    print()
    print("You can now run: streamlit run sportai_main.py")
    sys.exit(0)
