#!/bin/bash
# Script para ejecutar el workflow completo de scraping y conversión

set -e  # Salir si hay errores

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║          WORKFLOW COMPLETO: SCRAPING → CSV → JSON                      ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Entorno virtual no encontrado. Creándolo...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo -e "${BLUE}✓ Activando entorno virtual...${NC}"
    source venv/bin/activate
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo -e "${GREEN}1️⃣  PASO 1: SCRAPING DE MERCADO LIBRE${NC}"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Preguntar al usuario qué tipo de scraping quiere
echo "Selecciona el tipo de scraping:"
echo "  1) Prueba rápida (3 productos) - ~1 minuto"
echo "  2) Prueba mediana (10 productos) - ~5 minutos"
echo "  3) Scraping completo (48 productos) - ~20 minutos"
echo ""
read -p "Opción [1-3]: " opcion

case $opcion in
    1)
        echo -e "${BLUE}Ejecutando prueba rápida...${NC}"
        python test_detalles.py
        CSV_FILE="datos/csv/viaje_azul_productos_con_detalles.csv"
        ;;
    2)
        echo -e "${BLUE}Ejecutando prueba mediana...${NC}"
        python scraper_con_detalles_limitado.py
        CSV_FILE="datos/csv/viaje_azul_productos_con_detalles.csv"
        ;;
    3)
        echo -e "${BLUE}Ejecutando scraping completo...${NC}"
        python scraper_mercadolibre_v2.py
        CSV_FILE="datos/csv/viaje_azul_productos_con_detalles.csv"
        ;;
    *)
        echo -e "${YELLOW}Opción inválida. Usando prueba rápida.${NC}"
        python test_detalles.py
        CSV_FILE="datos/csv/viaje_azul_productos_con_detalles.csv"
        ;;
esac

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo -e "${GREEN}2️⃣  PASO 2: ORGANIZACIÓN DE DATOS${NC}"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Crear carpetas si no existen
mkdir -p datos/{csv,imagenes,json}

# Copiar archivos CSV
echo -e "${BLUE}Copiando archivos CSV...${NC}"
cp -f *.csv datos/csv/ 2>/dev/null || true

# Copiar imágenes
if [ -d "imagenes_mercadolibre" ]; then
    echo -e "${BLUE}Copiando imágenes...${NC}"
    cp -rf imagenes_mercadolibre/* datos/imagenes/ 2>/dev/null || true
fi

# Contar archivos
CSV_COUNT=$(ls datos/csv/*.csv 2>/dev/null | wc -l)
IMG_COUNT=$(ls datos/imagenes/*.jpg 2>/dev/null | wc -l)

echo -e "${GREEN}✓ CSV copiados: $CSV_COUNT${NC}"
echo -e "${GREEN}✓ Imágenes copiadas: $IMG_COUNT${NC}"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo -e "${GREEN}3️⃣  PASO 3: CONVERSIÓN A JSON${NC}"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

echo -e "${BLUE}Convirtiendo CSV a JSON según modelo de productos...${NC}"
python conversor_a_json.py

echo ""
echo "═══════════════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✅ WORKFLOW COMPLETADO${NC}"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Mostrar resumen
JSON_COUNT=$(ls datos/json/*.json 2>/dev/null | wc -l)

echo "📊 RESUMEN:"
echo "   • Archivos CSV: $CSV_COUNT"
echo "   • Imágenes: $IMG_COUNT"
echo "   • Archivos JSON: $JSON_COUNT"
echo ""
echo "📁 Archivos generados en:"
echo "   • CSV: datos/csv/"
echo "   • Imágenes: datos/imagenes/"
echo "   • JSON: datos/json/"
echo ""
echo -e "${GREEN}🎯 JSON principal: datos/json/productos_mercadolibre.json${NC}"
echo ""
echo "Para importar a MongoDB:"
echo "  const productos = require('./datos/json/productos_mercadolibre.json');"
echo "  await Product.insertMany(productos);"
echo ""
echo "╔════════════════════════════════════════════════════════════════════════╗"
echo "║                    ¡Proceso completado con éxito! 🎉                   ║"
echo "╚════════════════════════════════════════════════════════════════════════╝"
