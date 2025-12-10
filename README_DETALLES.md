# 🎉 ¡Scraper Actualizado con Extracción de Detalles!

## ✅ ¿Qué hay de nuevo?

El scraper ahora puede extraer **información completa** de cada producto visitando su página individual:

### 📋 Datos Que Ahora Extrae:

#### Datos Básicos (como antes):
- ✅ ID del producto
- ✅ Título
- ✅ Precio
- ✅ Condición (Nuevo/Usado)
- ✅ Ubicación del vendedor
- ✅ Información de envío
- ✅ Link directo al producto
- ✅ URL de imagen
- ✅ Imagen descargada localmente

#### 🆕 Datos Detallados (NUEVO):
- ✅ **Descripción completa** del producto (hasta 500 caracteres)
- ✅ **Características Principales** (Marca, Modelo, Color, etc.)
- ✅ **Características de Venta** (Garantía, devoluciones, etc.)
- ✅ **Otras Características** (Especificaciones técnicas)

---

## 🚀 Cómo Usar

### Opción 1: Scraping Rápido de Prueba (10 productos)

```bash
cd /home/clynova/proyectos/scrapping_web
source venv/bin/activate
python scraper_con_detalles_limitado.py
```

⏱️ **Tiempo:** ~5 minutos  
📊 **Resultado:** 10 productos con todos los detalles

### Opción 2: Scraping Completo (48 productos)

```bash
source venv/bin/activate
python scraper_mercadolibre_v2.py
```

⏱️ **Tiempo:** ~20 minutos  
📊 **Resultado:** Todos los productos con detalles completos

### Opción 3: Scraping Sin Detalles (Rápido)

Edita [scraper_mercadolibre_v2.py](scraper_mercadolibre_v2.py) línea ~461:
```python
data = scrapear_tienda_ml(url_inicial, descargar_imagenes=True, extraer_detalles=False)
```

⏱️ **Tiempo:** ~3 minutos  
📊 **Resultado:** Solo datos básicos

---

## 📊 Ejemplo de Datos Extraídos

### Producto de Ejemplo:

```
🆔 ID: 3
📌 TÍTULO: Inmovilizador Auto Distancia Corta Corriente Antirobo
💰 PRECIO: $19,980 CLP

📝 DESCRIPCIÓN:
Inmovilizador Auto Distancia Corta Corriente Antirobo Autos
- Tecnología de señal de transmisión bidireccional
- Fácil de ocultar
- Frecuencia de trabajo: 2,4 GHz FSK/GFSK
- Incluye 2 controles
- Alcance: 2M
...

⚙️  CARACTERÍSTICAS PRINCIPALES:
   • Marca: Genérica
   • Modelo: Inmovilizador 2.4 GHZ 2M

🖼️  IMAGEN: imagenes_mercadolibre/3_Producto_3.jpg
```

---

## 📁 Archivos Generados

Cuando ejecutas con **detalles**:
```
viaje_azul_productos_con_detalles.xlsx  ← Archivo Excel completo
viaje_azul_productos_con_detalles.csv   ← Archivo CSV
imagenes_mercadolibre/                   ← Carpeta con imágenes
```

Cuando ejecutas **sin detalles**:
```
viaje_azul_productos.xlsx
viaje_azul_productos.csv
imagenes_mercadolibre/
```

---

## 📈 Estadísticas de Completitud

Basado en prueba de 10 productos:

| Dato | Completitud |
|------|-------------|
| Descripción | 100% (10/10) |
| Características Principales | 100% (10/10) |
| Imágenes | 100% (10/10) |
| Características de Venta | Variable* |
| Otras Características | Variable* |

*Depende de si el vendedor completó esta información

---

## 🔧 Scripts Disponibles

| Script | Productos | Detalles | Tiempo | Uso |
|--------|-----------|----------|--------|-----|
| `test_detalles.py` | 3 | ✅ | ~1 min | Prueba inicial |
| `scraper_con_detalles_limitado.py` | 10 | ✅ | ~5 min | Prueba rápida |
| `scraper_mercadolibre_v2.py` | 48 | ✅ | ~20 min | Producción |
| `scraper_mercadolibre_v2.py` (sin detalles) | 48 | ❌ | ~3 min | Rápido |

