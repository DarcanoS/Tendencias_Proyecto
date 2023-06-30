from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# Definición del modelo del producto Create
class ProductoIn(BaseModel):
    id: int
    nombre: str
    precio: float

# Definición del modelo del producto Updtae
class ProductoInUP(BaseModel):
    nombre: str
    precio: float


class ProductoOut(BaseModel):
    id: int
    nombre: str
    precio: float


uri = "mongodb+srv://usuarioGeneral:ZWxGjUdSO9zffFwP@ud.wbeofk5.mongodb.net/?retryWrites=true&w=majority"

# Crear un nuevo cliente y conectarse al servidor
client = MongoClient(uri, server_api=ServerApi("1"))

# Enviar un ping para confirmar que la conexión se ha realizado correctamente
try:
    client.admin.command("ping")
    print("Ping a su despliegue. Se ha conectado correctamente a MongoDB.")
except Exception as e:
    print(e)

db = client["Tendencias"]
collection = db["Producto"]

app = FastAPI()


@app.get("/productos")
def obtener_productos():
    productos = list(collection.find())
    return {"productos": productos}


@app.get("/productos/{id}")
def obtener_producto(id: int):
    producto = collection.find_one({"_id": id})
    print("ENCONTRADO:",producto)
    if producto:
        return {"producto": producto}
    else:
        raise HTTPException(status_code=404, detail="Producto no encontrado")


@app.post("/productos")
def agregar_producto(producto: ProductoIn):
    nuevo_producto = {"_id":producto.id,"nombre": producto.nombre, "precio": producto.precio}
    result = collection.insert_one(nuevo_producto)
    if result.inserted_id:
        return {"mensaje": "Producto agregado exitosamente"}
    else:
        raise HTTPException(status_code=500, detail="Error al agregar el producto")


@app.put("/productos/{id}")
def actualizar_producto(id: int, producto: ProductoInUP):
    filtro = {"_id": id}
    nuevo_valor = {"$set": {"nombre": producto.nombre, "precio": producto.precio}}
    result = collection.update_one(filtro, nuevo_valor)
    if result.modified_count:
        producto_actualizado = collection.find_one({"_id": id})
        return {"producto": producto_actualizado}
    else:
        raise HTTPException(status_code=404, detail="Producto no encontrado")


@app.delete("/productos/{id}")
def eliminar_producto(id: int):
    filtro = {"_id": id}
    result = collection.delete_one(filtro)
    if result.deleted_count:
        return {"mensaje": "Producto eliminado exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Producto no encontrado")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
