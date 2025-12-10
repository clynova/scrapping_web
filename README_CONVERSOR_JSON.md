# 📦 Conversor de CSV a JSON - Modelo de Productos

## 🎯 Descripción

Script que transforma los datos extraídos del scraper de Mercado Libre a un formato JSON compatible con el modelo de productos de MongoDB/Mongoose.

## 📁 Estructura de Carpetas

```
proyectos/scrapping_web/
├── datos/
│   ├── csv/                          # Archivos CSV originales
│   │   ├── viaje_azul_productos.csv  # CSV básico (48 productos)
│   │   └── viaje_azul_productos_con_detalles.csv  # CSV con detalles (10 productos)
│   │
│   ├── imagenes/                     # Imágenes descargadas
│   │   ├── 1_Producto_1.jpg
│   │   ├── 2_Producto_2.jpg
│   │   └── ...
│   │
│   └── json/                         # JSON generados
│       ├── productos_mercadolibre.json  # Todos los productos en un array
│       ├── 1_producto-1.json         # Producto individual
│       ├── 2_producto-2.json
│       └── ...
│
├── conversor_a_json.py              # Script principal de conversión
└── README_CONVERSOR_JSON.md         # Esta documentación
```

## 🚀 Uso Rápido

### Conversión automática:
```bash
cd /home/clynova/proyectos/scrapping_web
source venv/bin/activate
python conversor_a_json.py
```

El script automáticamente:
- ✅ Busca el CSV con detalles en `datos/csv/`
- ✅ Genera JSON individuales por producto
- ✅ Genera JSON consolidado con todos los productos
- ✅ Muestra estadísticas de conversión

## 📊 Mapeo de Campos

### Del CSV al Modelo JSON:

| Campo CSV | Campo JSON | Tipo | Notas |
|-----------|------------|------|-------|
| `ID` | `sku` | string | Identificador único |
| `Titulo` | `nombre` | string | Nombre del producto |
| - | `slug` | string | Generado automáticamente del nombre |
| - | `categoria` | string | Siempre "Otros" |
| - | `subcategoria` | string | Siempre "Varios" |
| `Descripcion` | `descripcion.completa` | string | Descripción completa |
| `Descripcion` (160 chars) | `descripcion.corta` | string | Extracto para SEO |
| `URL_Imagen` | `multimedia.imagenes[0].url` | string | Imagen principal (externa) |
| `Imagen_Local` | `multimedia.imagenes[1].url` | string | Imagen descargada (local) |
| `Precio` | `variantes[0].precio` | number | Precio numérico sin formato |
| `Caracteristicas_Principales` | `atributos` | object | Parseado a key-value |
| `Caracteristicas_Principales` | `marca` | string | Extraído de "Marca: XXX" |
| `Titulo` + Características | `tags` | array | Palabras clave relevantes |
| - | `estado` | boolean | Siempre `true` |
| - | `requiereRefrigeracion` | boolean | Siempre `false` |
| - | `ratingAverage` | number | Siempre `0` |

## 🔧 Características del Conversor

### ✨ Funciones Principales:

1. **Generación de Slug**
   - Elimina acentos y caracteres especiales
   - Convierte a minúsculas
   - Reemplaza espacios por guiones

2. **Extracción de Marca**
   - Busca patrón "Marca: XXX" en características
   - Extrae automáticamente el valor

3. **Parseo de Características**
   - Convierte string "Marca: Genérica | Modelo: ABC" a objeto
   - Detecta valores numéricos automáticamente
   - Mantiene tipos de datos correctos

4. **Generación de Tags**
   - Extrae palabras relevantes del título (3-20 caracteres)
   - Filtra stopwords (de, la, el, para, etc.)
   - Limita a máximo 10 tags por producto

5. **Manejo de Imágenes**
   - Primera imagen: URL externa (marcada como principal)
   - Segunda imagen: Ruta local relativa
   - Texto alternativo automático

6. **SEO Automático**
   - Meta título: Primeros 60 caracteres del nombre
   - Meta descripción: Descripción corta
   - Palabras clave: Primeros 5 tags

## 📋 Ejemplo de Producto Generado

