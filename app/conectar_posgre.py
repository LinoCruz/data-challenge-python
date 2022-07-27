from decouple import config
import pandas as pd
from logging_config import log 
from sqlalchemy import create_engine, Date, String, Integer

# Conectarse a PostgreSQL usando sqlalchemy
engine = create_engine('postgresql+psycopg2://' + config('DB_USER') + ':' + config('DB_PASSWORD') + '@' + config('DB_HOST') + ':' + config('DB_PORT') + '/'+ config('DB_NAME'))

def cargar_tablas():
    '''
    Conecta con la base de datos y la actualiza con las tablas creadas
    '''
    try:
        # Primero obtenemos la tabla conjunta
        df_conjunto = pd.read_csv('df_conjunto.csv')

        # Pasarla a PostgreSQL
        df_conjunto.to_sql('datos_conjuntos', con=engine, if_exists='replace', index=False, dtype={
            'cod_localidad':String, 'id_provincia':String, 'id_departamento':String, 'categoria':String,
            'provincia':String, 'localidad':String, 'nombre':String, 'domicilio':String, 'código postal':String,
            'número de teléfono':String, 'mail':String, 'web':String, 'fecha_carga':Date})

        # Obtener la tabla de cantidad de registros
        df_registros = pd.read_csv('df_cantidad_registros.csv')

        # Pasarla a PostgreSQL
        df_registros.to_sql('cantidad_registros', con=engine, if_exists='replace', index=False, dtype={
            'categoría':String, 'total por categoría':Integer, 'fuente':String, 'total por fuente':Integer, 
            'provincia':String, 'categorías por provincia':Integer, 'fecha_carga':Date})

        # Obtener la tabla de salas de cine
        df_cines = pd.read_csv('df_cines.csv')

        # Pasarla a PostgreSQL
        df_cines.to_sql('info_cines', con=engine, if_exists='replace', index=False, dtype={
            'provincia':String, 'pantallas':Integer, 'butacas':Integer, 'espacios_INCAA':Integer, 'fecha_carga':Date})
        
        log.info('Se actualizó la base de datos con éxito')

    except Exception as e:
        log.error('No se pudieron subir las tablas')
        print(f'Error al subir las tablas: {e}')

if __name__ == '__main__':
    cargar_tablas()