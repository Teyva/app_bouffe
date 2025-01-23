@echo off
setlocal enabledelayedexpansion

REM Check if utilisateurs.json exists
if not exist "utilisateurs.json" (
    echo utilisateurs.json not found. Please ensure the file exists.
    pause
    exit /b 1
)

REM Ensure a clean password input
:password_prompt
set "new_password="
set /p new_password=No admin password set. Please enter a password: 

REM Validate password input
if not defined new_password (
    echo Password cannot be empty.
    goto password_prompt
)

REM Hash the password using PowerShell
for /f "delims=" %%i in ('powershell -Command "[System.BitConverter]::ToString((New-Object Security.Cryptography.MD5CryptoServiceProvider).ComputeHash([System.Text.Encoding]::UTF8.GetBytes('%new_password%'))).Replace('-','').ToLower()"') do set "hashed_password=%%i"

REM Use PowerShell to modify the JSON file
powershell -Command "$json = Get-Content utilisateurs.json | ConvertFrom-Json; $admin = $json.utilisateurs | Where-Object { $_.role -eq 'admin' }; $admin.password = '%hashed_password%'; $json | ConvertTo-Json -Depth 10 | Set-Content utilisateurs.json"

echo Admin password set successfully in utilisateurs.json!

REM Create desktop shortcut
set "script_path=%cd%\main.py"
set "shortcut_path=%userprofile%\Desktop\Launch App.lnk"

powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%shortcut_path%'); $Shortcut.TargetPath = 'python.exe'; $Shortcut.Arguments = '%script_path%'; $Shortcut.WorkingDirectory = '%cd%'; $Shortcut.Save()"

echo Shortcut created on your desktop to launch the app.
pause
