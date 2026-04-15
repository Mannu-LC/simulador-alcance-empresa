#!/bin/bash
# Script para instalar dependencias y ejecutar la aplicación
# Linux/Mac

echo "========================================"
echo "INSTALACION DE APLICACION - DIFUSION"
echo "========================================"
echo ""

echo "[1/3] Verificando Python..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python no está instalado"
    echo "Instala Python3 usando: sudo apt-get install python3 python3-pip"
    exit 1
fi

echo ""
echo "[2/3] Instalando dependencias..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: No se pudieron instalar las dependencias"
    exit 1
fi

echo ""
echo "[3/3] Iniciando aplicación..."
echo ""
python3 aplicacion_difusion_empresa.py
