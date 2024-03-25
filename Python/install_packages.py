import subprocess
import sys
import pkg_resources

def install_packages(packages):
    print("PACKAGE INSTALLATION")
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    for package in packages:
        if package not in installed_packages:
            print(f"Installation du package '{package}'...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"'{package}' installé avec succès.")
        
    print("PACKAGE INSTALLATION COMPLETED")

packages_to_install = ['requests', 'alive_progress', 'colorama', 'geopy', 'opencv-python', 'opencv-contrib-python', 'pyinstaller']

install_packages(packages_to_install)
