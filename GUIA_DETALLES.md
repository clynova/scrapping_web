# Guía de Uso - Scraper con Detalles de Productos

## 🎯 Nueva Funcionalidad Agregada

El scraper ahora puede extraer información detallada de cada producto visitando su página individual:

- ✅ **Descripción completa** del producto
- ✅ **Características principales** (marca, modelo, color, etc.)
- ✅ **Características de venta** (garantía, envío, etc.)
- ✅ **Otras características** (especificaciones técnicas)

---

## ⚡ Formas de Ejecutar

### 1️⃣ Scraping Completo con Detalles (Recomendado)

```bash
cd /home/clynova/proyectos/scrapping_web
source venv/bin/activate
python scraper_mercadolibre_v2.py
```

**Tiempo estimado:** 15-20 minutos para 48 productos  
**Resultado:** Datos completos con todas las características

### 2️⃣ Scraping Rápido (Solo 10 productos con detalles)

```bash
python scraper_con_detalles_limitado.py
```

**Tiempo estimado:** 3-5 minutos  
**Resultado:** Muestra de 10 productos con todos los detalles

### 3️⃣ Scraping Básico Sin Detalles (Más Rápido)

Edita `scraper_mercadolibre_v2.py` y cambia la línea:
```python
data = scrapear_tienda_ml(url_inicial, descargar_imagenes=True, extraer_detalles=False)
```

**Tiempo estimado:** 2-3 minutos  
**Resultado:** Solo datos básicos (sin descripción ni características)

---

## 📊 Datos Extraídos

### Datos Básicos (siempre incluidos):
- ID del producto
- Título
- Precio
- Condición
- Ubicación
- Envío
- Link directo
- URL de imagen
- Imagen local descargada

### Datos Detallados (cuando `extraer_detalles=True`):
- **Descripción:** Texto descriptivo del producto
- **Características Principales:** Marca, modelo, color, dimensiones, etc.
- **Características de Venta:** Garantía, devoluciones, envío gratis, etc.
- **Otras Características:** Especificaciones técnicas adicionales

---

## 📁 Archivos Generados

### Con Detalles:
```
viaje_azul_productos_con_detalles.xlsx  (Excel completo)
viaje_azul_productos_con_detalles.csv   (CSV para análisis)
imagenes_mercadolibre/                   (Carpeta con imágenes)
```

### Sin Detalles:
```
viaje_azul_productos.xlsx
viaje_azul_productos.csv
imagenes_mercadolibre/
```

---

## 🔧 Configuración Avanzada

### Cambiar Número de Productos a Extraer

En `scraper_con_detalles_limitado.py`, línea 47:
```python
items = soup.find_all('li', class_='ui-search-layout__item')[:10]  # Cambiar el 10
```

### Deshabilitar Descarga de Imágenes

```python
data = scrapear_tienda_ml(url_inicial, descargar_imagenes=False, extraer_detalles=True)
```

### Solo Extraer Detalles Sin Imágenes

```python
data = scrapear_tienda_ml(url_inicial, descargar_imagenes=False, extraer_detalles=True)
```

### Cambiar URL de la Tienda

En `scraper_mercadolibre_v2.py`, busca:
```python
url_inicial = "https://listado.mercadolibre.cl/pagina/ar20240628111129/"
```

Reemplaza con la URL que desees scrapear.

---

## 📖 Ejemplos de Uso en Python

### Ejemplo 1: Scraping Programático

```python
from scraper_mercadolibre_v2 import scrapear_tienda_ml, guardar_resultados

# Scrapear con detalles
url = "https://listado.mercadolibre.cl/pagina/ar20240628111129/"
productos = scrapear_tienda_ml(url, descargar_imagenes=True, extraer_detalles=True)

# Guardar
guardar_resultados(productos, nombre_archivo='mi_scraping')
```

### Ejemplo 2: Filtrar Productos por Precio

