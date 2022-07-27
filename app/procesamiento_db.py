import pandas as pd 
import numpy as np
from logging_config import log
from datetime import date 
from links import *

# Almacenar la fecha de descarga de los archivos
today = date.today()

def procesar_datos():
    '''
    Normaliza toda la información de Museos, Salas de Cine y Bibliotecas Populares, creando una tabla con todos los datos conjuntos.
    Procesa la tabla de datos conjuntos y crea una tabla con la cantidad de registros por categoría, fuente y provincia-categoría.
    Procesa la información de cines y crea una tabla con la cantidad de butacas, pantallas y espacios INCAA por provincia.
    '''
    try:
        # Se carga los datos del csv de bibliotecas
        carpeta = 'bibliotecas' + '/' + str(today.year) + '-' + meses[today.month]
        df_bibliotecas = pd.read_csv(carpeta + '/' + 'bibliotecas' + '-' + str(today.day) + '-' + str(today.month) + '-' + str(today.year) + '.csv', encoding='UTF-8')

        # Seleccionamos las columnas indicadas
        df_bibliotecas = df_bibliotecas[['Cod_Loc', 'IdProvincia', 'IdDepartamento', 'Categoría', 'Provincia', 'Localidad',
                                        'Nombre', 'Domicilio', 'CP', 'Teléfono', 'Mail', 'Web', 'Fuente']]

        # Renombramos las columnas
        df_bibliotecas.rename(
                            columns={'Cod_Loc':'cod_localidad', 'IdProvincia':'id_provincia', 'IdDepartamento':'id_departamento', 'Categoría':'categoría',
                            'Provincia':'provincia', 'Localidad':'localidad', 'Nombre':'nombre', 'Domicilio':'domicilio', 'CP':'código postal',
                            'Teléfono':'número de teléfono', 'Mail':'mail', 'Web':'web', 'Fuente':'fuente'}, inplace=True)

        # 1.- DATOS DE SALA DE CINE
        # Extraemos los datos de Salas de Cine
        carpeta = 'cines' + '/' + str(today.year) + '-' + meses[today.month]
        df_cines = pd.read_csv(carpeta + '/' + 'cines' + '-' + str(today.day) + '-' + str(today.month) + '-' + str(today.year) + '.csv', encoding='UTF-8')

        # Dataframe con información requerida
        df_salas_de_cine = df_cines[['Provincia', 'Pantallas', 'Butacas', 'espacio_INCAA']].copy()
        # Renombramos las columnas de la tabla de Sala de Cines
        df_salas_de_cine.rename(columns={'Provincia':'provincia', 'Pantallas':'pantallas', 'Butacas':'butacas'}, inplace=True)

        # En la columna "espacio_INCAA" mayormente hay valores nulos o con el valor 'sí', y los valores 0 son son INCAA. 
        df_salas_de_cine.replace('0', np.nan, inplace=True)

        # Generar tabla requerida y fecha requerida
        df_salas_de_cine = df_salas_de_cine.groupby('provincia').aggregate({'pantallas': 'sum', 'butacas':'sum', 'espacio_INCAA':'count'}).reset_index()
        df_salas_de_cine = df_salas_de_cine.assign(fecha_carga=today)
        
        df_salas_de_cine.to_csv('df_cines.csv',index=False, encoding='UTF-8') #Guardar

        # Seleccionar columnas de interés
        df_cines = df_cines[['Cod_Loc', 'IdProvincia', 'IdDepartamento', 'Categoría', 'Provincia', 'Localidad',
                                        'Nombre', 'Dirección', 'CP', 'Teléfono', 'Mail', 'Web', 'Fuente']]
        # Renombrar las columnas
        df_cines.rename(
                        columns={'Cod_Loc':'cod_localidad', 'IdProvincia':'id_provincia', 'IdDepartamento':'id_departamento', 'Categoría':'categoría',
                        'Provincia':'provincia', 'Localidad':'localidad', 'Nombre':'nombre', 'Dirección':'domicilio', 'CP':'código postal',
                        'Teléfono':'número de teléfono', 'Mail':'mail', 'Web':'web', 'Fuente':'fuente'}, inplace=True)

    
        # 2. DATA DE MUSEOS
        # Cargar datos de MUSEOS
        carpeta = 'museos' + '/' + str(today.year) + '-' + meses[today.month]
        df_museos = pd.read_csv(carpeta + '/' + 'museos' + '-' + str(today.day) + '-' + str(today.month) + '-' + str(today.year) + '.csv', encoding='UTF-8')

        # seleccionar columnas de interés
        df_museos = df_museos[['Cod_Loc', 'IdProvincia', 'IdDepartamento', 'categoria', 'provincia', 'localidad',
                                'nombre', 'direccion', 'CP', 'telefono', 'Mail', 'Web', 'fuente']]

        # Renombrar las columnas
        df_museos.rename(
                        columns={'Cod_Loc':'cod_localidad', 'IdProvincia':'id_provincia', 'IdDepartamento':'id_departamento', 'dirección':'domicilio',
                        'categoria':'categoría', 'CP':'código postal','telefono':'número de teléfono', 'Mail':'mail', 'Web':'web'}, inplace=True)

        # Nuevo Dataframe con las información 
        df_unido = pd.concat([df_bibliotecas, df_cines, df_museos])

        # Agregar la columna correspondiente a la fecha de carga 
        df_unido = df_unido.assign(fecha_carga=today)

        # Reemplazar los valores sin datos ("s/d") por null
        df_unido = df_unido.replace('s/d', np.nan)

        # Generar la segunda tabla con: cantidad total categoría, fuente y provincia-categoría
        df_categoria = df_unido.value_counts('categoría').reset_index(name='total por categoría')
        df_fuente = df_unido.value_counts('fuente').reset_index(name='total por fuente')
        df_provincia = df_unido.value_counts(['categoría', 'provincia']).reset_index(name='total por provincia y categoría')
        df_provincia.insert(0, 'provincia y categoría', df_provincia['provincia'] + "/" + df_provincia['categoría'])
        df_provincia.drop(['categoría', 'provincia'], axis=1, inplace=True)
        
        # segunda tabla 
        df_registros = pd.concat([df_categoria, df_fuente, df_provincia], axis=1) 
        
        # Agregar fecha de carga
        df_registros = df_registros.assign(fecha_carga=today) 

        # TABLA SOBRE REGISTROS TOTALES
        # Guardar en un nuevo csv 
        df_registros.to_csv('df_cantidad_registros.csv', index=False, encoding='UTF-8')

        # TABLA QUE UNIFICA LAS TRES TABLAS *MUSEO, CINES,BIBLIOTECAS()
        # Quitar columna 'fuente' porque no es necesaria
        df_unido.drop('fuente', axis=1, inplace=True)

        # Nuevo csv con los datos conjuntos
        df_unido.to_csv('df_conjunto.csv', index=False, encoding='UTF-8') 

        log.info('Los datos fueron procesados con éxito')

    except Exception as e:
        log.error('No pudieron procesarse correctamente los datos')
        print(f'Error al procesar los datos: {e}')

if __name__ == '__main__':
    procesar_datos()