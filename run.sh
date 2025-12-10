#!/bin/bash
# Script de inicio rápido para el scraper de Mercado Libre

echo "=================================================="
echo " SCRAPER DE MERCADO LIBRE - INICIO RÁPIDO"
echo "=================================================="
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ No se encontró el entorno virtual"
    echo "Creando entorno virtual..."
    python3 -m venv venv
    echo "Instalando dependencias..."
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Ejecutar scraper
echo "🚀 Ejecutando scraper..."
echo ""
python scraper_mercadolibre_v2.py

echo ""
echo "=================================================="
echo "✅ Proceso completado"
echo "=================================================="
