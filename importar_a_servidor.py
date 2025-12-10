#!/usr/bin/env python3
"""
Script para importar productos al servidor mediante API REST
Hace peticiones POST a http://localhost:4000/api/products
"""

import json
import requests
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import time

# Importar configuración
try:
    from config_servidor import (
        API_URL,
        AUTH_TOKEN,
        MAX_REINTENTOS,
        DELAY_ENTRE_PRODUCTOS,
        TIMEOUT
    )
except ImportError:
    # Si no existe config_servidor.py, mostrar error
    print("❌ Error: No se encontró config_servidor.py")
    print("Por favor, copia config_servidor.example.py a config_servidor.py")
    print("y edita los valores con tu configuración real.")
    print("\nComandos:")
    print("  cp config_servidor.example.py config_servidor.py")
    print("  nano config_servidor.py  # Edita con tu token")
    import sys
    sys.exit(1)


def cargar_productos(archivo_json: str) -> List[Dict]:
    """Carga los productos desde el archivo JSON"""
    ruta = Path(archivo_json)
    
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {archivo_json}")
    
    with open(ruta, 'r', encoding='utf-8') as f:
        productos = json.load(f)
    
    return productos


def verificar_servidor(url: str) -> bool:
    """Verifica que el servidor esté accesible"""
    try:
        response = requests.get(url.replace('/api/products', '/'), timeout=5)
        return True
    except requests.exceptions.RequestException:
        return False


def importar_producto(producto: Dict, headers: Dict, reintento: int = 0) -> Tuple[bool, str]:
    """
    Importa un producto al servidor
    
    Args:
        producto: Diccionario con los datos del producto
        headers: Headers HTTP con autenticación
        reintento: Número de reintento actual
    
    Returns:
        Tuple (éxito, mensaje)
    """
    try:
        response = requests.post(
            API_URL,
            json=producto,
            headers=headers,
            timeout=TIMEOUT
        )
        
        if response.status_code == 201 or response.status_code == 200:
            return True, "✓ Producto creado exitosamente"
        
        elif response.status_code == 409:
            return False, "⚠ Producto ya existe (duplicado)"
        
        elif response.status_code == 401:
            return False, "❌ Error de autenticación - Token inválido o expirado"
        
        elif response.status_code == 400:
            error_msg = response.json().get('message', 'Error de validación')
            return False, f"❌ Datos inválidos: {error_msg}"
        
        else:
            return False, f"❌ Error HTTP {response.status_code}: {response.text[:100]}"
    
    except requests.exceptions.Timeout:
        if reintento < MAX_REINTENTOS:
            time.sleep(2 ** reintento)  # Backoff exponencial
            return importar_producto(producto, headers, reintento + 1)
        return False, "❌ Timeout - Servidor no responde"
    
    except requests.exceptions.ConnectionError:
        return False, "❌ Error de conexión - Verifica que el servidor esté corriendo"
    
    except Exception as e:
        return False, f"❌ Error inesperado: {str(e)}"


