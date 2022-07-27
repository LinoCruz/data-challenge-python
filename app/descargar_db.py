import os 
import requests
from logging_config import log
from links import *
from datetime import date

# Almacenar la fecha de descarga de los archivos
now = date.today()

def descargar_csv(url, categoria):
    '''
    Descarga el csv desde la url pasada por parámetro, guardándolo en la ruta de archivo correspondiente a su categoría y
    fecha de descarga.
    '''
    try:
        # Determinar la carpeta para guardar la descarga
        carpeta = categoria + '/' + str(now.year) + '-' + meses[now.month]
        
        # Si no existe la carpeta, se crea
        if not os.path.exists(carpeta):
                os.makedirs(carpeta)
        
        # Crear la ruta con el nombre de archivo 
        filename = carpeta + '/' + categoria + '-' + str(now.day) + '-' + str(now.month) + '-' + str(now.year) + '.csv'

        # Descargar el archivo y guardarlo en esa ruta
        req = requests.get(url)
        url_content = req.content
        csv_file = open(filename, 'wb')
        csv_file.write(url_content)
        csv_file.close()

        log.info('Se realizó la descarga de los archivos')
        
    except Exception as e:
        log.error('No se pudo completar la descarga de los archivos')
        print(f'Error al realizar la descarga: {e}')

# Aquí ejecutamos las funciones definidas para extraer los datos.
if __name__ == "__main__":
    descargar_csv(BIBLIOTECAS_URL, 'bibliotecas')
    descargar_csv(MUSEOS_URL, 'museos')
    descargar_csv(CINES_URL, 'cines')