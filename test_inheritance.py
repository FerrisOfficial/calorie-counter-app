#!/usr/bin/env python3
"""
Simple test script to verify SetTargetOption class loads without metaclass conflicts
"""

try:
    print("Testing SetTargetOption import...")
    from src.SettingsDisplay.SetTargetOption.SetTargetOption import SetTargetOption
    print("✓ SetTargetOption imported successfully!")
    
    print("Testing class instantiation...")
    option = SetTargetOption()
    print("✓ SetTargetOption instantiated successfully!")
    
    print("Testing methods...")
    value = option.get_option_value()
    print(f"✓ Current target value: {value}")
    
    option.set_option_value(2500)
    new_value = option.get_option_value()
    print(f"✓ Updated target value: {new_value}")
    
    print("\n✅ All tests passed! Metaclass conflict resolved.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
