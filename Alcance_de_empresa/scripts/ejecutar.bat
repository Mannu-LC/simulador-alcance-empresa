@echo off
REM Script para instalar dependencias y ejecutar la aplicación
REM Windows - PowerShell

echo ========================================
echo INSTALACION DE APLICACION - DIFUSION
echo ========================================
echo.

echo [1/3] Verificando Python...
python --version
if errorlevel 1 (
    echo ERROR: Python no está instalado o no está en el PATH
    echo Descarga Python desde https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo [2/3] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: No se pudieron instalar las dependencias
    pause
    exit /b 1
)

echo.
echo [3/3] Iniciando aplicación...
echo.
python aplicacion_difusion_empresa.py

pause