def importar_productos_a_servidor(
    archivo_json: str = "datos/json/productos_mercadolibre.json",
    generar_reporte: bool = True
):
    """
    Importa todos los productos al servidor
    
    Args:
        archivo_json: Ruta al archivo JSON con los productos
        generar_reporte: Si True, genera un reporte JSON con los resultados
    """
    
    print("=" * 70)
    print("📤 IMPORTADOR DE PRODUCTOS AL SERVIDOR")
    print("=" * 70)
    print()
    
    # Verificar servidor
    print(f"🔍 Verificando servidor: {API_URL}")
    if not verificar_servidor(API_URL):
        print("❌ Error: No se puede conectar al servidor")
        print(f"   Asegúrate de que el servidor esté corriendo en http://localhost:4000")
        return
    print("✓ Servidor accesible")
    print()
    
    # Cargar productos
    print(f"📂 Cargando productos desde: {archivo_json}")
    try:
        productos = cargar_productos(archivo_json)
        print(f"✓ {len(productos)} productos cargados")
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: El archivo JSON está malformado")
        return
    print()
    
    # Preparar headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }
    
    # Importar productos
    print("=" * 70)
    print("Iniciando importación...")
    print("=" * 70)
    print()
    
    exitosos = []
    fallidos = []
    duplicados = []
    
    inicio = time.time()
    
    for idx, producto in enumerate(productos, 1):
        nombre = producto.get('nombre', 'Sin nombre')
        sku = producto.get('sku', 'Sin SKU')
        
        print(f"[{idx}/{len(productos)}] {nombre[:50]}...")
        print(f"  SKU: {sku}")
        
        # Importar producto
        exito, mensaje = importar_producto(producto, headers)
        print(f"  {mensaje}")
        
        if exito:
            exitosos.append({
                'sku': sku,
                'nombre': nombre
            })
        elif "duplicado" in mensaje.lower() or "ya existe" in mensaje.lower():
            duplicados.append({
                'sku': sku,
                'nombre': nombre,
                'error': mensaje
            })
        else:
            fallidos.append({
                'sku': sku,
                'nombre': nombre,
                'error': mensaje
            })
        
        print()
        
        # Delay entre productos para no saturar el servidor
        if idx < len(productos):
            time.sleep(DELAY_ENTRE_PRODUCTOS)
    
    tiempo_total = time.time() - inicio
    
    # Resumen
    print("=" * 70)
    print("📊 RESUMEN DE IMPORTACIÓN")
    print("=" * 70)
    print(f"✅ Productos importados exitosamente: {len(exitosos)}")
    print(f"⚠️  Productos duplicados (ya existían): {len(duplicados)}")
    print(f"❌ Productos con errores: {len(fallidos)}")
    print(f"📦 Total procesados: {len(productos)}")
    print(f"⏱️  Tiempo total: {tiempo_total:.2f} segundos")
    print("=" * 70)
    
    # Mostrar errores si hay
    if fallidos:
        print()
        print("⚠️  PRODUCTOS CON ERRORES:")
        for item in fallidos[:10]:  # Mostrar primeros 10
            print(f"   • {item['sku']} - {item['nombre'][:40]}")
            print(f"     {item['error']}")
        if len(fallidos) > 10:
            print(f"   ... y {len(fallidos) - 10} más")
    
    # Generar reporte
    if generar_reporte:
        reporte = {
            'fecha_importacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'servidor': API_URL,
            'total_productos': len(productos),
            'exitosos': len(exitosos),
            'duplicados': len(duplicados),
            'fallidos': len(fallidos),
            'tiempo_segundos': round(tiempo_total, 2),
            'productos_exitosos': exitosos[:100],  # Primeros 100
            'productos_fallidos': fallidos,
            'productos_duplicados': duplicados[:100]
        }
        
        ruta_reporte = Path('datos/json') / f"reporte_importacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(ruta_reporte, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, ensure_ascii=False, indent=2)
        
        print()
        print(f"📄 Reporte guardado en: {ruta_reporte.name}")
    
    print()
    print("=" * 70)
    print("✅ IMPORTACIÓN COMPLETADA")
    print("=" * 70)
    
    return {
        'exitosos': len(exitosos),
        'duplicados': len(duplicados),
        'fallidos': len(fallidos)
    }


def importar_producto_individual(archivo_json: str):
    """
    Importa un producto individual desde un archivo JSON
    
    Args:
        archivo_json: Ruta al archivo JSON del producto individual
    """
    print(f"📤 Importando producto desde: {archivo_json}")
    
    try:
        with open(archivo_json, 'r', encoding='utf-8') as f:
            producto = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {archivo_json}")
        return
    except json.JSONDecodeError:
        print(f"❌ Error: El archivo JSON está malformado")
        return
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }
    
    exito, mensaje = importar_producto(producto, headers)
    
    print(f"Nombre: {producto.get('nombre', 'Sin nombre')}")
    print(f"SKU: {producto.get('sku', 'Sin SKU')}")
    print(mensaje)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Modo: importar un producto individual
        archivo = sys.argv[1]
        importar_producto_individual(archivo)
    else:
        # Modo: importar todos los productos
        importar_productos_a_servidor(
            archivo_json="datos/json/productos_mercadolibre.json",
            generar_reporte=True
        )
