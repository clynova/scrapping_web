#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversor de CSV de Mercado Libre a JSON según modelo de Producto
Transforma los datos extraídos del scraping a la estructura del modelo de base de datos
"""

import pandas as pd
import json
import re
from pathlib import Path
from typing import Dict, List, Any
import unicodedata
import random

def limpiar_texto(texto: str) -> str:
    """Limpia y normaliza texto"""
    if pd.isna(texto) or texto == "":
        return ""
    return str(texto).strip()

def generar_slug(nombre: str) -> str:
    """Genera slug a partir del nombre del producto"""
    # Normalizar unicode (quitar acentos)
    texto = unicodedata.normalize('NFKD', nombre)
    texto = texto.encode('ascii', 'ignore').decode('ascii')
    # Convertir a minúsculas
    texto = texto.lower()
    # Reemplazar espacios y caracteres especiales por guiones
    texto = re.sub(r'[^\w\s-]', '', texto)
    texto = re.sub(r'[-\s]+', '-', texto)
    return texto.strip('-')

def generar_sku_personalizado(nombre: str, categoria: str, subcategoria: str) -> str:
    """Genera SKU personalizado: NOM-CAT-SUB-###"""
    # Extraer primeras 3 letras del nombre (solo letras)
    nombre_limpio = re.sub(r'[^a-zA-Z]', '', nombre.upper())
    prefijo_nombre = nombre_limpio[:3] if len(nombre_limpio) >= 3 else nombre_limpio.ljust(3, 'X')
    
    # Primeras 3-4 letras de categoría
    categoria_limpio = re.sub(r'[^a-zA-Z]', '', categoria.upper())
    prefijo_cat = categoria_limpio[:4] if len(categoria_limpio) >= 4 else categoria_limpio.ljust(4, 'X')
    
    # Primeras 3 letras de subcategoría
    subcategoria_limpio = re.sub(r'[^a-zA-Z]', '', subcategoria.upper())
    prefijo_sub = subcategoria_limpio[:3] if len(subcategoria_limpio) >= 3 else subcategoria_limpio.ljust(3, 'X')
    
    # 3 números aleatorios
    numeros = random.randint(100, 999)
    
    # Formato: NOM-CAT-SUB-###
    sku = f"{prefijo_nombre}-{prefijo_cat}-{prefijo_sub}-{numeros}"
    
    return sku

def extraer_marca(caracteristicas: str) -> str:
    """Extrae la marca de las características"""
    if pd.isna(caracteristicas):
        return ""
    
    # Buscar "Marca: XXX"
    match = re.search(r'Marca:\s*([^|]+)', caracteristicas)
    if match:
        return match.group(1).strip()
    return ""

def parsear_caracteristicas(caracteristicas: str) -> Dict[str, Any]:
    """Convierte string de características en diccionario de atributos"""
    if pd.isna(caracteristicas) or caracteristicas == "":
        return {}
    
    atributos = {}
    # Dividir por pipe "|"
    partes = caracteristicas.split('|')
    
    for parte in partes:
        parte = parte.strip()
        if ':' in parte:
            clave, valor = parte.split(':', 1)
            clave = clave.strip()
            valor = valor.strip()
            
            # Intentar convertir a número si es posible
            try:
                if '.' in valor:
                    valor_num = float(valor)
                else:
                    valor_num = int(valor)
                atributos[clave] = valor_num
            except ValueError:
                atributos[clave] = valor
    
    return atributos

def extraer_tags(titulo: str, caracteristicas: str = "") -> List[str]:
    """Extrae tags relevantes del título y características"""
    tags = set()
    
    # Palabras comunes a ignorar
    stopwords = {'de', 'la', 'el', 'en', 'para', 'con', 'y', 'a', 'por', 'un', 'una', 
                 'los', 'las', 'del', 'al', 'que', 'se', 'su', 'producto', 'este', 'esta',
                 'son', 'más', 'todo', 'cada', 'como', 'desde', 'hasta', 'muy', 'otros',
                 'mismo', 'también', 'solo', 'puede', 'cada'}
    
    # Extraer palabras del título (mínimo 3 caracteres, no más de 20)
    palabras_titulo = re.findall(r'\b[a-záéíóúñ]{3,20}\b', titulo.lower())
    for palabra in palabras_titulo:
        if palabra not in stopwords and not palabra.isdigit():
            tags.add(palabra)
    
    # Extraer de características también
    if caracteristicas:
        palabras_caract = re.findall(r'\b[a-záéíóúñ]{4,20}\b', caracteristicas.lower())
        for palabra in palabras_caract[:5]:  # Solo las primeras 5
            if palabra not in stopwords and not palabra.isdigit():
                tags.add(palabra)
    
    # Limitar a máximo 10 tags más relevantes
    return sorted(list(tags))[:10]