```json
{
  "sku": "3",
  "nombre": "Producto 3",
  "slug": "producto-3",
  "categoria": "Otros",
  "subcategoria": "Varios",
  "descripcion": {
    "corta": "Descripción Inmovilizador Auto Distancia Corta...",
    "completa": "Descripción completa del producto con todos los detalles..."
  },
  "multimedia": {
    "imagenes": [
      {
        "url": "https://http2.mlstatic.com/D_Q_NP_2X_941975...",
        "textoAlternativo": "Producto 3",
        "esPrincipal": true
      },
      {
        "url": "datos/imagenes/3_Producto_3.jpg",
        "textoAlternativo": "Producto 3 - imagen local",
        "esPrincipal": false
      }
    ]
  },
  "estado": true,
  "tags": ["genérica", "inmovilizador", "marca", "modelo"],
  "variantes": [
    {
      "nombre": "Estándar",
      "unidad": "unidades",
      "precio": 19980.0,
      "descuento": 0,
      "sku": "3-001",
      "esPredeterminado": true
    }
  ],
  "atributos": {
    "Marca": "Genérica",
    "Modelo": "Inmovilizador 2.4 GHZ 2M"
  },
  "seo": {
    "metaTitulo": "Producto 3",
    "metaDescripcion": "Descripción Inmovilizador Auto...",
    "palabrasClave": ["genérica", "inmovilizador", "marca"]
  },
  "marca": "Genérica",
  "requiereRefrigeracion": false,
  "ratingAverage": 0
}
```

## 📈 Estadísticas de Conversión

Después de ejecutar el conversor, verás:

```
📈 Estadísticas:
   • Total productos: 10
   • Con descripción: 10/10
   • Con marca: 10/10
   • Con imágenes: 10/10
   • Total de tags: 48
```

## 🔄 Workflow Completo

### 1️⃣ **Scraping**
```bash
python scraper_mercadolibre_v2.py
# Genera: viaje_azul_productos_con_detalles.csv + imágenes
```

### 2️⃣ **Organización**
```bash
# Las carpetas ya están creadas:
# datos/csv/ - datos/imagenes/ - datos/json/
```

### 3️⃣ **Conversión**
```bash
python conversor_a_json.py
# Genera: productos_mercadolibre.json + archivos individuales
```

### 4️⃣ **Uso del JSON**
```javascript
// En tu aplicación Node.js/MongoDB:
const productos = require('./datos/json/productos_mercadolibre.json');

// Insertar en MongoDB
await Product.insertMany(productos);
```

## 🛠️ Personalización

### Cambiar categoría y subcategoría:

Edita [conversor_a_json.py](conversor_a_json.py) línea ~220:

```python
producto = {
    # ...
    "categoria": "TuCategoría",  # Cambiar aquí
    "subcategoria": "TuSubcategoria",  # Cambiar aquí
    # ...
}
```

### Deshabilitar archivos individuales:

```bash
python -c "from conversor_a_json import convertir_csv_a_json; \
convertir_csv_a_json('datos/csv/viaje_azul_productos_con_detalles.csv', \
generar_individuales=False)"
```

### Cambiar unidad de medida en variantes:

Edita línea ~200:

```python
variantes = [{
    "nombre": "Estándar",
    "unidad": "kilogramos",  # Cambiar de "unidades"
    # ...
}]
```

## 📝 Campos Opcionales Soportados

El conversor respeta el esquema del modelo, omitiendo campos `null`:

- ✅ `origen` - Se puede agregar manualmente
- ✅ `vidaUtil` - Para productos perecederos
- ✅ `requiereRefrigeracion` - Detecta en descripción
- ✅ `ratingAverage` - Se puede calcular de reseñas

## 🔍 Validación de Datos

El conversor automáticamente:
- ✅ Limpia texto (trim, normalización)
- ✅ Convierte precios a números
- ✅ Genera slugs únicos
- ✅ Filtra campos vacíos/null
- ✅ Valida formato de atributos

## 💡 Tips

1. **Siempre usa el CSV con detalles** para obtener más información
2. **Revisa el JSON consolidado** antes de importar a BD
3. **Los tags mejoran el SEO** - revisa que sean relevantes
4. **Las rutas de imágenes** son relativas a la carpeta del proyecto

## 📦 Archivos Generados

### JSON Consolidado:
- **Nombre**: `productos_mercadolibre.json`
- **Ubicación**: `datos/json/`
- **Formato**: Array de objetos producto
- **Uso**: Importación masiva a MongoDB

### JSON Individuales:
- **Nombre**: `{sku}_{slug}.json`
- **Ubicación**: `datos/json/`
- **Formato**: Un objeto producto por archivo
- **Uso**: Importación selectiva, testing

## 🎯 Próximos Pasos

1. Importar JSON a MongoDB:
   ```javascript
   const productos = require('./datos/json/productos_mercadolibre.json');
   await Product.insertMany(productos);
   ```

2. Actualizar rutas de imágenes en servidor:
   ```javascript
   // Subir imágenes a tu CDN y actualizar URLs
   producto.multimedia.imagenes[1].url = 'https://cdn.tuapp.com/...';
   ```

3. Enriquecer con datos adicionales:
   - Agregar ratings de clientes
   - Calcular descuentos
   - Asignar categorías específicas

---

**Versión**: 1.0  
**Fecha**: Diciembre 10, 2025  
**Estado**: ✅ Funcional y probado
