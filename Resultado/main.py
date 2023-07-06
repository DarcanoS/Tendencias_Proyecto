from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

#Definicion del modelo Fruta CREATE
class FrutaIn(BaseModel):
   id: int
   nombreFruta: str
   color: str
   textura: str
   sabor: str
   cantSemillas: int
   paisOrigen: str

#Definicion del modelo Fruta UPDATE
class FrutaInUP(BaseModel):
   nombreFruta: str
   color: str
   textura: str
   sabor: str
   cantSemillas: int
   paisOrigen: str

#Definicion del modelo Fruta UPDATE
class FrutaOut(BaseModel):
   id: int
   nombreFruta: str
   color: str
   textura: str
   sabor: str
   cantSemillas: int
   paisOrigen: str

#Definicion del modelo Verdura CREATE
class VerduraIn(BaseModel):
   id: int
   vitamina: str
   mineral: str
   tallos: int

#Definicion del modelo Verdura UPDATE
class VerduraInUP(BaseModel):
   vitamina: str
   mineral: str
   tallos: int

#Definicion del modelo Verdura UPDATE
class VerduraOut(BaseModel):
   id: int
   vitamina: str
   mineral: str
   tallos: int

uri ='mongodb+srv://usuarioGeneral:ZWxGjUdSO9zffFwP@ud.wbeofk5.mongodb.net/?retryWrites=true&w=majority'

# Crear un nuevo cliente y conectarse al servidor
client = MongoClient(uri, server_api=ServerApi('1'))

# Enviar un ping para confirmar que la conexión se ha realizado correctamente
try:
   client.admin.command('ping')
   print('Ping a su despliegue. Se ha conectado correctamente a MongoDB.')
except Exception as e:
   print(e)

db = client['Tendencias']
collection_Fruta = db['Fruta']
collection_Verdura = db['Verdura']

app = FastAPI()

@app.get('/Fruta/{id}')
def obtener_Fruta(id: int):
   Fruta = list(collection_Fruta.find_one({'_id':id}))
   if Fruta:
       return {'Fruta': Fruta}
   else:
       raise HTTPException(status_code=404, detail='Fruta no encontrado')

@app.get('/Fruta')
def obtener_Fruta_all():
   Fruta = list(collection_Fruta.find())
   return {'Fruta': Fruta}

@app.post('/Fruta')
def agregar_Fruta(Fruta: FrutaIn):
   nuevo_Fruta = {'_id':Fruta.id, 'nombreFruta': Fruta.nombreFruta, 'color': Fruta.color, 'textura': Fruta.textura, 'sabor': Fruta.sabor, 'cantSemillas': Fruta.cantSemillas, 'paisOrigen': Fruta.paisOrigen}
   result = collection_Fruta.insert_one(nuevo_Fruta)
   if result.inserted_id:
       return {'mensaje': 'Fruta agregado exitosamente'}
   else:
       raise HTTPException(status_code=500, detail='Error al agregar Fruta')

@app.put('/Fruta/{id}')
def atualizar_Fruta(id:int,Fruta: FrutaInUP):
   filtro = {'_id': id}
   nuevo_Fruta = {'$set': {'nombreFruta': Fruta.nombreFruta,'color': Fruta.color,'textura': Fruta.textura,'sabor': Fruta.sabor,'cantSemillas': Fruta.cantSemillas,'paisOrigen': Fruta.paisOrigen,}}
   result = collection_Fruta.update_one(filtro,nuevo_Fruta)
   if result.modified_count:
       Fruta_atualizado = collection_Fruta.find_one({'_id':id})
       return {'Fruta Actualizado': Fruta_atualizado }
   else:
       raise HTTPException(status_code=500, detail='Error al buscar Fruta')

@app.delete('/Fruta/{id}')
def eliminar_Fruta(id:int):
   filtro = {'_id':id}
   result = collection_Fruta.delete_one(filtro)
   if result.deleted_count:
       return {'mensaje': 'Fruta eliminado correctamente.' }
   else:
       raise HTTPException(status_code=500, detail='Error al buscar Fruta')

@app.get('/buscarVerdura/{id}')
def obtener_buscarVerdura(id: int):
   Verdura = list(collection_Verdura.find_one({'_id':id}))
   if Verdura:
       return {'Verdura': Verdura}
   else:
       raise HTTPException(status_code=404, detail='Verdura no encontrado')

@app.get('/buscarVerdura')
def obtener_buscarVerdura_all():
   Verdura = list(collection_Verdura.find())
   return {'Verdura': Verdura}

@app.post('/nuevaVerdura')
def agregar_nuevaVerdura(Verdura: VerduraIn):
   nuevo_Verdura = {'_id':Verdura.id, 'vitamina': Verdura.vitamina, 'mineral': Verdura.mineral, 'tallos': Verdura.tallos}
   result = collection_Verdura.insert_one(nuevo_Verdura)
   if result.inserted_id:
       return {'mensaje': 'Verdura agregado exitosamente'}
   else:
       raise HTTPException(status_code=500, detail='Error al agregar Verdura')

@app.put('/editarVerdura/{id}')
def atualizar_editarVerdura(id:int,Verdura: VerduraInUP):
   filtro = {'_id': id}
   nuevo_Verdura = {'$set': {'vitamina': Verdura.vitamina,'mineral': Verdura.mineral,'tallos': Verdura.tallos,}}
   result = collection_Verdura.update_one(filtro,nuevo_Verdura)
   if result.modified_count:
       Verdura_atualizado = collection_Verdura.find_one({'_id':id})
       return {'Verdura Actualizado': Verdura_atualizado }
   else:
       raise HTTPException(status_code=500, detail='Error al buscar Verdura')

@app.delete('/editarVerdura/{id}')
def eliminar_editarVerdura(id:int):
   filtro = {'_id':id}
   result = collection_Verdura.delete_one(filtro)
   if result.deleted_count:
       return {'mensaje': 'Verdura eliminado correctamente.' }
   else:
       raise HTTPException(status_code=500, detail='Error al buscar Verdura')

if __name__ == '__main__':
   uvicorn.run(app, host='0.0.0.0', port=8000)
