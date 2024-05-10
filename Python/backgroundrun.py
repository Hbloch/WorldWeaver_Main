import subprocess
import sys

def uninstall_pip():
    """ Désinstalle pip du système. """
    try:
        # Commande pour désinstaller pip
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "pip", "-y"], check=True)
        print("pip a été désinstallé avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Une erreur est survenue lors de la tentative de désinstallation de pip : {e}")

# Appel de la fonction pour désinstaller pip
uninstall_pip()
