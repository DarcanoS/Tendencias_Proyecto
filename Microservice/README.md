# FastAPI CRUD App

Esta es una aplicación de ejemplo que utiliza el framework FastAPI y MongoDB Atlas para implementar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en una base de datos.

## Instalación


1. Ve al directorio del proyecto:

```
cd Microservice
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


5. Configuración de la base de datos:

- Crea una cuenta en MongoDB Atlas si aún no tienes una.
- Crea un clúster y obtén la cadena de conexión.
- En el archivo `main.py`, reemplaza `mongodb+srv://usuarioGeneral:ZWxGjUdSO9zffFwP@ud.wbeofk5.mongodb.net/?retryWrites=true&w=majority` con tu cadena de conexión.
- Verifica que tu Cluster se llama `Tendencias`. Si no cambia `db = client["Tendencias"]`.
- Verifica que tu Colección se llame `Producto`. Si no, cambia `collection = db["Producto"]`

## Ejecución

1. Asegúrate de que el entorno virtual esté activado.

2. Ejecuta el siguiente comando para iniciar el servidor FastAPI:
```
uvicorn main:app --reload
```


3. Accede a la aplicación en tu navegador web:

        http://localhost:8000


## Uso

- Para obtener todos los productos, envía una solicitud GET a la siguiente URL:

        http://localhost:8000/productos

- Para obtener un producto por su ID, envía una solicitud GET a la siguiente URL, reemplazando `{id}` con el ID del producto:

        http://localhost:8000/productos/{id}


- Para agregar un nuevo producto, envía una solicitud POST a la siguiente URL con los datos del producto en el cuerpo de la solicitud como JSON:

        http://localhost:8000/productos


- Para actualizar un producto existente, envía una solicitud PUT a la siguiente URL, reemplazando `{id}` con el ID del producto y proporcionando los nuevos datos del producto en el cuerpo de la solicitud como JSON:

        http://localhost:8000/productos/{id}


- Para eliminar un producto, envía una solicitud DELETE a la siguiente URL, reemplazando `{id}` con el ID del producto:

        http://localhost:8000/productos/{id}