def extraer_precio(precio_str: str) -> int:
    """Extrae el precio numérico del string como entero"""
    if pd.isna(precio_str):
        return 0
    
    # Eliminar símbolo $ y puntos de miles, convertir
    precio_limpio = re.sub(r'[^\d,]', '', str(precio_str))
    precio_limpio = precio_limpio.replace(',', '.')
    
    try:
        return int(float(precio_limpio))
    except ValueError:
        return 0

def generar_descripcion_corta(descripcion_completa: str, titulo: str) -> str:
    """Genera descripción corta (máx 160 chars)"""
    if pd.isna(descripcion_completa) or descripcion_completa == "":
        # Usar el título si no hay descripción
        return titulo[:160]
    
    # Tomar primeros 157 caracteres y agregar "..."
    desc = descripcion_completa.strip()
    if len(desc) <= 160:
        return desc
    
    return desc[:157] + "..."

def convertir_producto_a_json(row: pd.Series, ruta_imagenes: str = "datos/imagenes") -> Dict[str, Any]:
    """Convierte una fila del CSV al formato JSON del modelo"""
    
    # Extraer datos básicos
    nombre = limpiar_texto(row.get('Titulo', 'Producto sin nombre'))
    categoria = "OTROS"
    subcategoria = "Varios"
    
    # Generar SKU personalizado
    sku = generar_sku_personalizado(nombre, categoria, subcategoria)
    slug = generar_slug(nombre)
    
    # Descripción
    descripcion_completa = limpiar_texto(row.get('Descripcion', ''))
    descripcion_corta = generar_descripcion_corta(descripcion_completa, nombre)
    
    # Características
    caract_principales = limpiar_texto(row.get('Caracteristicas_Principales', ''))
    caract_ventas = limpiar_texto(row.get('Caracteristicas_Ventas', ''))
    otras_caract = limpiar_texto(row.get('Otras_Caracteristicas', ''))
    
    # Combinar todas las características para atributos
    todas_caracteristicas = ' | '.join(filter(None, [caract_principales, caract_ventas, otras_caract]))
    atributos = parsear_caracteristicas(todas_caracteristicas)
    
    # Marca
    marca = extraer_marca(caract_principales)
    
    # Tags
    tags = extraer_tags(nombre, todas_caracteristicas)
    
    # Precio
    precio = extraer_precio(row.get('Precio', '0'))
    
    # Imágenes - Priorizar imagen externa, si no existe usar local
    imagenes = []
    url_imagen = limpiar_texto(row.get('URL_Imagen', ''))
    imagen_local = limpiar_texto(row.get('Imagen_Local', ''))
    
    # Usar solo UNA imagen - preferir la externa si existe, sino la local
    if url_imagen:
        imagenes.append({
            "url": url_imagen,
            "textoAlternativo": nombre,
            "esPrincipal": True
        })
    elif imagen_local:
        # Convertir ruta de imagenes_mercadolibre/ a datos/imagenes/
        nombre_archivo = Path(imagen_local).name
        ruta_relativa = f"{ruta_imagenes}/{nombre_archivo}"
        
        imagenes.append({
            "url": ruta_relativa,
            "textoAlternativo": nombre,
            "esPrincipal": True
        })
    
    # Variante predeterminada con SKU basado en el SKU principal
    variantes = [{
        "nombre": "Estándar",
        "unidad": "unidades",
        "precio": precio,
        "descuento": 0,
        "sku": f"{sku}-VAR001",
        "esPredeterminado": True
    }]
    
    # SEO
    seo = {
        "metaTitulo": nombre[:60],
        "metaDescripcion": descripcion_corta,
        "palabrasClave": tags[:5]
    }
    
    # Construir objeto producto según el modelo
    producto = {
        "sku": sku,
        "nombre": nombre,
        "slug": slug,
        "categoria": categoria,
        "subcategoria": subcategoria,
        "descripcion": {
            "corta": descripcion_corta,
            "completa": descripcion_completa if descripcion_completa else None
        },
        "multimedia": {
            "imagenes": imagenes
        },
        "estado": True,
        "tags": tags,
        "variantes": variantes,
        "atributos": atributos if atributos else {},
        "seo": seo,
        "marca": marca if marca else None,
        "origen": None,
        "vidaUtil": None,
        "requiereRefrigeracion": False,
        "ratingAverage": 0
    }
    
    # Eliminar campos None para mantener el JSON limpio
    return {k: v for k, v in producto.items() if v is not None and v != ""}

