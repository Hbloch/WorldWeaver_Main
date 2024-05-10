import subprocess
import sys
import os

def find_python_path():
    """ Tente de trouver un chemin alternatif pour Python si celui actuel est l'environnement Unreal. """
    # Heuristique simple : vérifier si 'Unreal' est dans le chemin
    current_executable = sys.executable
    if 'Unreal' in current_executable:
        # Liste des chemins communs pour Python
        common_paths = [
            'C:\\Python39\\python.exe',
            'C:\\Python38\\python.exe',
            'C:\\Python37\\python.exe',
            'C:\\Python36\\python.exe',
            '/usr/bin/python3',
            '/usr/local/bin/python3'
        ]
        for path in common_paths:
            if os.path.exists(path):
                return path
        print("Aucun environnement Python alternatif trouvé. Utilisation de l'environnement actuel.")
    return current_executable

def check_pip_installed(python_path):
    """ Vérifie si pip est installé et retourne sa version. """
    try:
        result = subprocess.run([python_path, "-m", "pip", "--version"], capture_output=True, text=True, check=True)
        pip_version = result.stdout.split()[1]
        return True, pip_version
    except subprocess.CalledProcessError:
        return False, None

def install_or_upgrade_pip(python_path, get_pip_script_path):
    pip_installed, pip_version = check_pip_installed(python_path)
    
    if not pip_installed:
        print("pip n'est pas installé. Installation en cours...")
        try:
            subprocess.run([python_path, get_pip_script_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Erreur lors de l'installation de pip : {e}")
    else:
        min_pip_version = "24.0"
        if pip_version < min_pip_version:
            print(f"Version actuelle de pip ({pip_version}) inférieure à {min_pip_version}. Mise à niveau en cours...")
            try:
                subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Erreur lors de la mise à niveau de pip : {e}")
        else:
            print(f"Version actuelle de pip ({pip_version}) est {min_pip_version} ou supérieure. Aucune action requise.")

python_path = find_python_path()  # Détection automatique de l'environnement Python
get_pip_script_path = os.path.join("C:", "WorldWeaver_Main", "WorldWeaver_Main", "Pythonget-pip.py")

install_or_upgrade_pip(python_path, get_pip_script_path)
