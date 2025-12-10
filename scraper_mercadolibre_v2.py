import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
from urllib.parse import urljoin, urlparse
import re
import json

def descargar_imagen(url_imagen, carpeta_destino, nombre_producto, indice):
    """
    Descarga una imagen y la guarda localmente.
    """
    try:
        if not os.path.exists(carpeta_destino):
            os.makedirs(carpeta_destino)
        
        # Limpiar nombre para el archivo
        nombre_limpio = re.sub(r'[^\w\s-]', '', nombre_producto)[:50]
        nombre_limpio = re.sub(r'[-\s]+', '_', nombre_limpio)
        
        # Agregar índice para evitar duplicados
        extension = '.jpg'
        nombre_archivo = f"{indice}_{nombre_limpio}{extension}"
        ruta_completa = os.path.join(carpeta_destino, nombre_archivo)
        
        # Evitar descargar si ya existe
        if os.path.exists(ruta_completa):
            return ruta_completa
        
        # Limpiar URL de imagen (Mercado Libre a veces usa tamaños diferentes)
        if '-I' in url_imagen or '-O' in url_imagen or '-D' in url_imagen:
            url_imagen = re.sub(r'-[IOD]\..*$', '-F.jpg', url_imagen)
        
        response = requests.get(url_imagen, timeout=10)
        if response.status_code == 200:
            with open(ruta_completa, 'wb') as f:
                f.write(response.content)
            return ruta_completa
        return None
    except Exception as e:
        print(f"Error descargando imagen: {e}")
        return None

def extraer_detalles_producto(url_producto, headers):
    """
    Extrae los detalles completos de un producto individual visitando su página.
    """
    detalles = {
        'Descripcion': '',
        'Caracteristicas_Principales': {},
        'Caracteristicas_Ventas': {},
        'Otras_Caracteristicas': {}
    }
    
    try:
        print(f"    → Extrayendo detalles del producto...", end=' ')
        response = requests.get(url_producto, headers=headers, timeout=15)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Extraer descripción
        desc_elem = soup.find('div', class_=re.compile(r'ui-pdp-description'))
        if not desc_elem:
            desc_elem = soup.find('div', class_=re.compile(r'item-description'))
        if not desc_elem:
            # Buscar en el contenido de texto
            desc_elem = soup.find('p', class_=re.compile(r'ui-pdp-description__content'))
        
        if desc_elem:
            detalles['Descripcion'] = desc_elem.get_text(strip=True, separator=' ')[:500]
        
        # Extraer características/especificaciones
        # Mercado Libre usa diferentes estructuras según el tipo de producto
        
        # Método 1: Tabla de especificaciones estándar
        spec_table = soup.find('table', class_=re.compile(r'andes-table|specs'))
        if spec_table:
            rows = spec_table.find_all('tr')
            for row in rows:
                cells = row.find_all(['th', 'td'])
                if len(cells) >= 2:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    detalles['Caracteristicas_Principales'][key] = value
        
        # Método 2: Divs con atributos
        specs_container = soup.find_all('div', class_=re.compile(r'ui-pdp-highlighted-specs|ui-vpp-highlighted-specs'))
        for container in specs_container:
            spec_items = container.find_all('div', class_=re.compile(r'ui-pdp-highlighted-specs__item'))
            for item in spec_items:
                label = item.find('span', class_=re.compile(r'label'))
                value = item.find('span', class_=re.compile(r'value'))
                if label and value:
                    detalles['Caracteristicas_Ventas'][label.get_text(strip=True)] = value.get_text(strip=True)
        
        # Método 3: Sección de especificaciones técnicas
        tech_specs = soup.find_all('div', class_=re.compile(r'ui-pdp-specs'))
        for spec_section in tech_specs:
            spec_pairs = spec_section.find_all('tr')
            for pair in spec_pairs:
                th = pair.find('th')
                td = pair.find('td')
                if th and td:
                    key = th.get_text(strip=True)
                    value = td.get_text(strip=True)
                    if key and value:
                        detalles['Otras_Caracteristicas'][key] = value
        
        # Método 4: Buscar en scripts JSON-LD (datos estructurados)
        scripts = soup.find_all('script', type='application/ld+json')
        for script in scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    # Extraer descripción si está disponible
                    if 'description' in data and not detalles['Descripcion']:
                        detalles['Descripcion'] = data['description'][:500]
                    
                    # Extraer propiedades adicionales
                    if 'additionalProperty' in data:
                        for prop in data['additionalProperty']:
                            if isinstance(prop, dict):
                                name = prop.get('name', '')
                                value = prop.get('value', '')
                                if name and value:
                                    detalles['Caracteristicas_Principales'][name] = str(value)
            except:
                continue
        
        print("✓")
        time.sleep(0.5)  # Pequeña pausa entre peticiones de detalles
        
    except Exception as e:
        print(f"✗ Error: {e}")
    
    return detalles

