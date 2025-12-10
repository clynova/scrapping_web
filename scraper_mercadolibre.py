import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from urllib.parse import urljoin, urlparse
import re

def descargar_imagen(url_imagen, carpeta_destino, nombre_producto):
    """
    Descarga una imagen y la guarda localmente.
    """
    try:
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)
        
        # Limpiar nombre para el archivo
        nombre_limpio = re.sub(r'[^\w\s-]', '', nombre_producto)[:50]
        nombre_limpio = re.sub(r'[-\s]+', '_', nombre_limpio)
        
        # Obtener extensión de la imagen
        extension = os.path.splitext(urlparse(url_imagen).path)[1] or '.jpg'
        nombre_archivo = f"{nombre_limpio}{extension}"
        ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
        
        # Evitar descargar si ya existe
        if os.path.exists(ruta_completa):
            return ruta_completa
        
        response = requests.get(url_imagen, timeout=10)
        if response.status_code == 200:
            with open(ruta_completa, 'wb') as f:
                f.write(response.content)
            return ruta_completa
        return None
    except Exception as e:
        print(f"Error descargando imagen: {e}")
        return None

def scrapear_tienda_ml(url_tienda, descargar_imagenes=True):
    """
    Scrapea productos de Mercado Libre con sus detalles e imágenes.
    
    Args:
        url_tienda (str): URL de la tienda o búsqueda de Mercado Libre
        descargar_imagenes (bool): Si es True, descarga las imágenes localmente
    
    Returns:
        list: Lista de diccionarios con información de productos
    """
    productos = []
    carpeta_imagenes = 'imagenes_mercadolibre'
    
    # Headers para parecer un navegador real y evitar bloqueos
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    pagina_actual = 1
    max_paginas = 10  # Límite de seguridad para evitar loops infinitos

    while url_tienda and pagina_actual <= max_paginas:
        print(f"Scrapeando página {pagina_actual}: {url_tienda[:80]}...")
        
        try:
            response = requests.get(url_tienda, headers=headers, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Error al obtener la página: {e}")
            break
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Seleccionamos los contenedores de los productos
        # Mercado Libre usa diferentes clases dependiendo del tipo de listado
        items = soup.find_all('li', class_='ui-search-layout__item')
        
        if not items:
            print("No se encontraron productos. Las clases CSS pueden haber cambiado.")
            break

        print(f"Encontrados {len(items)} productos en esta página.")

        for idx, item in enumerate(items, 1):
            try:
                # Título del producto
                titulo_elem = item.find('h2', class_='ui-search-item__title')
                titulo = titulo_elem.text.strip() if titulo_elem else "Sin título"
                
                # Precio - Mercado Libre separa en fracciones y centavos
                precio_texto = "0"
                precio_container = item.find('span', class_='andes-money-amount__fraction')
                if precio_container:
                    precio_texto = precio_container.text.strip().replace('.', '').replace(',', '')
                    
                    # Intentar obtener centavos si existen
                    centavos = item.find('span', class_='andes-money-amount__cents')
                    if centavos:
                        precio_texto = f"{precio_texto}.{centavos.text.strip()}"
                
                # Link del producto
                link_elem = item.find('a', class_='ui-search-link')
                link = link_elem['href'] if link_elem else ""
                
                # Imagen del producto
                img_elem = item.find('img', class_='ui-search-result-image__element')
                url_imagen = ""
                ruta_imagen_local = ""
                
                if img_elem:
                    # Mercado Libre puede usar 'src' o 'data-src'
                    url_imagen = img_elem.get('src') or img_elem.get('data-src', '')
                    
                    if descargar_imagenes and url_imagen:
                        ruta_imagen_local = descargar_imagen(
                            url_imagen, 
                            carpeta_imagenes, 
                            f"{idx}_{titulo}"
                        )
                
                # Vendedor/Tienda (si está disponible)
                vendedor_elem = item.find('span', class_='ui-search-item__group__element ui-search-item__shipping-label')
                vendedor = vendedor_elem.text.strip() if vendedor_elem else ""
                
                # Ubicación
                ubicacion_elem = item.find('span', class_='ui-search-item__location-label')
                ubicacion = ubicacion_elem.text.strip() if ubicacion_elem else ""
                
                # Condición (Nuevo/Usado)
                condicion_elem = item.find('span', class_='ui-search-item__group__element ui-search-item__condition')
                condicion = condicion_elem.text.strip() if condicion_elem else ""
                
                producto = {
                    'Titulo': titulo,
                    'Precio': precio_texto,
                    'Condicion': condicion,
                    'Ubicacion': ubicacion,
                    'Vendedor': vendedor,
                    'Link': link,
                    'URL_Imagen': url_imagen,
                    'Imagen_Local': ruta_imagen_local if descargar_imagenes else ""
                }
                
                productos.append(producto)
                
            except AttributeError as e:
                print(f"Error procesando producto {idx}: {e}")
                continue
            except Exception as e:
                print(f"Error inesperado en producto {idx}: {e}")
                continue

        # Lógica de Paginación
        next_btn = soup.find('a', title='Siguiente')
        if next_btn and next_btn.get('href'):
            url_tienda = next_btn['href']
            pagina_actual += 1
            # Pausa ética para no saturar el servidor
            time.sleep(2)
        else:
            print("No hay más páginas.")
            url_tienda = None

    return productos

def guardar_resultados(productos, nombre_archivo='productos_mercadolibre'):
    """
    Guarda los productos en Excel y CSV.
    """
    if not productos:
        print("No hay productos para guardar.")
        return
    
    df = pd.DataFrame(productos)
    
    # Guardar en Excel
    archivo_excel = f'{nombre_archivo}.xlsx'
    df.to_excel(archivo_excel, index=False, engine='openpyxl')
    print(f"✓ Guardado en Excel: {archivo_excel}")
    
    # Guardar en CSV como respaldo
    archivo_csv = f'{nombre_archivo}.csv'
    df.to_csv(archivo_csv, index=False, encoding='utf-8-sig')
    print(f"✓ Guardado en CSV: {archivo_csv}")
    
    # Mostrar resumen
    print(f"\nResumen:")
    print(f"- Total de productos: {len(productos)}")
    print(f"- Productos con imagen: {df['URL_Imagen'].notna().sum()}")
    if 'Imagen_Local' in df.columns:
        print(f"- Imágenes descargadas: {df['Imagen_Local'].astype(bool).sum()}")

# --- EJEMPLO DE USO ---
if __name__ == "__main__":
    # INSTRUCCIONES:
    # 1. Ve a Mercado Libre y busca productos o ve a una tienda
    # 2. Copia la URL completa de la página de resultados
    # 3. Pégala aquí abajo:
    
    # URL del listado de todos los productos de la tienda
    url_inicial = "https://listado.mercadolibre.cl/pagina/ar20240628111129"  # Tienda Viaje Azul Chile
    
    print("=== Scraper de Mercado Libre ===\n")
    print("Iniciando scraping...")
    print("NOTA: Asegúrate de respetar los términos de servicio de Mercado Libre\n")
    
    # Scrapear productos (con imágenes)
    data = scrapear_tienda_ml(url_inicial, descargar_imagenes=True)
    
    # Guardar resultados
    guardar_resultados(data)
    
    print("\n¡Proceso completado!")
