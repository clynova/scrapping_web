# 🔒 Guía de Seguridad - Protección del Token JWT

## ⚠️ **IMPORTANTE: NO COMPARTAS TU TOKEN EN GITHUB**

Este documento explica cómo mantener tu token de autenticación seguro y fuera de GitHub.

---

## 📋 Estructura Actual

### Archivos que SÍ pueden subirse a GitHub:
- ✅ `config_servidor.example.py` - Plantilla sin token real
- ✅ `importar_a_servidor.py` - Script que importa config desde el archivo
- ✅ `test_conexion_servidor.py` - Script de prueba
- ✅ Todos los demás archivos de código

### Archivos que NO deben subirse a GitHub:
- ❌ `config_servidor.py` - Contiene tu token real
- ❌ `.env` - Variables de entorno
- ❌ Cualquier archivo con credenciales

---

## 🔐 Cómo Funciona

### 1. Archivo de Configuración Ejemplo
**`config_servidor.example.py`** (público, sin token real)
```python
API_URL = "http://localhost:4000/api/products"
AUTH_TOKEN = "tu_token_jwt_aqui"
# ... resto de configuración
```

### 2. Archivo de Configuración Real
**`config_servidor.py`** (privado, NO en GitHub)
```python
API_URL = "http://localhost:4000/api/products"
AUTH_TOKEN = "eyJhbGc..."  # Tu token real
# ... resto de configuración
```

### 3. Scripts que Importan
Los scripts importan desde `config_servidor.py`:
```python
from config_servidor import API_URL, AUTH_TOKEN
```

---

## ✅ Configuración en tu Máquina

### Paso 1: Crear archivo local de configuración
```bash
cp config_servidor.example.py config_servidor.py
```

### Paso 2: Editar con tu token real
```bash
nano config_servidor.py
# o
code config_servidor.py
```

Reemplaza:
```python
AUTH_TOKEN = "tu_token_jwt_aqui"
```

Con tu token real:
```python
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6I..."
```

### Paso 3: Verificar .gitignore
```bash
cat .gitignore | grep config_servidor
# Debería mostrar: config_servidor.py  # Contiene token de autenticación
```

---

## 🛡️ Protecciones Implementadas

### 1. .gitignore Configurado
El archivo `.gitignore` excluye:
```ignore
config_servidor.py  # Contiene token de autenticación
```

### 2. Script de Validación
`importar_a_servidor.py` y `test_conexion_servidor.py` validan que:
- ✅ `config_servidor.py` existe
- ✅ Contiene configuración válida
- ✅ Si no existe, muestran error claro

### 3. Archivo de Ejemplo Público
`config_servidor.example.py` es la plantilla para nuevos usuarios:
- ✅ Sin credenciales reales
- ✅ Instrucciones claras
- ✅ Puede subirse a GitHub

---

## 📝 Instrucciones para Otros Desarrolladores

Si otro desarrollador clona tu repositorio:

### 1. Ver archivos de ejemplo
```bash
ls -la | grep config_servidor
# Verá: config_servidor.example.py
```

### 2. Crear archivo local
```bash
cp config_servidor.example.py config_servidor.py
```

### 3. Editar con su token
```bash
nano config_servidor.py
# Pegar su token JWT en AUTH_TOKEN
```

### 4. Verificar que funciona
```bash
python test_conexion_servidor.py
```

---

## 🚀 Flujo Seguro de Trabajo

### Desarrollo Local
```bash
# Tu máquina (desarrollo)
├── config_servidor.py          # Tu token real (LOCAL ONLY)
├── config_servidor.example.py  # Plantilla (en GitHub)
└── importar_a_servidor.py      # Script (en GitHub)
```

### GitHub (Repositorio Público)
```bash
# GitHub (repositorio remoto)
├── config_servidor.example.py  # Plantilla ✅
├── importar_a_servidor.py      # Script ✅
└── .gitignore                  # Excluye config_servidor.py ✅
# ❌ NO contiene config_servidor.py
# ❌ NO contiene tokens reales
```

---

## ⚠️ Qué Evitar

### ❌ NO hagas esto:
```python
# ❌ Token hardcodeado en script
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiI..."  # ¡Nunca!

# ❌ Token en rama default
git add config_servidor.py
git push origin main

# ❌ Token en archivos públicos
# config_servidor.py versión pública con token real
```

### ✅ HAZ esto:
```python
# ✅ Leer desde archivo de configuración
from config_servidor import AUTH_TOKEN

# ✅ Archivo de ejemplo sin token
# config_servidor.example.py con placeholder

# ✅ Excluir con .gitignore
echo "config_servidor.py" >> .gitignore
```

---

## 🔍 Verificación de Seguridad

### 1. Verificar que config_servidor.py está excluido
```bash
git status | grep config_servidor
# No debe aparecer nada si está bien

# o
git check-ignore -v config_servidor.py
# Debe mostrar: .gitignore:XX: config_servidor.py
```

### 2. Verificar que no hay tokens en historial
```bash
git log -p --all | grep "eyJhbGc"
# Si aparece algo, ¡tu token está en el historial!
# Ver sección de "Recuperación de Incidente"
```

### 3. Verificar archivos a subir
```bash
git diff --cached | grep AUTH_TOKEN
# No debe aparecer tu token real
```

---

## 🚨 Recuperación de Incidente

Si accidentalmente subiste tu token a GitHub:

### ⚠️ ACCIÓN INMEDIATA:
1. **Revoca el token en el servidor**
   - Contacta al administrador
   - Pide generar un nuevo token
   - Reemplaza en `config_servidor.py`

2. **Limpia el historial de Git**
   ```bash
   # Eliminar el commit del historial (SI AÚN NO HAS HECHO PUSH)
   git reset --soft HEAD~1
   git restore config_servidor.py
   
   # Si YA HICISTE PUSH, necesitas:
   # - Revocar el token en el servidor (crítico)
   # - Usar git-filter-branch para limpiar el historial
   ```

3. **Genera nuevo token**
   - Solicita al servidor uno nuevo
   - Actualiza `config_servidor.py`

---

## 📚 Referencias

### Variables de Entorno Alternativa (Avanzado)
En lugar de archivo de configuración, podrías usar variables de entorno:

```python
import os

API_URL = os.getenv('API_URL', 'http://localhost:4000/api/products')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

if not AUTH_TOKEN:
    raise ValueError("Error: AUTH_TOKEN no definido en variables de entorno")
```

Luego ejecutar:
```bash
export AUTH_TOKEN="tu_token_real"
python importar_a_servidor.py
```

---

## ✅ Checklist de Seguridad

- [ ] `config_servidor.py` está en `.gitignore`
- [ ] `config_servidor.example.py` está en GitHub (sin token)
- [ ] Tu `config_servidor.py` local tiene tu token real
- [ ] Nunca hiciste `git add config_servidor.py`
- [ ] Verificaste `git status` antes de hacer push
- [ ] Tu token real NO aparece en GitHub
- [ ] Otros desarrolladores pueden clonar y usar `config_servidor.example.py`
- [ ] Documentación clara para nuevos desarrolladores

---

## 🎓 Conclusión

**El sistema es seguro cuando:**
1. ✅ `config_servidor.py` está excluido de git
2. ✅ Cada desarrollador tiene su propia copia local
3. ✅ Tokens nunca se guardan en repositorio
4. ✅ Ejemplo público disponible para referencia

**Mantén tu repositorio seguro: tokens fuera de GitHub** 🔒
