# 🔄 Modo Incremental - Sistema de Actualización de Productos

## ¿Qué es el Modo Incremental?

El modo incremental permite actualizar la base de datos de productos sin eliminar los existentes. Solo agrega productos nuevos e ignora duplicados.

## ✨ Características

- ✅ **Preserva productos existentes**: No elimina ni sobrescribe productos ya importados
- ✅ **Detección de duplicados**: Usa el nombre del producto como identificador único
- ✅ **Reportes detallados**: Genera JSON con estadísticas de cada actualización
- ✅ **SKUs únicos**: Genera SKUs personalizados solo para productos nuevos

## 📋 Cómo Funciona

### 1. Detecta Productos Existentes
```
Carga: datos/json/productos_mercadolibre.json
Crea diccionario con nombre como clave
```

### 2. Compara con CSV
```
Lee: datos/csv/viaje_azul_productos_con_detalles.csv
Para cada producto:
  - Si existe → ignora
  - Si es nuevo → convierte y agrega
```

### 3. Genera Reporte
```
Crea: datos/json/reporte_actualizacion_YYYYMMDD_HHMMSS.json
Incluye:
  - Productos anteriores
  - Productos nuevos agregados
  - Productos ignorados (duplicados)
  - Total productos ahora
  - SKUs de nuevos productos
  - Nombres de productos ignorados
```

## 🚀 Uso

### Ejecución Manual

```bash
cd /home/clynova/proyectos/scrapping_web
source venv/bin/activate
python conversor_a_json.py
```

### Salida Esperada

```
======================================================================
🔄 CONVERSOR DE CSV A JSON - MODO INCREMENTAL
======================================================================

📋 Usando CSV con detalles completos

📂 Leyendo archivo CSV: datos/csv/viaje_azul_productos_con_detalles.csv
📊 Total de productos en CSV: 48
📋 Cargando productos existentes...
  ✅ 10 productos existentes cargados

💾 Actualizando archivo consolidado: productos_mercadolibre.json

✅ Conversión incremental completada!

📊 RESUMEN:
   • Productos anteriores: 10
   • Productos nuevos agregados: 38
   • Productos ignorados (duplicados): 10
   • Total productos ahora: 48

🆕 SKUs de productos nuevos:
   • SUB-OTRO-VAR-456
   • CAB-OTRO-VAR-789
   • KIT-OTRO-VAR-123
   ... y 35 más

📄 Reporte guardado en: reporte_actualizacion_20251210_143045.json
```

## 📊 Estructura del Reporte

```json
{
  "fecha_actualizacion": "2025-12-10 14:30:45",
  "productos_anteriores": 10,
  "productos_nuevos": 38,
  "productos_ignorados": 10,
  "total_productos": 48,
  "skus_nuevos": [
    "SUB-OTRO-VAR-456",
    "CAB-OTRO-VAR-789"
  ],
  "nombres_ignorados": [
    "Kit Cables Para Amplificador...",
    "Antena Corta Hilo Curado..."
  ]
}
```

## 🔄 Flujo de Trabajo Completo

### Para Actualizar la Tienda

1. **Scraping de nuevos productos**
   ```bash
   python scraper_mercadolibre_v2.py
   ```
   - Visita la tienda de Mercado Libre
   - Extrae todos los productos (nuevos y existentes)
   - Genera CSV actualizado

2. **Conversión incremental**
   ```bash
   python conversor_a_json.py
   ```
   - Lee productos existentes en JSON
   - Compara con CSV actualizado
   - Solo agrega productos nuevos

3. **Revisar reporte**
   - Ver `datos/json/reporte_actualizacion_YYYYMMDD_HHMMSS.json`
   - Verificar cantidad de productos nuevos
   - Revisar SKUs generados

## 🎯 Casos de Uso

### Caso 1: Primera Importación
```
Estado inicial: 0 productos
Resultado: Todos los productos del CSV se agregan como nuevos
```

### Caso 2: Actualización (sin cambios)
```
Estado inicial: 10 productos
CSV: 10 productos (mismos)
Resultado: 0 nuevos, 10 ignorados
```

### Caso 3: Actualización (con nuevos)
```
Estado inicial: 10 productos
CSV: 48 productos (10 viejos + 38 nuevos)
Resultado: 38 nuevos, 10 ignorados, total 48
```

## ⚙️ Configuración Avanzada

### Cambiar a Modo Batch (reemplazar todo)

Si necesitas reemplazar todos los productos:

1. Editar `conversor_a_json.py`
2. Cambiar línea 473:
   ```python
   # Modo incremental (actual)
   reporte = convertir_csv_a_json_incremental(...)
   
   # Cambiar a modo batch
   productos = convertir_csv_a_json(...)
   ```

### Modificar Criterio de Duplicado

Actualmente usa `nombre` del producto. Para cambiar:

```python
# En convertir_csv_a_json_incremental(), línea ~283
productos_existentes = {p['nombre']: p for p in productos_list}

# Cambiar por SKU o slug:
productos_existentes = {p['sku']: p for p in productos_list}
productos_existentes = {p['slug']: p for p in productos_list}
```

## 📁 Archivos Generados

```
datos/json/
├── productos_mercadolibre.json          # Archivo consolidado actualizado
├── reporte_actualizacion_*.json         # Reportes históricos
└── [SKU]_[slug].json                    # JSONs individuales (nuevos)
```

## ⚠️ Notas Importantes

1. **Nombres duplicados**: Si el mismo producto aparece con nombres ligeramente diferentes, se tratará como nuevo
2. **Reportes históricos**: Los reportes no se eliminan, se acumulan para historial
3. **Backup recomendado**: Hacer backup de `productos_mercadolibre.json` antes de actualizar
4. **Tiempo de ejecución**: Depende del número de productos nuevos (~1-2 seg por producto)

## 🐛 Solución de Problemas

### Error: "No se encontró ningún archivo CSV"
```bash
# Verificar que existe el CSV
ls -lh datos/csv/viaje_azul_productos_con_detalles.csv

# Si no existe, ejecutar scraper primero
python scraper_mercadolibre_v2.py
```

### Error: JSON malformado
```bash
# Validar JSON actual
python -m json.tool datos/json/productos_mercadolibre.json

# Si está corrupto, restaurar backup o regenerar
```

### Productos no se detectan como duplicados
- Verificar que los nombres sean exactamente iguales
- Revisar espacios en blanco o caracteres especiales
- Considerar usar `slug` o `sku` como criterio

## 📈 Métricas y Monitoreo

Puedes revisar el historial completo revisando todos los reportes:

```bash
ls -lht datos/json/reporte_actualizacion_*.json
```

Para ver un resumen rápido:

```bash
for f in datos/json/reporte_actualizacion_*.json; do
  echo "=== $f ==="
  jq '.fecha_actualizacion, .productos_nuevos' "$f"
done
```