def extraer_datos_json(soup):
    """
    Intenta extraer datos de producto desde el JSON embebido en la página.
    Mercado Libre a menudo incluye datos estructurados en JSON-LD o en scripts.
    """
    productos = []
    
    # Buscar scripts con datos JSON
    scripts = soup.find_all('script', type='application/ld+json')
    
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and data.get('@type') == 'Product':
                producto = {
                    'Titulo': data.get('name', ''),
                    'Precio': data.get('offers', {}).get('price', ''),
                    'URL_Imagen': data.get('image', ''),
                    'Link': data.get('url', '')
                }
                productos.append(producto)
        except:
            continue
    
    return productos

def scrapear_tienda_ml(url_tienda, descargar_imagenes=True, extraer_detalles=True):
    """
    Scrapea productos de Mercado Libre con sus detalles e imágenes.
    Versión mejorada que detecta diferentes estructuras de página.
    
    Args:
        url_tienda: URL del listado de productos
        descargar_imagenes: Si es True, descarga las imágenes localmente
        extraer_detalles: Si es True, visita cada producto para extraer características detalladas
    """
    productos = []
    carpeta_imagenes = 'imagenes_mercadolibre'
    contador_productos = 0
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'es-CL,es;q=0.9,en;q=0.8',
        # Removido Accept-Encoding para que requests maneje la descompresión automáticamente
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }

    pagina_actual = 1
    max_paginas = 10

    while url_tienda and pagina_actual <= max_paginas:
        print(f"\n{'='*60}")
        print(f"Scrapeando página {pagina_actual}")
        print(f"URL: {url_tienda[:80]}...")
        print(f"{'='*60}")
        
        try:
            response = requests.get(url_tienda, headers=headers, timeout=15)
            response.raise_for_status()
            response.encoding = 'utf-8'
        except requests.RequestException as e:
            print(f"❌ Error al obtener la página: {e}")
            break
        
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Intentar múltiples selectores para encontrar productos
        items = []
        
        # Intento 1: Layout estándar de listado
        items = soup.find_all('li', class_='ui-search-layout__item')
        
        if not items:
            # Intento 2: Grilla de productos
            items = soup.find_all('div', class_='ui-search-result__wrapper')
        if not items:
            # Intento 3: Otro formato común
            items = soup.find_all('div', class_='andes-card')
        if not items:
            # Intento 4: Productos en la tienda
            items = soup.find_all('div', class_='shops__layout-item')
        if not items:
            # Intento 5: Formato de artículos
            items = soup.find_all('article', class_='')
        
        if not items:
            print(f"⚠️  No se encontraron productos con los selectores conocidos.")
            print("Intentando método alternativo...")
            
            # Buscar todos los enlaces que apunten a productos
            enlaces_productos = soup.find_all('a', href=lambda href: href and ('/p/' in href or '/MLC' in href))
            print(f"Encontrados {len(enlaces_productos)} enlaces potenciales")
            
            # Si realmente no hay items, el sitio probablemente usa JavaScript
            if not enlaces_productos:
                print("❌ No se pudieron extraer productos. La página podría requerir JavaScript.")
                break
            
            # Crear items pseudo desde los enlaces
            items = []
            for enlace in enlaces_productos[:50]:  # Limitar a 50 para no saturar
                parent = enlace.find_parent('div', class_=re.compile(r'poly-card|ui-search|shops'))
                if parent and parent not in items:
                    items.append(parent)
        
        print(f"✓ Encontrados {len(items)} elementos para procesar")

        for idx, item in enumerate(items, 1):
            contador_productos += 1
            try:
                # Título del producto
                titulo = ""
                
                # Método 1: Buscar en <a> con clase poly-component__title
                titulo_elem = item.find('a', class_=re.compile(r'poly-component__title'))
                if titulo_elem:
                    titulo = titulo_elem.text.strip()
                
                # Método 2: Buscar en <h2>
                if not titulo:
                    titulo_elem = item.find('h2', class_=re.compile(r'ui-search-item__title|poly-component__title'))
                    if titulo_elem:
                        titulo = titulo_elem.text.strip()
                
                # Método 3: Buscar por atributo title en enlaces
                if not titulo:
                    any_link = item.find('a', title=True)
                    if any_link:
                        titulo = any_link.get('title', '').strip()
                
                # Método 4: Buscar en <h3>
                if not titulo:
                    titulo_elem = item.find('h3')
                    if titulo_elem:
                        titulo = titulo_elem.text.strip()
                
                # Fallback solo si realmente no se encuentra nada
                if not titulo:
                    print(f"  ⚠️  No se pudo extraer título para item {contador_productos}")
                    titulo = f"Producto {contador_productos}"
                
                # Precio
                precio_texto = "0"
                precio_container = item.find('span', class_='andes-money-amount__fraction')
                if not precio_container:
                    precio_container = item.find('span', class_=re.compile(r'price'))
                if not precio_container:
                    precio_match = item.find('div', class_=re.compile(r'price'))
                    if precio_match:
                        precio_texto = re.sub(r'[^\d,.]', '', precio_match.text.strip())
                
                if precio_container:
                    precio_texto = precio_container.text.strip().replace('.', '').replace(',', '')
                    centavos = item.find('span', class_='andes-money-amount__cents')
                    if centavos:
                        precio_texto = f"{precio_texto}.{centavos.text.strip()}"
                
                # Link del producto
                link = ""
                link_elem = item.find('a', href=re.compile(r'/p/|/MLC|/up/'))
                if link_elem:
                    link = link_elem.get('href', '')
                    # Asegurar URL completa
                    if link and not link.startswith('http'):
                        link = urljoin(url_tienda, link)
                
                # Imagen del producto
                url_imagen = ""
                ruta_imagen_local = ""
                
                img_elem = item.find('img')
                if img_elem:
                    url_imagen = img_elem.get('data-src') or img_elem.get('src', '')
                    
                    # Limpiar data URIs
                    if url_imagen.startswith('data:'):
                        url_imagen = ""
                    
                    if descargar_imagenes and url_imagen:
                        ruta_imagen_local = descargar_imagen(
                            url_imagen, 
                            carpeta_imagenes, 
                            titulo,
                            contador_productos
                        )
                
                # Información adicional
                ubicacion = ""
                ubicacion_elem = item.find('span', class_=re.compile(r'location'))
                if ubicacion_elem:
                    ubicacion = ubicacion_elem.text.strip()
                
                # Condición
                condicion = ""
                condicion_elem = item.find('span', class_=re.compile(r'condition'))
                if condicion_elem:
                    condicion = condicion_elem.text.strip()
                
                # Envío
                envio = ""
                envio_elem = item.find('span', class_=re.compile(r'shipping|envio'))
                if envio_elem:
                    envio = envio_elem.text.strip()
                
                # Crear producto base
                producto = {
                    'ID': contador_productos,
                    'Titulo': titulo,
                    'Precio': precio_texto,
                    'Condicion': condicion,
                    'Ubicacion': ubicacion,
                    'Envio': envio,
                    'Link': link,
                    'URL_Imagen': url_imagen,
                    'Imagen_Local': ruta_imagen_local if descargar_imagenes else "",
                    'Descripcion': '',
                    'Caracteristicas_Principales': '',
                    'Caracteristicas_Ventas': '',
                    'Otras_Caracteristicas': ''
                }
                
                # Extraer detalles del producto si está habilitado
                if extraer_detalles and link:
                    detalles = extraer_detalles_producto(link, headers)
                    producto['Descripcion'] = detalles['Descripcion']
                    
                    # Convertir diccionarios a strings formatados
                    if detalles['Caracteristicas_Principales']:
                        producto['Caracteristicas_Principales'] = ' | '.join(
                            [f"{k}: {v}" for k, v in detalles['Caracteristicas_Principales'].items()]
                        )
                    
                    if detalles['Caracteristicas_Ventas']:
                        producto['Caracteristicas_Ventas'] = ' | '.join(
                            [f"{k}: {v}" for k, v in detalles['Caracteristicas_Ventas'].items()]
                        )
                    
                    if detalles['Otras_Caracteristicas']:
                        producto['Otras_Caracteristicas'] = ' | '.join(
                            [f"{k}: {v}" for k, v in detalles['Otras_Caracteristicas'].items()]
                        )
                
                productos.append(producto)
                print(f"  [{idx}/{len(items)}] ✓ {titulo[:60]}... - ${precio_texto}")
                
            except Exception as e:
                print(f"  [{idx}/{len(items)}] ❌ Error: {e}")
                continue

        # Lógica de Paginación
        next_btn = soup.find('a', {'title': re.compile(r'Siguiente|Next', re.I)})
        if not next_btn:
            next_btn = soup.find('a', class_=re.compile(r'andes-pagination__button--next'))
        
        if next_btn and next_btn.get('href'):
            url_tienda = next_btn['href']
            if not url_tienda.startswith('http'):
                # Construir URL completa si es relativa
                from urllib.parse import urljoin
                url_tienda = urljoin(response.url, url_tienda)
            pagina_actual += 1
            print(f"\n⏳ Esperando 2 segundos antes de la siguiente página...")
            time.sleep(2)
        else:
            print(f"\n✓ No hay más páginas disponibles")
            url_tienda = None

    return productos