```python
import pandas as pd

# Leer datos
df = pd.read_excel('viaje_azul_productos_con_detalles.xlsx')

# Filtrar productos con precio < $20000
baratos = df[df['Precio'].astype(float) < 20000]

# Guardar filtrados
baratos.to_excel('productos_baratos.xlsx', index=False)
print(f"Productos encontrados: {len(baratos)}")
```

### Ejemplo 3: Analizar Características

```python
import pandas as pd

df = pd.read_excel('viaje_azul_productos_con_detalles.xlsx')

# Productos con descripción
con_desc = df[df['Descripcion'].notna() & (df['Descripcion'] != '')]
print(f"Productos con descripción: {len(con_desc)}/{len(df)}")

# Productos con características principales
con_caract = df[df['Caracteristicas_Principales'].notna() & (df['Caracteristicas_Principales'] != '')]
print(f"Productos con características: {len(con_caract)}/{len(df)}")

# Mostrar marcas encontradas
for idx, row in df.iterrows():
    if 'Marca:' in str(row['Caracteristicas_Principales']):
        # Extraer marca
        import re
        match = re.search(r'Marca: ([^|]+)', row['Caracteristicas_Principales'])
        if match:
            print(f"Producto: {row['Titulo'][:40]}... - Marca: {match.group(1).strip()}")
```

---

## ⏱️ Tiempos de Ejecución Estimados

| Modo | Productos | Detalles | Imágenes | Tiempo |
|------|-----------|----------|----------|--------|
| Completo | 48 | ✅ | ✅ | ~20 min |
| Completo | 48 | ❌ | ✅ | ~3 min |
| Limitado | 10 | ✅ | ✅ | ~5 min |
| Limitado | 10 | ❌ | ✅ | ~1 min |

---

## ⚠️ Consideraciones

### Velocidad vs Completitud
- **Con detalles:** Más completo pero más lento (visita cada página de producto)
- **Sin detalles:** Más rápido pero con menos información

### Pausas Entre Peticiones
El scraper incluye pausas automáticas para:
- ✅ No saturar el servidor de Mercado Libre
- ✅ Evitar bloqueos por IP
- ✅ Ser ético con el scraping

**No modifiques** los tiempos de espera a menos que sea necesario.

### Bloqueos
Si el scraper es bloqueado:
1. Aumenta el tiempo de espera entre peticiones
2. Cambia el User-Agent
3. Usa un proxy o VPN
4. Espera unas horas antes de volver a intentar

---

## 🐛 Solución de Problemas

### Error: No se encuentran características

**Causa:** La estructura HTML de Mercado Libre cambió

**Solución:** El scraper intenta múltiples métodos de extracción. Si falla:
1. Inspecciona la página del producto con el navegador
2. Busca las nuevas clases CSS
3. Actualiza la función `extraer_detalles_producto()`

### Datos incompletos

**Normal:** No todos los productos tienen todas las características

**Verifica:**
- Visita manualmente la URL del producto
- Confirma que la información existe en la página
- Algunos vendedores no completan todos los campos

### Scraping muy lento

**Reduce productos:**
- Usa el script limitado
- Deshabilita extracción de detalles
- Deshabilita descarga de imágenes

---

## 📞 Archivos del Proyecto

| Archivo | Descripción |
|---------|-------------|
| `scraper_mercadolibre_v2.py` | Scraper principal con detalles |
| `scraper_con_detalles_limitado.py` | Versión limitada a 10 productos |
| `test_detalles.py` | Script de prueba de extracción |
| `ejecutar_scraper.py` | Ejecutor automático |
| `run.sh` | Script bash de inicio rápido |

---

## ✅ Checklist de Verificación

Antes de ejecutar el scraper completo:

- [ ] Probé con `test_detalles.py` y funciona
- [ ] Probé con `scraper_con_detalles_limitado.py`
- [ ] Verifiqué que los datos son correctos
- [ ] Tengo espacio en disco para imágenes
- [ ] Tengo tiempo suficiente (~20 minutos)
- [ ] La URL de la tienda es correcta

---

¡Todo listo para extraer datos completos de Mercado Libre! 🎉
