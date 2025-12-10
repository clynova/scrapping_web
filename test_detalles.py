#!/usr/bin/env python3
# Script de prueba - Extrae solo los primeros 5 productos para verificar funcionalidad

import sys
sys.path.insert(0, '/home/clynova/proyectos/scrapping_web')

from scraper_mercadolibre_v2 import scrapear_tienda_ml, guardar_resultados

print("\n" + "="*70)
print(" PRUEBA DE SCRAPER CON DETALLES - 5 PRODUCTOS")
print("="*70)

url_inicial = "https://listado.mercadolibre.cl/pagina/ar20240628111129/"

print(f"\n📍 URL: {url_inicial}")
print("🔧 Extrayendo primeros productos con detalles completos...")
print("⏱️  Esto tomará aproximadamente 1-2 minutos\n")

# Modificar temporalmente para obtener solo los primeros productos
import requests
from bs4 import BeautifulSoup
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'es-CL,es;q=0.9,en;q=0.8',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Importar función de detalles
from scraper_mercadolibre_v2 import extraer_detalles_producto

response = requests.get(url_inicial, headers=headers)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

items = soup.find_all('li', class_='ui-search-layout__item')[:5]

print(f"✓ Encontrados {len(items)} productos para probar\n")

# Probar con el primer producto
for idx, item in enumerate(items[:3], 1):
    print(f"{'='*70}")
    print(f"PRODUCTO {idx}/3")
    print(f"{'='*70}")
    
    # Título - buscar en múltiples lugares
    import re
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
        titulo = "Sin título"
    
    print(f"📦 Título: {titulo}")
    
    # Link
    link_elem = item.find('a', href=True)
    link = link_elem.get('href', '') if link_elem else ""
    if link and not link.startswith('http'):
        from urllib.parse import urljoin
        link = urljoin(url_inicial, link)
    
    print(f"🔗 Link: {link[:80]}...")
    
    if link:
        print("\n🔍 Extrayendo detalles...")
        detalles = extraer_detalles_producto(link, headers)
        
        print(f"\n📝 Descripción ({len(detalles['Descripcion'])} chars):")
        if detalles['Descripcion']:
            print(f"   {detalles['Descripcion'][:200]}...")
        else:
            print("   (No disponible)")
        
        print(f"\n⚙️  Características Principales ({len(detalles['Caracteristicas_Principales'])} items):")
        if detalles['Caracteristicas_Principales']:
            for key, value in list(detalles['Caracteristicas_Principales'].items())[:3]:
                print(f"   • {key}: {value}")
            if len(detalles['Caracteristicas_Principales']) > 3:
                print(f"   ... y {len(detalles['Caracteristicas_Principales']) - 3} más")
        else:
            print("   (No disponible)")
        
        print(f"\n💼 Características de Venta ({len(detalles['Caracteristicas_Ventas'])} items):")
        if detalles['Caracteristicas_Ventas']:
            for key, value in list(detalles['Caracteristicas_Ventas'].items())[:3]:
                print(f"   • {key}: {value}")
        else:
            print("   (No disponible)")
        
        print(f"\n🔧 Otras Características ({len(detalles['Otras_Caracteristicas'])} items):")
        if detalles['Otras_Caracteristicas']:
            for key, value in list(detalles['Otras_Caracteristicas'].items())[:3]:
                print(f"   • {key}: {value}")
            if len(detalles['Otras_Caracteristicas']) > 3:
                print(f"   ... y {len(detalles['Otras_Caracteristicas']) - 3} más")
        else:
            print("   (No disponible)")
        
        print("\n⏳ Esperando 2 segundos antes del siguiente producto...")
        time.sleep(2)

print("\n" + "="*70)
print("✅ PRUEBA COMPLETADA")
print("="*70)
print("\n💡 Si los resultados son correctos, ejecuta el scraper completo con:")
print("   python scraper_mercadolibre_v2.py")
