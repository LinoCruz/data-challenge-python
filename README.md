# Challenge Data Analytics - Python

### Iniciar un Entorno Conda

Para este proyecto, he usado la distribución Anaconda de Python. Así que sigue estos pasos para crear un entorno:

1. Para crear un entorno, ejecutar:

```
conda create -n yourenv pip
```

- Reemplace "yourenv" con el nombre del nuevo entorno. El comando pip debería permitirle trabajar con pip para instalar los paquetes necesarios con pip.

2. Para activar un Entorno Conda:

```
conda activate myenv
```

- Esto debería activar el entorno y cargar algunos paquetes.

3. Para descargar todos los paquetes, ejecute:

```
pip install -r requirements.txt
```

#### Tener en cuenta:

Las urls de las bases de datos se pueden cambiar en el `app/links.py` si es necesario.

- Para conectarse con PostgreSQL, debe agregar sus datos de PostgreSQL en `.env`

4. Una vez que tenga todos los paquetes instalados, podemos ejecutar la applicación así:

```
python app/main.py
```
