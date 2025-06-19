#!/usr/bin/env python3
"""
EconoVisionAI Launcher
Simple launcher with dependency checking and error handling
"""

import sys
import os
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again")
        return False
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = {
        'customtkinter': 'customtkinter',
        'pandas': 'pandas',
        'tkinter': 'tkinter'
    }

    missing_packages = []

    for package, import_name in required_packages.items():
        try:
            if import_name == 'tkinter':
                import tkinter
            elif import_name == 'customtkinter':
                import customtkinter
            elif import_name == 'pandas':
                import pandas
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   • {package}")
        print()
        print("📦 To install missing packages:")
        print("   pip install -r requirements.txt")
        print("   or")
        print("   ./install.sh")
        return False

    return True

def check_data_files():
    """Check if data and report files exist"""
    issues = []

    # Check directories
    if not os.path.exists("data"):
        issues.append("Missing 'data' directory")
    elif not os.listdir("data"):
        issues.append("'data' directory is empty")

    if not os.path.exists("reports"):
        issues.append("Missing 'reports' directory")
    elif not os.listdir("reports"):
        issues.append("'reports' directory is empty")

    # Check main application file
    if not os.path.exists("main.py"):
        issues.append("Missing main.py file")

    if issues:
        print("⚠️  Data file warnings:")
        for issue in issues:
            print(f"   • {issue}")
        print()
        print("ℹ️  The application will still run, but may have limited functionality")
        return False

    return True

def launch_application():
    """Launch the main application"""
    try:
        print("🚀 Launching EconoVisionAI...")

        # Import and run the main application
        from main import main
        main()

    except ImportError as e:
        print(f"❌ Error importing main application: {e}")
        print("   Please ensure main.py is in the current directory")
        return False
    except Exception as e:
        print(f"❌ Error running application: {e}")
        print("   Please check the error details above")
        return False

    return True

def main():
    """Main launcher function"""
    print("🌍 EconoVisionAI Launcher")
    print("=" * 40)

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    print("✅ Python version check passed")

    # Check dependencies
    if not check_dependencies():
        print()
        print("💡 Quick fix: Run the following command:")
        print("   pip install customtkinter pandas")
        sys.exit(1)

    print("✅ Dependencies check passed")

    # Check data files
    data_ok = check_data_files()
    if data_ok:
        print("✅ Data files check passed")

    print()

    # Launch application
    if launch_application():
        print("👋 Application closed successfully")
    else:
        print("❌ Application failed to start")
        sys.exit(1)

if __name__ == "__main__":
    main()
