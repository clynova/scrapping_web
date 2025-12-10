# 📤 Importador de Productos al Servidor

Sistema para importar productos JSON al servidor mediante peticiones POST a la API REST.

## 📋 Índice

- [Características](#características)
- [Configuración](#configuración)
- [Uso](#uso)
- [Modos de Operación](#modos-de-operación)
- [Manejo de Errores](#manejo-de-errores)
- [Reportes](#reportes)

## ✨ Características

- ✅ Importación automática de todos los productos
- ✅ Autenticación con Bearer Token (JWT)
- ✅ Detección de duplicados
- ✅ Reintentos automáticos en caso de timeout
- ✅ Delay configurable entre peticiones
- ✅ Reportes detallados de importación
- ✅ Importación individual de productos
- ✅ Verificación previa del servidor
- ✅ Manejo robusto de errores

## ⚙️ Configuración

### 1. Editar Configuración del Servidor

Edita el archivo [config_servidor.py](config_servidor.py):

```python
# URL del servidor
API_URL = "http://localhost:4000/api/products"

# Token de autenticación (JWT)
AUTH_TOKEN = "tu_token_aqui"

# Configuración de reintentos
MAX_REINTENTOS = 3

# Delay entre productos (segundos)
DELAY_ENTRE_PRODUCTOS = 0.5

# Timeout para peticiones (segundos)
TIMEOUT = 30
```

### 2. Verificar Servidor Corriendo

Asegúrate de que tu servidor esté corriendo en `http://localhost:4000`:

```bash
# Ejemplo con curl
curl http://localhost:4000

# Ejemplo con navegador
# Abrir: http://localhost:4000
```

## 🚀 Uso

### Modo 1: Importar Todos los Productos

Importa todos los productos desde `datos/json/productos_mercadolibre.json`:

```bash
cd /home/clynova/proyectos/scrapping_web
source venv/bin/activate
python importar_a_servidor.py
```

**Salida esperada:**

```
======================================================================
📤 IMPORTADOR DE PRODUCTOS AL SERVIDOR
======================================================================

🔍 Verificando servidor: http://localhost:4000/api/products
✓ Servidor accesible

📂 Cargando productos desde: datos/json/productos_mercadolibre.json
✓ 10 productos cargados

======================================================================
Iniciando importación...
======================================================================

[1/10] Kit Cables Para Amplificador Betensh 1500 Watts...
  SKU: KIT-OTRO-VAR-248
  ✓ Producto creado exitosamente

[2/10] Antena Corta Hilo Curado Moto Retractil Corta P...
  SKU: ANT-OTRO-VAR-122
  ✓ Producto creado exitosamente

...

======================================================================
📊 RESUMEN DE IMPORTACIÓN
======================================================================
✅ Productos importados exitosamente: 10
⚠️  Productos duplicados (ya existían): 0
❌ Productos con errores: 0
📦 Total procesados: 10
⏱️  Tiempo total: 15.45 segundos
======================================================================

📄 Reporte guardado en: reporte_importacion_20251210_143500.json

======================================================================
✅ IMPORTACIÓN COMPLETADA
======================================================================
```

### Modo 2: Importar un Producto Individual

Importa un producto específico desde un archivo JSON individual:

```bash
python importar_a_servidor.py datos/json/KIT-OTRO-VAR-248_kit-cables-para-amplificador.json
```

**Salida esperada:**

```
📤 Importando producto desde: datos/json/KIT-OTRO-VAR-248_kit-cables-para-amplificador.json
Nombre: Kit Cables Para Amplificador Betensh 1500 Watts Subwoofer RCA Rojo/Azul
SKU: KIT-OTRO-VAR-248
✓ Producto creado exitosamente
```

## 🔄 Modos de Operación

### 1. Importación Completa

Procesa todos los productos del archivo consolidado:

```bash
python importar_a_servidor.py
```

- Lee: `datos/json/productos_mercadolibre.json`
- Importa: Todos los productos uno por uno
- Genera: Reporte completo en `datos/json/reporte_importacion_*.json`

### 2. Importación Individual

Procesa un producto específico:

```bash
python importar_a_servidor.py <archivo_producto.json>
```

- Lee: El archivo JSON especificado
- Importa: Solo ese producto
- No genera reporte

## 🛡️ Manejo de Errores

El importador maneja diferentes tipos de errores:

### Error 401: Autenticación

```
❌ Error de autenticación - Token inválido o expirado
```

**Solución:**
- Obtén un nuevo token del servidor
- Actualiza `config_servidor.py` con el nuevo token

### Error 409: Duplicado

```
⚠ Producto ya existe (duplicado)
```

**Solución:**
- Normal si el producto ya fue importado
- Se registra en el reporte como duplicado

### Error 400: Datos Inválidos

```
❌ Datos inválidos: [mensaje de error del servidor]
```

**Solución:**
- Verifica que el JSON del producto sea válido
- Revisa el mensaje de error específico
- Corrige el formato en el conversor

### Error de Conexión

```
❌ Error de conexión - Verifica que el servidor esté corriendo
```

**Solución:**
- Asegúrate de que el servidor esté corriendo
- Verifica la URL en `config_servidor.py`
- Comprueba el puerto (4000 por defecto)

### Timeout

```
❌ Timeout - Servidor no responde
```

**Solución:**
- El script reintenta automáticamente (máx 3 veces)
- Si persiste, verifica la conectividad del servidor
- Aumenta `TIMEOUT` en `config_servidor.py`

## 📊 Reportes

### Estructura del Reporte

Cada importación genera un reporte JSON:

```json
{
  "fecha_importacion": "2025-12-10 14:35:00",
  "servidor": "http://localhost:4000/api/products",
  "total_productos": 10,
  "exitosos": 10,
  "duplicados": 0,
  "fallidos": 0,
  "tiempo_segundos": 15.45,
  "productos_exitosos": [
    {
      "sku": "KIT-OTRO-VAR-248",
      "nombre": "Kit Cables Para Amplificador..."
    }
  ],
  "productos_fallidos": [],
  "productos_duplicados": []
}
```

### Ubicación de Reportes

Los reportes se guardan en:

```
datos/json/reporte_importacion_YYYYMMDD_HHMMSS.json
```

### Ver Reportes

```bash
# Listar reportes de importación
ls -lht datos/json/reporte_importacion_*.json

# Ver contenido de un reporte
cat datos/json/reporte_importacion_20251210_143500.json | jq

# Ver solo el resumen
jq '{fecha: .fecha_importacion, exitosos: .exitosos, duplicados: .duplicados, fallidos: .fallidos}' datos/json/reporte_importacion_20251210_143500.json
```

## 🔧 Configuración Avanzada

### Cambiar Delay Entre Productos

Si el servidor se satura, aumenta el delay:

```python
# config_servidor.py
DELAY_ENTRE_PRODUCTOS = 1.0  # 1 segundo entre cada producto
```

### Cambiar Número de Reintentos

```python
# config_servidor.py
MAX_REINTENTOS = 5  # 5 reintentos en caso de timeout
```

### Cambiar Timeout

```python
# config_servidor.py
TIMEOUT = 60  # 60 segundos de timeout por petición
```

## 🎯 Casos de Uso

### Caso 1: Primera Importación

```bash
# 1. Scraping de productos
python scraper_mercadolibre_v2.py

# 2. Conversión a JSON
python conversor_a_json.py

# 3. Importación al servidor
python importar_a_servidor.py
```

**Resultado:** Todos los productos se importan como nuevos

### Caso 2: Actualización con Productos Nuevos

```bash
# 1. Scraping (incluye nuevos productos)
python scraper_mercadolibre_v2.py

# 2. Conversión incremental (solo agrega nuevos)
python conversor_a_json.py

# 3. Importación al servidor
python importar_a_servidor.py
```

**Resultado:** 
- Productos nuevos: se importan
- Productos existentes: se marcan como duplicados

### Caso 3: Re-importar un Producto Específico

Si necesitas actualizar un producto específico:

```bash
# Importar solo ese producto
python importar_a_servidor.py datos/json/KIT-OTRO-VAR-248_kit-cables.json
```

**Nota:** Si el producto ya existe, el servidor puede rechazarlo (409).

## 🔍 Verificación

### Verificar Token Válido

```bash
curl -H "Authorization: Bearer TU_TOKEN" http://localhost:4000/api/products
```

Si el token es válido, deberías ver una respuesta exitosa.

### Verificar Producto Importado

```bash
# Obtener todos los productos
curl http://localhost:4000/api/products

# Buscar por SKU
curl http://localhost:4000/api/products?sku=KIT-OTRO-VAR-248
```

## ⚠️ Notas Importantes

1. **Token Expiration**: El token JWT tiene una fecha de expiración. Si obtienes error 401, necesitas un nuevo token.

2. **Duplicados**: El servidor debe manejar duplicados. Si no, los productos se pueden duplicar en la base de datos.

3. **Orden de Importación**: Los productos se importan en el orden que aparecen en el JSON.

4. **Backup**: Antes de importar, considera hacer backup de la base de datos.

5. **Rate Limiting**: Si el servidor tiene rate limiting, ajusta `DELAY_ENTRE_PRODUCTOS` en consecuencia.

## 🐛 Solución de Problemas

### El servidor no responde

```bash
# Verificar que el servidor esté corriendo
curl http://localhost:4000

# Si no funciona, inicia el servidor
# (comando depende de tu configuración)
```

### Token expirado

1. Obtén un nuevo token desde el servidor
2. Actualiza `config_servidor.py`:
   ```python
   AUTH_TOKEN = "nuevo_token_aqui"
   ```

### Productos no se importan

1. Verifica el formato JSON:
   ```bash
   python -m json.tool datos/json/productos_mercadolibre.json
   ```

2. Revisa los logs del servidor para ver el error específico

3. Prueba importar un producto individual para debug:
   ```bash
   python importar_a_servidor.py datos/json/PRODUCTO.json
   ```

### Error de importación

Revisa el reporte generado:

```bash
# Ver productos fallidos
jq '.productos_fallidos' datos/json/reporte_importacion_*.json
```

## 📈 Monitoreo

### Ver Progreso en Tiempo Real

El script muestra progreso en tiempo real. Ejemplo:

```
[5/10] Procesando producto...
  📦 Medios De 8 Pulgadas El Par Color Negro
  SKU: MED-OTRO-VAR-789
  ✓ Producto creado exitosamente
```

### Estadísticas de Importación

Al final de cada importación verás:

- Total de productos procesados
- Exitosos vs fallidos
- Tiempo total de importación
- Lista de productos con errores (si hay)

## 🔗 Integración con Workflow

Puedes integrar el importador en tu workflow completo:

```bash
#!/bin/bash
# workflow_completo_con_importacion.sh

# 1. Scraping
echo "📥 Scraping productos..."
python scraper_mercadolibre_v2.py

# 2. Conversión incremental
echo "🔄 Convirtiendo a JSON..."
python conversor_a_json.py

# 3. Importación al servidor
echo "📤 Importando al servidor..."
python importar_a_servidor.py

echo "✅ Workflow completado"
```
