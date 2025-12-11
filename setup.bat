@echo off
setlocal enabledelayedexpansion

echo ╔═══════════════════════════════════════════════════════════╗
echo ║             XTrace - Final Installation Script            ║
echo ╚═══════════════════════════════════════════════════════════╝
echo.
echo This script will make the 'xtrace' command available system-wide
echo for the current user by doing the following:
echo 1. Creating a safe directory at '%%LOCALAPPDATA%%\scripts'.
echo 2. Placing a launcher script there.
echo 3. Safely adding that directory to your user PATH.
echo.

:CONFIRM
set /P "CHOICE=Do you want to continue? (Y/N): "
if /I "%CHOICE%" == "Y" goto :INSTALL
if /I "%CHOICE%" == "N" goto :CANCEL
echo Invalid choice.
goto :CONFIRM

:INSTALL
:: --- 1. Define and create the installation directory ---
set "INSTALL_DIR=%LOCALAPPDATA%\scripts"
echo.
echo [*] Ensuring installation directory exists at %INSTALL_DIR%...
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo    Directory created.
) else (
    echo    Directory already exists.
)

:: --- 2. Safely add the directory to the user's PATH ---
echo.
echo [*] Checking user PATH for installation directory...
powershell -NoProfile -Command "& {
    $pathName = 'Path';
    $pathType = [System.EnvironmentVariableTarget]::User;
    $currentPath = [System.Environment]::GetEnvironmentVariable($pathName, $pathType);
    $installDir = '%INSTALL_DIR%';
    if ($currentPath -notlike '*' + $installDir + '*') {
        echo '    Directory not in PATH. Adding it...';
        $newPath = $currentPath + ';' + $installDir;
        [System.Environment]::SetEnvironmentVariable($pathName, $newPath, $pathType);
        echo '    PATH updated successfully.';
    } else {
        echo '    Directory already in PATH. No changes needed.';
    }
}"

:: --- 3. Generate the launcher script ---
echo.
echo [*] Generating 'xtrace.bat' launcher in the installation directory...
set "PROJECT_DIR=%cd%"
(
    echo @echo off
    echo setlocal enabledelayedexpansion
    echo.
    echo :: This is an auto-generated launcher for XTrace. Do not edit.
    echo.
    echo set "PROJECT_DIR=%PROJECT_DIR%"
    echo set "VENV_DIR=%%PROJECT_DIR%%\.venv"
    echo set "PYTHON_EXE=%%VENV_DIR%%\Scripts\python.exe"
    echo.
    echo if not exist "%%PYTHON_EXE%%" (
    echo     echo [!] First-time setup for XTrace. This may take a moment...
    echo     echo [*] Creating virtual environment in %%PROJECT_DIR%%...
    echo     python -m venv "%%VENV_DIR%%"
    echo     if !errorlevel! neq 0 (
    echo         echo [!] ERROR: Failed to create virtual environment.
    echo         pause
    echo         exit /b 1
    echo     )
    echo.
    echo     echo [*] Installing dependencies...
    echo     "%%PYTHON_EXE%%" -m pip install -e "%%PROJECT_DIR%%"
    echo     if !errorlevel! neq 0 (
    echo         echo [!] ERROR: Failed to install dependencies.
    echo         pause
    echo         exit /b 1
    echo     )
    echo     echo [✓] Setup complete!
    echo )
    echo.
    echo "%%PYTHON_EXE%%" "%%PROJECT_DIR%%\xtrace.py" %%*
    echo.
    echo endlocal
) > "%INSTALL_DIR%\xtrace.bat"
echo    Launcher created.

echo.
echo ╔═════════════════════════════════════════════════════════════════════════════╗
echo ║ [✓] Installation Complete!                                                ║
echo ║                                                                             ║
echo ║ IMPORTANT: You must CLOSE and REOPEN ALL TERMINALS for the 'xtrace' command ║
echo ║ to be available everywhere.                                                 ║
echo ║                                                                             ║
echo ╚═════════════════════════════════════════════════════════════════════════════╝
echo.
goto :END

:CANCEL
echo.
echo Installation cancelled by user.
echo.

:END
pause
