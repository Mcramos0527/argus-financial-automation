@echo off
:: ============================================================
:: ARGUS — Script de compilación para Windows
:: Powered by McFlow
::
:: Uso: doble clic en build.bat
:: Genera: dist/ARGUS.exe  (ejecutable standalone)
::         installer_output/ARGUS_Setup_v1.0.0.exe  (instalador)
:: ============================================================

echo.
echo  ╔══════════════════════════════════════════╗
echo  ║   ARGUS — Build Script  ^|  McFlow        ║
echo  ╚══════════════════════════════════════════╝
echo.

:: ── 1. Verificar Python ──────────────────────────────────────────────────────
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Python no encontrado. Instalá Python 3.10+
    pause
    exit /b 1
)
echo  [OK] Python detectado

:: ── 2. Instalar dependencias ─────────────────────────────────────────────────
echo  Instalando dependencias...
pip install -r requirements.txt --quiet
pip install pyinstaller --quiet
echo  [OK] Dependencias instaladas

:: ── 3. Limpiar builds anteriores ─────────────────────────────────────────────
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "ARGUS.spec" del "ARGUS.spec"
echo  [OK] Carpetas anteriores limpiadas

:: ── 4. Compilar con PyInstaller ──────────────────────────────────────────────
echo.
echo  Compilando ARGUS.exe...
echo  (Esto puede tardar 1-2 minutos)
echo.

pyinstaller ^
    --onefile ^
    --windowed ^
    --name "ARGUS" ^
    --icon "icon.ico" ^
    --add-data "app;app" ^
    --hidden-import "openpyxl" ^
    --hidden-import "openpyxl.styles" ^
    --hidden-import "openpyxl.utils" ^
    --hidden-import "pandas" ^
    main.py

if %errorlevel% neq 0 (
    echo.
    echo  [ERROR] La compilación falló. Revisá los errores arriba.
    pause
    exit /b 1
)

echo.
echo  [OK] ARGUS.exe generado en: dist\ARGUS.exe
echo.

:: ── 5. Generar instalador con Inno Setup (si está instalado) ─────────────────
set INNO="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if exist %INNO% (
    echo  Generando instalador Windows...
    %INNO% installer.iss
    echo  [OK] Instalador generado en: installer_output\
) else (
    echo  [INFO] Inno Setup no encontrado — saltando generación de instalador.
    echo         Descargalo de: https://jrsoftware.org/isinfo.php
    echo         Luego abrí installer.iss con Inno Setup Compiler.
)

echo.
echo  ╔══════════════════════════════════════════════════════╗
echo  ║  BUILD COMPLETADO                                    ║
echo  ║                                                      ║
echo  ║  Ejecutable:  dist\ARGUS.exe                         ║
echo  ║  Instalador:  installer_output\ARGUS_Setup_v1.0.0.exe║
echo  ╚══════════════════════════════════════════════════════╝
echo.
pause
