from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#Definicion del modelo Usuario CREATE
class UsuarioIn(BaseModel):
   id: int
   user: str
   password: str

#Definicion del modelo Usuario UPDATE
class UsuarioInUP(BaseModel):
   user: str
   password: str

#Definicion del modelo Usuario UPDATE
class UsuarioOut(BaseModel):
   id: int
   user: str
   password: str

#Definicion del modelo Rol CREATE
class RolIn(BaseModel):
   id: int
   nombre: str

#Definicion del modelo Rol UPDATE
class RolInUP(BaseModel):
   nombre: str

#Definicion del modelo Rol UPDATE
class RolOut(BaseModel):
   id: int
   nombre: str

#Definicion del modelo Permiso CREATE
class PermisoIn(BaseModel):
   id: int
   descripcion: str
   nombre: str

#Definicion del modelo Permiso UPDATE
class PermisoInUP(BaseModel):
   descripcion: str
   nombre: str

#Definicion del modelo Permiso UPDATE
class PermisoOut(BaseModel):
   id: int
   descripcion: str
   nombre: str

uri ='mongodb+srv://usuarioGeneral:ZWxGjUdSO9zffFwP@ud.wbeofk5.mongodb.net/?retryWrites=true&w=majority'

# Crear un nuevo cliente y conectarse al servidor
client = MongoClient(uri, server_api=ServerApi('1'))

# Enviar un ping para confirmar que la conexión se ha realizado correctamente
try:
   client.admin.command('ping')
   print('Ping a su despliegue. Se ha conectado correctamente a MongoDB.')
except Exception as e:
   print(e)

db = client['Autenticador']
collection_Usuario = db['Usuario']
collection_Rol = db['Rol']
collection_Permiso = db['Permiso']

app = FastAPI()

@app.put('/Usuario/{id}')
def atualizar_Usuario(id:int,Usuario: UsuarioInUP):
   filtro = {'_id': id}
   nuevo_Usuario = {'$set': {'user': Usuario.user,'password': Usuario.password,}}
   result = collection_Usuario.update_one(filtro,nuevo_Usuario)
   if result.modified_count:
       Usuario_atualizado = collection_Usuario.find_one({'_id':id})
       return {'Usuario Actualizado': Usuario_atualizado }
   else:
       raise HTTPException(status_code=500, detail='Error al buscar Usuario')

@app.post('/Usuario')
def agregar_Usuario(Usuario: UsuarioIn):
   nuevo_Usuario = {'_id':Usuario.id, 'user': Usuario.user, 'password': Usuario.password}
   result = collection_Usuario.insert_one(nuevo_Usuario)
   if result.inserted_id:
       return {'mensaje': 'Usuario agregado exitosamente'}
   else:
       raise HTTPException(status_code=500, detail='Error al agregar Usuario')

@app.delete('/Usuario/{id}')
def eliminar_Usuario(id:int):
   filtro = {'_id':id}
   result = collection_Usuario.delete_one(filtro)
   if result.deleted_count:
       return {'mensaje': 'Usuario eliminado correctamente.' }
   else:
       raise HTTPException(status_code=500, detail='Error al buscar Usuario')

@app.get('/Usuario')
def obtener_Usuario_all():
   Usuario = list(collection_Usuario.find())
   return {'Usuario': Usuario}

@app.get('/Usuario/{id}')
def obtener_Usuario(id: int):
   Usuario = collection_Usuario.find_one({'_id':id})
   if Usuario:
       return {'Usuario': Usuario}
   else:
       raise HTTPException(status_code=404, detail='Usuario no encontrado')

@app.put('/Rol/{id}')
def atualizar_Rol(id:int,Rol: RolInUP):
   filtro = {'_id': id}
   nuevo_Rol = {'$set': {'nombre': Rol.nombre,}}
   result = collection_Rol.update_one(filtro,nuevo_Rol)
   if result.modified_count:
       Rol_atualizado = collection_Rol.find_one({'_id':id})
       return {'Rol Actualizado': Rol_atualizado }
   else:
       raise HTTPException(status_code=500, detail='Error al buscar Rol')

@app.post('/Rol')
def agregar_Rol(Rol: RolIn):
   nuevo_Rol = {'_id':Rol.id, 'nombre': Rol.nombre}
   result = collection_Rol.insert_one(nuevo_Rol)
   if result.inserted_id:
       return {'mensaje': 'Rol agregado exitosamente'}
   else:
       raise HTTPException(status_code=500, detail='Error al agregar Rol')

@app.delete('/Rol/{id}')
def eliminar_Rol(id:int):
   filtro = {'_id':id}
   result = collection_Rol.delete_one(filtro)
   if result.deleted_count:
       return {'mensaje': 'Rol eliminado correctamente.' }
   else:
       raise HTTPException(status_code=500, detail='Error al buscar Rol')

@app.get('/Rol')
def obtener_Rol_all():
   Rol = list(collection_Rol.find())
   return {'Rol': Rol}

@app.get('/Rol/{id}')
def obtener_Rol(id: int):
   Rol = list(collection_Rol.find_one({'_id':id}))
   if Rol:
       return {'Rol': Rol}
   else:
       raise HTTPException(status_code=404, detail='Rol no encontrado')

@app.put('/Permiso/{id}')
def atualizar_Permiso(id:int,Permiso: PermisoInUP):
   filtro = {'_id': id}
   nuevo_Permiso = {'$set': {'descripcion': Permiso.descripcion,'nombre': Permiso.nombre,}}
   result = collection_Permiso.update_one(filtro,nuevo_Permiso)
   if result.modified_count:
       Permiso_atualizado = collection_Permiso.find_one({'_id':id})
       return {'Permiso Actualizado': Permiso_atualizado }
   else:
       raise HTTPException(status_code=500, detail='Error al buscar Permiso')

@app.post('/Permiso')
def agregar_Permiso(Permiso: PermisoIn):
   nuevo_Permiso = {'_id':Permiso.id, 'descripcion': Permiso.descripcion, 'nombre': Permiso.nombre}
   result = collection_Permiso.insert_one(nuevo_Permiso)
   if result.inserted_id:
       return {'mensaje': 'Permiso agregado exitosamente'}
   else:
       raise HTTPException(status_code=500, detail='Error al agregar Permiso')

@app.delete('/Permiso/{id}')
def eliminar_Permiso(id:int):
   filtro = {'_id':id}
   result = collection_Permiso.delete_one(filtro)
   if result.deleted_count:
       return {'mensaje': 'Permiso eliminado correctamente.' }
   else:
       raise HTTPException(status_code=500, detail='Error al buscar Permiso')

@app.get('/Permiso')
def obtener_Permiso_all():
   Permiso = list(collection_Permiso.find())
   return {'Permiso': Permiso}

@app.get('/Permiso/{id}')
def obtener_Permiso(id: int):
   Permiso = list(collection_Permiso.find_one({'_id':id}))
   if Permiso:
       return {'Permiso': Permiso}
   else:
       raise HTTPException(status_code=404, detail='Permiso no encontrado')

if __name__ == '__main__':
   uvicorn.run(app, host='0.0.0.0', port=8000)
