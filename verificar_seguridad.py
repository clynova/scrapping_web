#!/usr/bin/env python3
"""
Script para verificar que no hay tokens en el código
Ejecuta este script ANTES de hacer git push
"""

import os
import sys
from pathlib import Path

def verificar_seguridad():
    """Verifica que no hay tokens expuestos en el código"""
    
    print("=" * 70)
    print("🔒 VERIFICACIÓN DE SEGURIDAD - TOKENS EN CÓDIGO")
    print("=" * 70)
    print()
    
    problemas = []
    avisos = []
    
    # 1. Verificar que config_servidor.py está en .gitignore
    print("1️⃣  Verificando .gitignore...")
    gitignore_path = Path(".gitignore")
    if gitignore_path.exists():
        with open(".gitignore", "r") as f:
            gitignore_content = f.read()
        if "config_servidor.py" in gitignore_content:
            print("   ✅ config_servidor.py está en .gitignore")
        else:
            problemas.append("❌ config_servidor.py NO está en .gitignore")
            print(f"   {problemas[-1]}")
    else:
        avisos.append("⚠️  No se encontró .gitignore")
        print(f"   {avisos[-1]}")
    
    print()
    
    # 2. Verificar que archivos Python no tienen tokens hardcodeados
    print("2️⃣  Buscando tokens en archivos Python...")
    
    archivos_python = list(Path(".").glob("*.py"))
    archivos_sin_config = [f for f in archivos_python if f.name not in ["config_servidor.py", "verificar_seguridad.py"]]
    
    tokens_encontrados = False
    for archivo in archivos_sin_config:
        with open(archivo, "r") as f:
            contenido = f.read()
        
        # Buscar patrones de JWT (excluyendo comentarios con ejemplos)
        lineas = contenido.split('\n')
        for num_linea, linea in enumerate(lineas, 1):
            # Saltarse comentarios
            if linea.strip().startswith('#'):
                continue
            # Buscar token real (no en strings de ejemplo)
            if 'AUTH_TOKEN = "eyJhbGc' in linea or "AUTH_TOKEN = 'eyJhbGc" in linea:
                problemas.append(f"❌ Token JWT hardcodeado en {archivo.name}:{num_linea}")
                print(f"   {problemas[-1]}")
                tokens_encontrados = True
    
    if not tokens_encontrados:
        print("   ✅ No se encontraron tokens JWT hardcodeados en archivos Python")
    
    print()
    
    # 3. Verificar que config_servidor.py existe
    print("3️⃣  Verificando archivos de configuración...")
    
    if Path("config_servidor.py").exists():
        print("   ✅ config_servidor.py existe (LOCAL)")
    else:
        avisos.append("⚠️  config_servidor.py no existe localmente")
        print(f"   {avisos[-1]}")
        print("   💡 Ejecuta: cp config_servidor.example.py config_servidor.py")
    
    if Path("config_servidor.example.py").exists():
        # Verificar que example no tiene token real
        with open("config_servidor.example.py", "r") as f:
            example_content = f.read()
        
        if "eyJhbGc" not in example_content:
            print("   ✅ config_servidor.example.py es seguro (sin token real)")
        else:
            problemas.append("❌ config_servidor.example.py contiene token real")
            print(f"   {problemas[-1]}")
    else:
        print("   ⚠️  config_servidor.example.py no existe")
    
    print()
    
    # 4. Resumen
    print("=" * 70)
    print("📊 RESUMEN")
    print("=" * 70)
    
    if problemas:
        print()
        print("❌ PROBLEMAS ENCONTRADOS:")
        for problema in problemas:
            print(f"   {problema}")
        print()
        print("⚠️  NO HAGAS PUSH A GITHUB HASTA RESOLVER ESTOS PROBLEMAS")
        return False
    
    if avisos:
        print()
        print("⚠️  AVISOS:")
        for aviso in avisos:
            print(f"   {aviso}")
    
    print()
    print("✅ SEGURIDAD VERIFICADA")
    print("   Puedes hacer push a GitHub de forma segura")
    return True

if __name__ == "__main__":
    es_seguro = verificar_seguridad()
    sys.exit(0 if es_seguro else 1)