---

## ⚙️ Configuración

### Cambiar URL de la Tienda

Edita `scraper_mercadolibre_v2.py`:
```python
url_inicial = "TU_URL_AQUI"
```

### Deshabilitar Descarga de Imágenes

```python
data = scrapear_tienda_ml(url_inicial, descargar_imagenes=False, extraer_detalles=True)
```

### Solo Datos Básicos (Más Rápido)

```python
data = scrapear_tienda_ml(url_inicial, descargar_imagenes=True, extraer_detalles=False)
```

---

## 📖 Documentación

- **[GUIA_DETALLES.md](GUIA_DETALLES.md)** - Guía completa de uso
- **[README.md](README.md)** - Documentación original
- **[RESULTADOS.md](RESULTADOS.md)** - Instrucciones de configuración

---

## 💡 Consejos

### ✅ Buenas Prácticas:

1. **Prueba primero** con el script limitado
2. **Verifica** que los datos son correctos
3. **Respeta** los tiempos de espera (no los modifiques)
4. **Usa** para fines educativos o personales

### ⚠️ Ten en Cuenta:

- La extracción de detalles es **más lenta** pero **más completa**
- No todos los productos tienen **todas** las características
- Mercado Libre puede **cambiar** su estructura HTML
- El scraping intensivo puede resultar en **bloqueos temporales**

---

## 🐛 Solución de Problemas

### No se extraen características

**Normal:** Algunos vendedores no completan todas las características.

**Verifica:** Visita manualmente la URL del producto y confirma que la información existe.

### Error al extraer detalles

**Causa:** La estructura HTML cambió.

**Solución:** Inspecciona la página con DevTools y actualiza los selectores en `extraer_detalles_producto()`.

### Scraping muy lento

**Soluciones:**
- Usa el script limitado
- Deshabilita `extraer_detalles`
- Deshabilita descarga de imágenes

---

## 📞 Estructura del Proyecto

```
scrapping_web/
├── scraper_mercadolibre_v2.py          ← Principal (CON detalles)
├── scraper_con_detalles_limitado.py   ← 10 productos con detalles
├── test_detalles.py                    ← Prueba de 3 productos
├── scraper_mercadolibre.py             ← Versión original (SIN detalles)
├── ejecutar_scraper.py                 ← Ejecutor automático
├── run.sh                              ← Script bash
├── requirements.txt                    ← Dependencias
├── GUIA_DETALLES.md                   ← Guía completa
├── README.md                           ← Documentación
└── venv/                               ← Entorno virtual
```

---

## 🎯 Ejemplo de Uso en Python

```python
from scraper_mercadolibre_v2 import scrapear_tienda_ml, guardar_resultados

# Scrapear con todos los detalles
url = "https://listado.mercadolibre.cl/pagina/ar20240628111129/"
productos = scrapear_tienda_ml(
    url, 
    descargar_imagenes=True,  # Descargar imágenes
    extraer_detalles=True      # Extraer características
)

# Guardar resultados
guardar_resultados(productos, nombre_archivo='mi_scraping_completo')

print(f"✅ Extraídos {len(productos)} productos con detalles completos")
```

---

## ✅ Resultados de Prueba

**Última ejecución exitosa:**
- ✅ 10 productos extraídos
- ✅ 100% con descripción
- ✅ 100% con características principales
- ✅ 10 imágenes descargadas
- ⏱️ Tiempo: 5 minutos

---

## 📝 Changelog

### Versión 2.0 (Actual)
- ✨ **NUEVO:** Extracción de descripción completa
- ✨ **NUEVO:** Extracción de características principales
- ✨ **NUEVO:** Extracción de características de venta
- ✨ **NUEVO:** Extracción de otras características
- ✨ **NUEVO:** Script de prueba limitado
- ✨ **NUEVO:** Modo configurable (con/sin detalles)
- 🔧 Mejora en manejo de errores
- 📚 Documentación expandida

### Versión 1.0
- ✅ Extracción de datos básicos
- ✅ Descarga de imágenes
- ✅ Paginación automática
- ✅ Exportación a Excel/CSV

---

¡Todo listo para extraer información completa de Mercado Libre! 🚀

**Archivo actualizado:** Diciembre 10, 2025
