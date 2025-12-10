# Configuración del Servidor API - EJEMPLO
# Copia este archivo a 'config_servidor.py' y edita con tus valores reales

# URL del servidor
API_URL = "http://localhost:4000/api/products"

# Token de autenticación (JWT)
# Obtén tu token del servidor y reemplaza este valor
AUTH_TOKEN = "tu_token_jwt_aqui"

# Configuración de reintentos
MAX_REINTENTOS = 3

# Delay entre productos (segundos) para no saturar el servidor
DELAY_ENTRE_PRODUCTOS = 0.5

# Timeout para peticiones (segundos)
TIMEOUT = 30
