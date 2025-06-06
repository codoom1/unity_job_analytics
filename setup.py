#!/usr/bin/env python3
"""
Setup script for SLURM Job Analytics Project
"""

import subprocess
import sys
import os

def install_requirements():
    """Install requirements with specific versions to avoid conflicts"""
    requirements = [
        "duckdb>=0.8.0",
        "pandas>=1.5.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "streamlit>=1.28.0",
        "fire==0.4.0",  # Pin to avoid Inspector.__init__ issue
        "numpy>=1.21.0"
    ]
    
    print("Installing requirements...")
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
            print(f"✅ Installed {req}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {req}")
            return False
    
    return True

def setup_paths():
    """Add src to Python path for imports"""
    src_path = os.path.join(os.path.dirname(__file__), "src")
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

def main():
    """Main setup function"""
    print("🚀 Setting up SLURM Job Analytics Project...")
    
    if not install_requirements():
        print("❌ Setup failed during requirements installation")
        return 1
    
    setup_paths()
    
    print("✅ Setup complete!")
    print("\n📖 Next steps:")
    print("1. Run the dashboard: cd src/dashboard && streamlit run app.py")
    print("2. Try command line tools: cd src/analytics && python gpu_metrics.py waittime")
    print("3. Generate emails: cd src/outreach && python email_outreach.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
