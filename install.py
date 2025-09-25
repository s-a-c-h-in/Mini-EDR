import os
import sys
import subprocess

def install_requirements():
    requirements = [
        'psutil>=5.8.0',
        'watchdog>=2.1.0',
        'flask>=2.0.0'
    ]
    
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', req])
            print(f"✓ Installed {req}")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {req}")

def create_directories():
    dirs = ['config', 'agents', 'database', 'alerts', 'dashboard', 'logs', 'quarantine']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
        print(f"✓ Created directory: {dir_name}")

def main():
    print("🛡️ Mini EDR Installation")
    print("=" * 30)
    
    create_directories()
    install_requirements()
    
    print("\n✅ Installation complete!")
    print("Run: python main.py")

if __name__ == "__main__":
    main()
