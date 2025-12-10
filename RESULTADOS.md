# ========================================================
# 🚀 SCRAPER DE MERCADO LIBRE - VIAJE AZUL
# ========================================================

## ✅ Completado Exitosamente!

El scraper ha extraído **48 productos** de la tienda "Viaje Azul" en Mercado Libre Chile.

### 📁 Archivos Generados:

1. **viaje_azul_productos.xlsx** - Archivo Excel con todos los productos
2. **viaje_azul_productos.csv** - Archivo CSV (compatible con cualquier editor)
3. **imagenes_mercadolibre/** - Carpeta con 48 imágenes de productos

### 📊 Datos Extraídos por Producto:

- ✅ ID del producto
- ✅ Título completo
- ✅ Precio
- ✅ Condición (Nuevo/Usado)
- ✅ Ubicación del vendedor
- ✅ Información de envío
- ✅ Link directo al producto
- ✅ URL de la imagen
- ✅ Ruta de imagen descargada localmente

---

## 🔄 Cómo Ejecutar el Scraper Nuevamente:

### Opción 1: Script Automático
```bash
cd /home/clynova/proyectos/scrapping_web
source venv/bin/activate
python ejecutar_scraper.py
```

### Opción 2: Ejecutar Directamente
```bash
cd /home/clynova/proyectos/scrapping_web
source venv/bin/activate
python scraper_mercadolibre_v2.py
```

---

## 🎯 Cambiar la URL a Scrapear:

Edita el archivo `scraper_mercadolibre_v2.py` en la línea ~320:

```python
# URL del listado de productos de la tienda Viaje Azul (con barra final)
url_inicial = "https://listado.mercadolibre.cl/pagina/ar20240628111129/"
```

### URLs de Ejemplo:

```python
# Otra tienda
url_inicial = "https://listado.mercadolibre.cl/tienda/nombre-tienda/"

# Búsqueda específica
url_inicial = "https://listado.mercadolibre.cl/laptops"

# Categoría
url_inicial = "https://listado.mercadolibre.cl/accesorios-vehiculos/"
```

---

## ⚙️ Configuraciones Útiles:

### Desactivar Descarga de Imágenes:
En `scraper_mercadolibre_v2.py`, línea ~323:
```python
data = scrapear_tienda_ml(url_inicial, descargar_imagenes=False)
```

### Cambiar Límite de Páginas:
En `scraper_mercadolibre_v2.py`, línea ~84:
```python
max_paginas = 5  # Cambiar el número según necesites
```

### Modificar Tiempo de Espera:
En `scraper_mercadolibre_v2.py`, línea ~234:
```python
time.sleep(3)  # Aumentar si el sitio bloquea las peticiones
```

---

## 📖 Archivos del Proyecto:

- `scraper_mercadolibre_v2.py` - Scraper principal (MEJORADO)
- `scraper_mercadolibre.py` - Versión original
- `ejecutar_scraper.py` - Script de ejecución automática
- `ejemplo_uso.py` - Ejemplos de uso avanzado
- `requirements.txt` - Dependencias necesarias
- `README.md` - Documentación completa

---

## ⚠️ Notas Importantes:

1. **Respeta los Términos de Servicio**: Este scraper es para uso educativo
2. **No abuses**: Las pausas entre peticiones son importantes
3. **API Oficial**: Para uso comercial, considera la [API de Mercado Libre](https://developers.mercadolibre.com/)
4. **Cambios en la Web**: Si el scraper deja de funcionar, Mercado Libre puede haber cambiado su estructura

---

## 🐛 Solución de Problemas:

### No se encuentran productos:
- Verifica que la URL sea del listado (debe contener `/listado/` o terminar en `/`)
- La estructura de Mercado Libre puede haber cambiado

### Error de dependencias:
```bash
pip install -r requirements.txt
```

### Imágenes no se descargan:
- Verifica permisos de escritura en la carpeta
- Algunas imágenes pueden fallar (es normal)

---

## 📞 Datos del Proyecto:

**Tienda:** Viaje Azul  
**País:** Chile  
**URL:** https://www.mercadolibre.cl/pagina/ar20240628111129  
**Fecha:** Diciembre 2025  
**Productos extraídos:** 48  
**Rango de precios:** $4,280 - $53,899 CLP  

---

¡Scraping completado con éxito! 🎉
