# Flask Validate XML App

Esta es una aplicación que lee y procesa un XML. Además de generar el codigo del API en lenguaje Python.

## Instalación


1. Ve al directorio del proyecto:

```
cd Back
```

2. Crea un entorno virtual para la aplicación:

- Para entornos virtuales basados en `venv` (Python 3):

  ```
  python3 -m venv env
  ```

- Para entornos virtuales basados en `virtualenv` (Python 2) (No funciona actualmente con esta versión):

  ```
  virtualenv env
  ```

3. Activa el entorno virtual:

- En sistemas basados en Unix/Linux:

  ```
  source env/bin/activate
  ```

- En Windows:

  ```
  env\Scripts\activate
  ```

4. Instala las dependencias del proyecto:

```
pip install -r requirements.txt
```


## Ejecución

1. Asegúrate de que el entorno virtual esté activado.

2. Ejecuta el siguiente comando para iniciar el servidor Flask:
```
python app.py
```


3. Accede a la aplicación en tu navegador web:

        http://localhost:5000


## Uso

- Para validar el XML y retornar un comprimido con el Codigo Fuente.

        http://localhost:8000/validate-xml

