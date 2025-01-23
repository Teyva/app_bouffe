import os
import sys
import platform
from pathlib import Path

def create_shortcut(target, shortcut_name):
    """Crée un raccourci sur le bureau ou à un emplacement choisi."""
    if platform.system() == "Windows":
        import winshell
        from win32com.client import Dispatch

        # Récupérer le chemin du bureau
        desktop = winshell.desktop()

        # Chemin complet du raccourci
        shortcut_path = os.path.join(desktop, f"{shortcut_name}.lnk")

        # Créer un raccourci
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = target
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.IconLocation = target
        shortcut.save()

        print(f"Raccourci créé : {shortcut_path}")

    elif platform.system() == "Linux":
        # Récupérer le chemin du bureau
        desktop = str(Path.home() / "Bureau")

        # Chemin complet du raccourci
        shortcut_path = os.path.join(desktop, f"{shortcut_name}.desktop")

        # Créer un fichier .desktop
        with open(shortcut_path, "w") as f:
            f.write(f"""[Desktop Entry]
Version=1.0
Type=Application
Name={shortcut_name}
Exec=python3 {target}
Icon=application-python
Terminal=false
""")

        # Rendre exécutable
        os.chmod(shortcut_path, 0o755)
        print(f"Raccourci créé : {shortcut_path}")

    elif platform.system() == "Darwin":  # macOS
        print("La création de raccourcis sur macOS n'est pas encore prise en charge automatiquement.")
    else:
        print("Système non pris en charge.")

if __name__ == "__main__":
    # Cible (script principal à lancer)
    target_script = os.path.abspath("main.py")

    # Nom du raccourci
    shortcut_name = "Application nouriture"

    # Créer le raccourci
    create_shortcut(target_script, shortcut_name)
