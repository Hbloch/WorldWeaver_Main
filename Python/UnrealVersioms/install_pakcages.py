import subprocess
import json
import unreal

def get_installed_packages(python_exec):
    """Retrieve the list of installed packages using an external command prompt."""
    try:
        result = subprocess.run([python_exec, "-m", "pip", "list", "--format=json"], capture_output=True, text=True, check=True)
        if result.stdout:
            installed_packages = json.loads(result.stdout)
            unreal.log(f"Installed packages retrieved successfully.")
            return {package['name'].lower() for package in installed_packages}
        else:
            unreal.log_error("No output received from pip list command.")
            return set()
    except subprocess.CalledProcessError as e:
        unreal.log_error(f"Error fetching installed packages: {str(e)}")
        return set()

def install_packages(packages, python_exec):
    installed_packages = get_installed_packages(python_exec)
    for package in packages:
        if package.lower() not in installed_packages:
            result = subprocess.run([python_exec, "-m", "pip", "install", package], capture_output=True, text=True, check=True)
            if result.returncode == 0:
                # Re-check if the package was successfully installed
                newly_installed_packages = get_installed_packages(python_exec)
                if package.lower() in newly_installed_packages:
                    unreal.log(f"'{package}' installed successfully.")
                else:
                    unreal.log_error(f"Failed to install '{package}': Package not found after installation.")
            else:
                unreal.log_error(f"Failed to install '{package}'. Error: {result.stderr}")
        else:
            unreal.log(f"'{package}' is already installed.")
    unreal.log("Package installation completed.")


python_exec = r"C:\Program Files\Epic Games\UE_5.3\Engine\Binaries\ThirdParty\Python3\Win64\python.exe"
packages_to_install = ['geographiclib', 'requests', 'geopy', 'pyinstaller']
install_packages(packages_to_install, python_exec)