def guardar_resultados(productos, nombre_archivo='productos_mercadolibre'):
    """
    Guarda los productos en Excel y CSV.
    """
    if not productos:
        print("\n⚠️  No hay productos para guardar.")
        return
    
    df = pd.DataFrame(productos)
    
    # Guardar en Excel
    archivo_excel = f'{nombre_archivo}.xlsx'
    try:
        df.to_excel(archivo_excel, index=False, engine='openpyxl')
        print(f"\n✅ Guardado en Excel: {archivo_excel}")
    except Exception as e:
        print(f"\n❌ Error guardando Excel: {e}")
    
    # Guardar en CSV como respaldo
    archivo_csv = f'{nombre_archivo}.csv'
    try:
        df.to_csv(archivo_csv, index=False, encoding='utf-8-sig')
        print(f"✅ Guardado en CSV: {archivo_csv}")
    except Exception as e:
        print(f"❌ Error guardando CSV: {e}")
    
    # Mostrar resumen
    print(f"\n{'='*60}")
    print("RESUMEN DEL SCRAPING")
    print(f"{'='*60}")
    print(f"📦 Total de productos extraídos: {len(productos)}")
    print(f"🖼️  Productos con imagen URL: {df['URL_Imagen'].astype(bool).sum()}")
    if 'Imagen_Local' in df.columns:
        imagenes_descargadas = df['Imagen_Local'].astype(bool).sum()
        print(f"💾 Imágenes descargadas localmente: {imagenes_descargadas}")
    if 'Descripcion' in df.columns:
        con_descripcion = df['Descripcion'].astype(bool).sum()
        print(f"📝 Productos con descripción: {con_descripcion}")
    if 'Caracteristicas_Principales' in df.columns:
        con_caracteristicas = df['Caracteristicas_Principales'].astype(bool).sum()
        print(f"⚙️  Productos con características: {con_caracteristicas}")
    print(f"💰 Rango de precios: ${df['Precio'].astype(str).str.replace(',', '').replace('', '0').astype(float).min():.0f} - ${df['Precio'].astype(str).str.replace(',', '').replace('', '0').astype(float).max():.0f}")
    print(f"{'='*60}")

# --- EJEMPLO DE USO ---
if __name__ == "__main__":
    print("\n" + "="*60)
    print(" SCRAPER DE MERCADO LIBRE - VERSIÓN MEJORADA")
    print("="*60)
    
    # URL del listado de productos de la tienda Viaje Azul (con barra final)
    url_inicial = "https://listado.mercadolibre.cl/pagina/ar20240628111129/"
    
    print(f"\n📍 URL objetivo: {url_inicial}")
    print(f"⚠️  NOTA: Respeta los términos de servicio de Mercado Libre")
    print(f"⏱️  La extracción de detalles hará el proceso más lento pero más completo\n")
    
    # Scrapear productos con detalles completos
    # Cambia extraer_detalles=False si solo quieres datos básicos (más rápido)
    print(f"Iniciando scraping de TODOS los productos de la tienda...")
    print(f"Esto puede tomar aproximadamente 20-25 minutos.\n")
    data = scrapear_tienda_ml(url_inicial, descargar_imagenes=True, extraer_detalles=True)
    
    # Guardar resultados
    if data:
        guardar_resultados(data, nombre_archivo='viaje_azul_productos')
    
    print("\n🎉 ¡Proceso completado!")
