#!/usr/bin/env python3
# Script para scrapear con límite de productos

import sys
import os

# Agregar directorio al path
sys.path.insert(0, '/home/clynova/proyectos/scrapping_web')

print("\n" + "="*70)
print(" SCRAPER DE MERCADO LIBRE - EXTRACCIÓN CON DETALLES")
print("="*70)

url_inicial = "https://listado.mercadolibre.cl/pagina/ar20240628111129/"

print(f"\n📍 URL: {url_inicial}")
print("⚙️  Configuración:")
print("   • Descargar imágenes: SÍ")
print("   • Extraer detalles: SÍ")
print("   • Límite: 10 productos (para prueba rápida)")
print("\n⏱️  Tiempo estimado: 3-5 minutos")
print("⚠️  NOTA: El scraper completo (48 productos) tomará ~15-20 minutos\n")

input("Presiona ENTER para continuar o Ctrl+C para cancelar...")

import requests
from bs4 import BeautifulSoup
from scraper_mercadolibre_v2 import extraer_detalles_producto, descargar_imagen, guardar_resultados
import time
from urllib.parse import urljoin
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-CL,es;q=0.9',
    'DNT': '1',
    'Connection': 'keep-alive',
}

print("\n" + "="*70)
print("Iniciando scraping...")
print("="*70)

response = requests.get(url_inicial, headers=headers)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

items = soup.find_all('li', class_='ui-search-layout__item')[:10]  # Limitar a 10

print(f"\n✓ Encontrados {len(items)} productos para procesar\n")

productos = []
carpeta_imagenes = 'imagenes_mercadolibre'

for idx, item in enumerate(items, 1):
    print(f"[{idx}/{len(items)}] Procesando producto...")
    
    # Título - buscar en múltiples lugares
    titulo = ""
    titulo_elem = item.find('a', class_=re.compile(r'poly-component__title'))
    if titulo_elem:
        titulo = titulo_elem.text.strip()
    
    if not titulo:
        titulo_elem = item.find('h2')
        if titulo_elem:
            titulo = titulo_elem.text.strip()
    
    if not titulo:
        titulo_elem = item.find('a', title=True)
        if titulo_elem:
            titulo = titulo_elem.get('title', '').strip()
    
    if not titulo:
        titulo = f"Producto {idx}"
    
    print(f"  📦 {titulo[:65]}...")
    
    # Precio
    precio = "0"
    precio_elem = item.find('span', class_='andes-money-amount__fraction')
    if precio_elem:
        precio = precio_elem.text.strip().replace('.', '').replace(',', '')
    
    # Link
    link_elem = item.find('a', href=True)
    link = link_elem.get('href', '') if link_elem else ""
    if link and not link.startswith('http'):
        link = urljoin(url_inicial, link)
    
    # Imagen
    url_imagen = ""
    ruta_imagen_local = ""
    img_elem = item.find('img')
    if img_elem:
        url_imagen = img_elem.get('data-src') or img_elem.get('src', '')
        if url_imagen and not url_imagen.startswith('data:'):
            ruta_imagen_local = descargar_imagen(url_imagen, carpeta_imagenes, titulo, idx)
    
    # Crear producto base
    producto = {
        'ID': idx,
        'Titulo': titulo,
        'Precio': precio,
        'Link': link,
        'URL_Imagen': url_imagen,
        'Imagen_Local': ruta_imagen_local,
        'Descripcion': '',
        'Caracteristicas_Principales': '',
        'Caracteristicas_Ventas': '',
        'Otras_Caracteristicas': ''
    }
    
    # Extraer detalles
    if link:
        detalles = extraer_detalles_producto(link, headers)
        producto['Descripcion'] = detalles['Descripcion']
        
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
    print(f"  ✓ Completado\n")
    
    # Pausa entre productos
    if idx < len(items):
        time.sleep(1)

# Guardar resultados
print("\n" + "="*70)
print("Guardando resultados...")
print("="*70)

guardar_resultados(productos, nombre_archivo='viaje_azul_productos_con_detalles')

print("\n" + "="*70)
print("✅ SCRAPING COMPLETADO")
print("="*70)
print("\n📄 Archivos generados:")
print("   • viaje_azul_productos_con_detalles.xlsx")
print("   • viaje_azul_productos_con_detalles.csv")
print(f"   • {len([f for f in os.listdir(carpeta_imagenes) if f.endswith('.jpg')])} imágenes en {carpeta_imagenes}/")
print("\n💡 Para ver los datos:")
print("   libreoffice viaje_azul_productos_con_detalles.xlsx")
