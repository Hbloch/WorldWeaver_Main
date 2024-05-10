import subprocess
import unreal

def parse_version(version_string):
    """Parse the version string into a tuple of integers."""
    return tuple(map(int, version_string.split('.')))

def check_pip_installed(python_exec):
    """Check if pip is installed and return its version."""
    try:
        command = [python_exec, "-m", "pip", "--version"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        pip_version = result.stdout.split()[1]
        unreal.log(f"pip version found: {pip_version}")
        return True, parse_version(pip_version)
    except subprocess.CalledProcessError as e:
        unreal.log_error(f"Error checking pip version: {e}")
        return False, None

def install_or_upgrade_pip(get_pip_script_path, python_exec):
    pip_installed, pip_version = check_pip_installed(python_exec)
    
    try:
        if not pip_installed:
            unreal.log("pip is not installed. Installing now...")
            subprocess.run([python_exec, get_pip_script_path], check=True)
            pip_installed, _ = check_pip_installed(python_exec)
            if pip_installed:
                unreal.log("pip installed successfully.")
            else:
                unreal.log_error("Failed to install pip.")
        elif pip_version < parse_version("24.0"):
            unreal.log("Upgrading pip...")
            subprocess.run([python_exec, "-m", "pip", "install", "--upgrade", "pip"], check=True)
            _, new_pip_version = check_pip_installed(python_exec)
            if new_pip_version >= parse_version("24.0"):
                unreal.log(f"pip upgraded successfully to version {'.'.join(map(str, new_pip_version))}.")
            else:
                unreal.log_error("Failed to upgrade pip.")
        else:
            unreal.log(f"Current version of pip ({'.'.join(map(str, pip_version))}) is 24.0 or higher. No action required.")
    except Exception as e:
        unreal.log_error(f"An error occurred during pip installation or upgrade: {str(e)}")

python_exec = r"C:\Program Files\Epic Games\UE_5.3\Engine\Binaries\ThirdParty\Python3\Win64\python.exe"
get_pip_script_path = r"C:\WorldWeaver_Main\WorldWeaver_Main\Python\get-pip.py"
install_or_upgrade_pip(get_pip_script_path, python_exec)
