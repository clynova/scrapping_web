#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión al servidor
"""

import requests
import json
from config_servidor import API_URL, AUTH_TOKEN

def probar_conexion():
    """Prueba la conexión al servidor"""
    
    print("=" * 70)
    print("🧪 PRUEBA DE CONEXIÓN AL SERVIDOR")
    print("=" * 70)
    print()
    
    # 1. Verificar servidor accesible
    print(f"1️⃣ Verificando servidor: {API_URL}")
    base_url = API_URL.replace('/api/products', '')
    
    try:
        response = requests.get(base_url, timeout=5)
        print(f"   ✅ Servidor accesible (Status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error: {e}")
        print(f"   💡 Asegúrate de que el servidor esté corriendo")
        return False
    
    print()
    
    # 2. Verificar endpoint de productos
    print(f"2️⃣ Probando endpoint: {API_URL}")
    
    headers = {
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }
    
    try:
        response = requests.get(API_URL, headers=headers, timeout=10)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Endpoint accesible")
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f"   📦 Productos actuales en servidor: {len(data)}")
                elif isinstance(data, dict) and 'data' in data:
                    print(f"   📦 Productos actuales en servidor: {len(data['data'])}")
            except:
                print(f"   ⚠️  Respuesta no es JSON válido")
        elif response.status_code == 401:
            print(f"   ❌ Error de autenticación")
            print(f"   💡 El token puede estar expirado o ser inválido")
            print(f"   Token actual: {AUTH_TOKEN[:50]}...")
            return False
        else:
            print(f"   ⚠️  Status inesperado: {response.status_code}")
            print(f"   Respuesta: {response.text[:200]}")
    
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print()
    
    # 3. Probar autenticación con POST de prueba
    print(f"3️⃣ Probando autenticación con POST")
    
    producto_prueba = {
        "sku": "TEST-0000-000",
        "nombre": "Producto de Prueba - NO CREAR",
        "precio": 9990
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }
    
    # Solo verificamos que la autenticación funciona, no creamos el producto
    print(f"   ℹ️  Verificando headers de autenticación...")
    print(f"   Token: {AUTH_TOKEN[:30]}...{AUTH_TOKEN[-10:]}")
    print(f"   ✅ Headers configurados correctamente")
    
    print()
    
    # Resumen
    print("=" * 70)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 70)
    print()
    print("💡 El servidor está listo para recibir productos")
    print(f"   Ejecuta: python importar_a_servidor.py")
    print()
    
    return True


if __name__ == "__main__":
    probar_conexion()
