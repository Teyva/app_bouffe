@echo off
:: Titre de la fenêtre
title Configuration de l'Application CEGP

:: Afficher un message d'information
echo =====================================
echo   Configuration de l'Application
echo =====================================
echo.

:: Définir les chemins
set PYTHON_PATH=C:\Users\%USERNAME%\anaconda3\python.exe
set SCRIPT_PATH=%~dp0main.py
set SHORTCUT_SCRIPT=%~dp0create_shortcut.py

:: Vérifier que Python est installé
echo Vérification de l'installation de Python...
"%PYTHON_PATH%" --version >nul 2>&1
if errorlevel 1 (
    echo Erreur : Python n'est pas installé ou le chemin est incorrect.
    pause
    exit /b
)

:: Installer les dépendances
echo Installation des dépendances...
"%PYTHON_PATH%" -m pip install -r "%~dp0requi.txt" --quiet
if errorlevel 1 (
    echo Erreur : Impossible d'installer les dépendances.
    pause
    exit /b
)

:: Créer le raccourci sur le bureau
echo Création d'une icône sur le bureau...
"%PYTHON_PATH%" "%SHORTCUT_SCRIPT%"
if errorlevel 1 (
    echo Erreur : Impossible de créer l'icône.
    pause
    exit /b
)

:: Lancer le programme une fois la configuration terminée
echo Lancement de l'application...
"%PYTHON_PATH%" "%SCRIPT_PATH%"
if errorlevel 1 (
    echo Erreur : Impossible de lancer l'application.
    pause
    exit /b
)

echo.
echo =====================================
echo   Configuration terminée !
echo =====================================
pause