def convertir_csv_a_json_incremental(
    archivo_csv: str,
    carpeta_salida: str = "datos/json",
    archivo_salida: str = "productos_mercadolibre.json",
    generar_individuales: bool = True
):
    """
    Convierte el CSV a JSON de manera incremental, sin eliminar productos existentes
    
    Args:
        archivo_csv: Ruta al archivo CSV con los datos
        carpeta_salida: Carpeta donde guardar los JSON
        archivo_salida: Nombre del archivo JSON con todos los productos
        generar_individuales: Si True, genera un JSON por cada producto
    """
    from datetime import datetime
    
    print(f"📂 Leyendo archivo CSV: {archivo_csv}")
    df = pd.read_csv(archivo_csv)
    
    print(f"📊 Total de productos en CSV: {len(df)}")
    
    # Crear carpeta de salida si no existe
    Path(carpeta_salida).mkdir(parents=True, exist_ok=True)
    
    # Leer productos existentes
    ruta_consolidado = Path(carpeta_salida) / archivo_salida
    productos_existentes = {}
    productos_anteriores = 0
    
    if ruta_consolidado.exists():
        print(f"📋 Cargando productos existentes...")
        with open(ruta_consolidado, 'r', encoding='utf-8') as f:
            productos_list = json.load(f)
            productos_anteriores = len(productos_list)
            # Usar el título como clave única para identificar duplicados
            for p in productos_list:
                productos_existentes[p['nombre']] = p
        print(f"  ✅ {productos_anteriores} productos existentes cargados")
    
    # Convertir productos nuevos
    productos_nuevos = []
    productos_ignorados = []
    skus_nuevos = []
    
    for idx, row in df.iterrows():
        nombre = limpiar_texto(row.get('Titulo', 'Producto sin nombre'))
        
        # Verificar si el producto ya existe
        if nombre in productos_existentes:
            productos_ignorados.append(nombre)
            continue
        
        # Producto nuevo - convertir
        producto = convertir_producto_a_json(row)
        productos_existentes[nombre] = producto
        productos_nuevos.append(producto)
        skus_nuevos.append(producto['sku'])
        
        # Generar JSON individual si se solicita
        if generar_individuales:
            nombre_archivo = f"{producto['sku']}_{producto['slug'][:30]}.json"
            ruta_archivo = Path(carpeta_salida) / nombre_archivo
            
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(producto, f, ensure_ascii=False, indent=2)
        
        if (idx + 1) % 10 == 0:
            print(f"  ⏳ Procesados {idx + 1}/{len(df)} productos...")
    
    # Guardar archivo consolidado actualizado
    print(f"\n💾 Actualizando archivo consolidado: {archivo_salida}")
    todos_productos = list(productos_existentes.values())
    
    with open(ruta_consolidado, 'w', encoding='utf-8') as f:
        json.dump(todos_productos, f, ensure_ascii=False, indent=2)
    
    # Generar reporte
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reporte = {
        "fecha_actualizacion": fecha_hora,
        "productos_anteriores": productos_anteriores,
        "productos_nuevos": len(productos_nuevos),
        "productos_ignorados": len(productos_ignorados),
        "total_productos": len(todos_productos),
        "skus_nuevos": skus_nuevos,
        "nombres_ignorados": productos_ignorados[:10] if len(productos_ignorados) > 10 else productos_ignorados
    }
    
    # Guardar reporte
    ruta_reporte = Path(carpeta_salida) / f"reporte_actualizacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(ruta_reporte, 'w', encoding='utf-8') as f:
        json.dump(reporte, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Conversión incremental completada!")
    print(f"\n📊 RESUMEN:")
    print(f"   • Productos anteriores: {productos_anteriores}")
    print(f"   • Productos nuevos agregados: {len(productos_nuevos)}")
    print(f"   • Productos ignorados (duplicados): {len(productos_ignorados)}")
    print(f"   • Total productos ahora: {len(todos_productos)}")
    
    if skus_nuevos:
        print(f"\n🆕 SKUs de productos nuevos:")
        for sku in skus_nuevos[:10]:
            print(f"   • {sku}")
        if len(skus_nuevos) > 10:
            print(f"   ... y {len(skus_nuevos) - 10} más")
    
    print(f"\n📄 Reporte guardado en: {ruta_reporte.name}")
    
    return reporte

def convertir_csv_a_json(
    archivo_csv: str,
    carpeta_salida: str = "datos/json",
    archivo_salida: str = "productos.json",
    generar_individuales: bool = True
):
    """
    Convierte el CSV de productos a JSON según el modelo
    
    Args:
        archivo_csv: Ruta al archivo CSV con los datos
        carpeta_salida: Carpeta donde guardar los JSON
        archivo_salida: Nombre del archivo JSON con todos los productos
        generar_individuales: Si True, genera un JSON por cada producto
    """
    
    print(f"📂 Leyendo archivo: {archivo_csv}")
    df = pd.read_csv(archivo_csv)
    
    print(f"📊 Total de productos en CSV: {len(df)}")
    
    # Crear carpeta de salida si no existe
    Path(carpeta_salida).mkdir(parents=True, exist_ok=True)
    
    productos_json = []
    
    # Convertir cada producto
    for idx, row in df.iterrows():
        producto = convertir_producto_a_json(row)
        productos_json.append(producto)
        
        # Generar JSON individual si se solicita
        if generar_individuales:
            nombre_archivo = f"{producto['sku']}_{producto['slug'][:30]}.json"
            ruta_archivo = Path(carpeta_salida) / nombre_archivo
            
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(producto, f, ensure_ascii=False, indent=2)
            
            if (idx + 1) % 10 == 0:
                print(f"  ✅ Procesados {idx + 1}/{len(df)} productos")
    
    print(f"\n💾 Guardando archivo consolidado: {archivo_salida}")
    
    # Guardar todos los productos en un solo archivo
    ruta_consolidado = Path(carpeta_salida) / archivo_salida
    with open(ruta_consolidado, 'w', encoding='utf-8') as f:
        json.dump(productos_json, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Conversión completada!")
    print(f"📁 Archivos generados en: {carpeta_salida}/")
    print(f"   - {archivo_salida} (todos los productos)")
    if generar_individuales:
        print(f"   - {len(productos_json)} archivos individuales")
    
    # Mostrar estadísticas
    print(f"\n📈 Estadísticas:")
    print(f"   • Total productos: {len(productos_json)}")
    
    productos_con_descripcion = sum(1 for p in productos_json if p.get('descripcion', {}).get('completa'))
    print(f"   • Con descripción: {productos_con_descripcion}/{len(productos_json)}")
    
    productos_con_marca = sum(1 for p in productos_json if p.get('marca'))
    print(f"   • Con marca: {productos_con_marca}/{len(productos_json)}")
    
    productos_con_imagen = sum(1 for p in productos_json if p.get('multimedia', {}).get('imagenes'))
    print(f"   • Con imágenes: {productos_con_imagen}/{len(productos_json)}")
    
    total_tags = sum(len(p.get('tags', [])) for p in productos_json)
    print(f"   • Total de tags: {total_tags}")
    
    # Mostrar ejemplo de producto
    if productos_json:
        print(f"\n📦 Ejemplo de producto convertido:")
        print(f"   Nombre: {productos_json[0]['nombre']}")
        print(f"   SKU: {productos_json[0]['sku']}")
        print(f"   Slug: {productos_json[0]['slug']}")
        print(f"   Precio: ${productos_json[0]['variantes'][0]['precio']:,.0f}")
        print(f"   Tags: {', '.join(productos_json[0]['tags'][:5])}")
        print(f"   Marca: {productos_json[0].get('marca', 'N/A')}")
    
    return productos_json

if __name__ == "__main__":
    import sys
    
    print("=" * 70)
    print("🔄 CONVERSOR DE CSV A JSON - MODO INCREMENTAL")
    print("=" * 70)
    print()
    
    # Determinar qué archivo CSV usar
    archivo_csv_base = "datos/csv/viaje_azul_productos.csv"
    archivo_csv_detallado = "datos/csv/viaje_azul_productos_con_detalles.csv"
    
    # Usar el archivo con detalles si existe
    if Path(archivo_csv_detallado).exists():
        archivo_csv = archivo_csv_detallado
        print("📋 Usando CSV con detalles completos")
    elif Path(archivo_csv_base).exists():
        archivo_csv = archivo_csv_base
        print("📋 Usando CSV básico")
    else:
        print("❌ Error: No se encontró ningún archivo CSV en datos/csv/")
        print("   Esperado: viaje_azul_productos_con_detalles.csv o viaje_azul_productos.csv")
        sys.exit(1)
    
    print()
    
    # Convertir en modo incremental (preserva productos existentes)
    reporte = convertir_csv_a_json_incremental(
        archivo_csv=archivo_csv,
        carpeta_salida="datos/json",
        archivo_salida="productos_mercadolibre.json",
        generar_individuales=True
    )
    
    print()
    print("=" * 70)
    print("✅ PROCESO COMPLETADO")
    print("=" * 70)
