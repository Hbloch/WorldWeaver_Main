import subprocess

scripts = ["install_packages.py", "heightmaps_downloads.py", "ImageRescalerv3.py"]

for script in scripts:
    subprocess.run(["python", script])

