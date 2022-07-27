import descargar_db
import conectar_posgre
import procesamiento_db
from logging_config import log
from links import *

# Descargar Base de Datos
log.info('Descargando archivos fuente')
descargar_db.descargar_csv(BIBLIOTECAS_URL, 'bibliotecas')
descargar_db.descargar_csv(MUSEOS_URL, 'museos')
descargar_db.descargar_csv(CINES_URL, 'cines')

# Procesar datos y crear Tablas Solicitadas
log.info('Procesando datos y creando tablas')
procesamiento_db.procesar_datos()

# Cargar las tablas creadas a PostgreSQL
log.info('Conectando con base de datos y subiendo tablas')
conectar_posgre.cargar_tablas()

# Información de Logs
log.info('Ejecución finalizada con éxito')