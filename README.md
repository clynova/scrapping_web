# Web Scraper para Mercado Libre

Script de Python para extraer información de productos de Mercado Libre, incluyendo detalles y descarga de imágenes.

## 🚀 Características

- ✅ Extrae título, precio, condición, ubicación y vendedor
- 📷 Descarga imágenes de productos automáticamente
- 📄 Guarda resultados en Excel y CSV
- 🔄 Navegación automática por páginas
- ⏱️ Pausas éticas para no saturar el servidor
- 🛡️ Headers para evitar bloqueos simples

## 📋 Requisitos

- Python 3.7+
- Dependencias listadas en `requirements.txt`

## 🔧 Instalación

1. Clona o descarga este proyecto

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 📖 Uso

1. Abre el archivo `scraper_mercadolibre.py`

2. Modifica la URL en la línea del ejemplo:
```python
url_inicial = "TU_URL_DE_MERCADO_LIBRE_AQUI"
```

3. Ejecuta el script:
```bash
python scraper_mercadolibre.py
```

4. Los resultados se guardarán en:
   - `productos_mercadolibre.xlsx` (Excel)
   - `productos_mercadolibre.csv` (CSV)
   - `imagenes_mercadolibre/` (carpeta con imágenes)

## 🎯 Ejemplos de URLs válidas

```
https://listado.mercadolibre.com.ar/laptops
https://listado.mercadolibre.com.mx/celulares
https://www.mercadolibre.com.ar/tienda/nombre-tienda
```

## ⚙️ Configuración

### Desactivar descarga de imágenes
```python
data = scrapear_tienda_ml(url_inicial, descargar_imagenes=False)
```

### Cambiar límite de páginas
Edita la variable `max_paginas` en la función `scrapear_tienda_ml`:
```python
max_paginas = 5  # Límite de páginas a scrapear
```

### Personalizar tiempo de espera
Modifica el `time.sleep()` en la función:
```python
time.sleep(3)  # Esperar 3 segundos entre páginas
```

## 📊 Datos Extraídos

El script extrae la siguiente información:

| Campo | Descripción |
|-------|-------------|
| Titulo | Nombre del producto |
| Precio | Precio en formato numérico |
| Condicion | Nuevo/Usado |
| Ubicacion | Ubicación del vendedor |
| Vendedor | Información del vendedor |
| Link | URL del producto |
| URL_Imagen | URL de la imagen del producto |
| Imagen_Local | Ruta local de la imagen descargada |

## ⚠️ Consideraciones Importantes

1. **Términos de Servicio**: Este script es para uso educativo. Asegúrate de cumplir con los [Términos y Condiciones de Mercado Libre](https://www.mercadolibre.com.ar/terminos-y-condiciones).

2. **Rate Limiting**: El script incluye pausas entre peticiones. No modifiques estos tiempos para evitar ser bloqueado.

3. **Cambios en la estructura HTML**: Mercado Libre puede cambiar sus clases CSS. Si el script deja de funcionar, inspecciona la página y actualiza los selectores.

4. **Uso responsable**: No abuses del scraping. Considera usar la [API oficial de Mercado Libre](https://developers.mercadolibre.com/) para proyectos comerciales.

## 🔍 Solución de Problemas

### No se encuentran productos
- Verifica que la URL sea correcta
- Las clases CSS pueden haber cambiado. Inspecciona la página con DevTools del navegador
- Actualiza los selectores en el código

### Error de conexión
- Verifica tu conexión a Internet
- Mercado Libre puede estar bloqueando las peticiones
- Intenta aumentar el tiempo de espera entre peticiones

### Imágenes no se descargan
- Verifica que tengas permisos de escritura en la carpeta
- Algunas imágenes pueden usar lazy loading
- Revisa la consola para ver errores específicos

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir cambios mayores.

---

**Nota**: Este proyecto es solo para fines educativos. Úsalo de manera responsable y ética.
