"""Test script to verify all modules can be imported"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

modules_to_test = [
    'dashboard',
    'ai_scheduling',
    'dynamic_pricing',
    'sponsorship_optimizer',
    'membership_manager',
    'facility_ops',
    'grant_builder',
    'board_governance',
    'event_manager',
    'reports',
    'sponsor_portal',
    'member_portal',
    'bookings'
]

print("Testing module imports...")
print("=" * 50)

failed = []
succeeded = []

for module_name in modules_to_test:
    try:
        module_path = f"modules.{module_name}"
        module = __import__(module_path, fromlist=[module_name])

        # Check if run function exists
        if hasattr(module, 'run'):
            succeeded.append(module_name)
            print(f"✓ {module_name}: OK")
        else:
            failed.append(f"{module_name}: Missing run() function")
            print(f"✗ {module_name}: Missing run() function")

    except Exception as e:
        failed.append(f"{module_name}: {str(e)}")
        print(f"✗ {module_name}: {str(e)}")

print("=" * 50)
print(f"\nResults: {len(succeeded)} succeeded, {len(failed)} failed")

if failed:
    print("\nFailed modules:")
    for f in failed:
        print(f"  - {f}")
else:
    print("\n✅ All modules imported successfully!")
