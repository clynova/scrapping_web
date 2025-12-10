# Ejemplo de uso avanzado del scraper de Mercado Libre

from scraper_mercadolibre import scrapear_tienda_ml, guardar_resultados

# Ejemplo 1: Scrapear sin descargar imágenes
print("=== Ejemplo 1: Sin descargar imágenes ===")
url = "https://listado.mercadolibre.com.ar/celulares"
productos = scrapear_tienda_ml(url, descargar_imagenes=False)
guardar_resultados(productos, nombre_archivo='celulares_sin_imagenes')

# Ejemplo 2: Scrapear con imágenes
print("\n=== Ejemplo 2: Con imágenes ===")
url = "https://listado.mercadolibre.com.mx/laptops"
productos = scrapear_tienda_ml(url, descargar_imagenes=True)
guardar_resultados(productos, nombre_archivo='laptops_con_imagenes')

# Ejemplo 3: Filtrar productos por precio
print("\n=== Ejemplo 3: Filtrar productos ===")
url = "https://listado.mercadolibre.com.ar/zapatillas"
productos = scrapear_tienda_ml(url, descargar_imagenes=False)

# Filtrar productos con precio menor a 50000
productos_filtrados = [p for p in productos if p['Precio'] and float(p['Precio'].replace(',', '')) < 50000]
print(f"Productos encontrados: {len(productos)}")
print(f"Productos con precio < 50000: {len(productos_filtrados)}")

guardar_resultados(productos_filtrados, nombre_archivo='zapatillas_economicas')

# Ejemplo 4: Búsqueda de tienda específica
print("\n=== Ejemplo 4: Tienda específica ===")
# Reemplaza con la URL de la tienda que quieras scrapear
url_tienda = "https://www.mercadolibre.com.ar/tienda/nombre-tienda"
# productos_tienda = scrapear_tienda_ml(url_tienda, descargar_imagenes=True)
# guardar_resultados(productos_tienda, nombre_archivo='productos_tienda')
