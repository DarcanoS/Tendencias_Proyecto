from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from lxml import etree
import xmltodict
import json
import os
import zipfile


app = Flask(__name__)
CORS(app)  # Configura CORS para permitir todas las solicitudes desde cualquier origen


@app.route("/validate-xml", methods=["POST"])
def validate_xml():
    xml_data = request.data.decode(
        "utf-8"
    )  # Obtener el XML enviado en el cuerpo de la solicitud
    xsd_path = "../XML/MicroSerFor.xsd"  # Ruta al archivo XSD que se utilizará para validar el XML
    # Parsear el XML y el XSD
    xml_tree = etree.fromstring(xml_data)
    xsd_tree = etree.parse(xsd_path)

    # Crear el validador XMLSchema
    schema = etree.XMLSchema(xsd_tree)

    # Validar el XML
    is_valid = schema.validate(xml_tree)

    print("Es valido:", is_valid)

    if is_valid:
        try:
            # El XML es válido
            # Extraer la información relevante del XML y formatearla en JSON
            json_data = xml_to_json(xml_data)

            conexion_XML = json_data["App"]

            construirMicro(conexion_XML)

            # Obtener la ruta de la carpeta a comprimir desde la solicitud POST
            carpeta = '../Resultado'

            # Verificar si la carpeta existe
            if not os.path.exists(carpeta):
                return "La carpeta no existe", 400

            print("Carpete Encontrada")
            # Crear el archivo comprimido
            nombre_zip = "carpeta_comprimida.zip"
            with zipfile.ZipFile(nombre_zip, "w") as zipf:
                for root, _, files in os.walk(carpeta):
                    for file in files:
                        archivo = os.path.join(root, file)
                        zipf.write(archivo, os.path.relpath(archivo, carpeta))

            # Enviar el archivo comprimido como respuesta
            return send_file(nombre_zip, as_attachment=True)

            # Crear la respuesta JSON con la información extraída
            # response = {
            #     "status": "success",
            #     "message": "El archivo XML es válido.",
            #     "Entidades": conexion_XML["Entidades"],
            #     "Conexion": conexion_XML["Conexion"],
            # }

            # return jsonify(response)

        except Exception as e:
            return {
                "status": "error",
                "message": "Ocurrió un error durante la validación del XML.",
                "error": str(e),
            }, 400

    else:
        # El XML no es válido
        response = {"status": "error", "message": "El archivo XML no es válido."}
        return jsonify(response), 400


@app.route("/", methods=["GET"])
def get_help():
    return {
        "message": "API de Validación de XML",
        "endpoints": {
            "POST /validate-xml": "Validar un archivo XML con un esquema XSD"
        },
    }


def xml_to_json(xml_string):
    # Convertir XML a diccionario
    xml_dict = xmltodict.parse(xml_string)

    # Convertir diccionario a JSON
    json_data = json.dumps(xml_dict, indent=4)

    return json.loads(json_data)


def construirMicro(jsonData):
    # Obtener los datos necesarios
    conexion = jsonData["Conexion"]
    entidades = jsonData["Entidades"]
    if "atributo" in entidades:
        entidades = [entidades]

    llave_aux_izq = "{"
    llave_aux_der = "}"

    # Crear un nuevo archivo .py
    with open("../Resultado/main.py", "w") as file:
        # Escribir la información de la conexión
        file.write(f"from pymongo.mongo_client import MongoClient\n")
        file.write(f"from pymongo.server_api import ServerApi\n")
        file.write(f"from fastapi import FastAPI, HTTPException\n")
        file.write(f"from pydantic import BaseModel\n")
        file.write(f"\n")

        # Escribir la información de las entidades
        for entidad in entidades:
            nombre_entidad = entidad["nombreEntidad"]

            # Definicion del MODELO CREATE
            file.write(f"#Definicion del modelo {nombre_entidad} CREATE\n")
            file.write(f"class {nombre_entidad}In(BaseModel):\n")
            file.write(f"   id: int\n")

            atributos = entidad["atributo"]
            if "nombreAtributo" in atributos:
                atributos = [atributos]
            if isinstance(atributos, list):
                for atributo in atributos:
                    nombre_atributo = atributo["nombreAtributo"]
                    tipo_atributo = atributo["tipoAtributo"]
                    file.write(f"   {nombre_atributo}: {tipo_atributo}\n")

            file.write(f"\n")

            # Definicion del MODELO UPDATE
            file.write(f"#Definicion del modelo {nombre_entidad} UPDATE\n")
            file.write(f"class {nombre_entidad}InUP(BaseModel):\n")

            atributos = entidad["atributo"]
            if "nombreAtributo" in atributos:
                atributos = [atributos]
            if isinstance(atributos, list):
                for atributo in atributos:
                    nombre_atributo = atributo["nombreAtributo"]
                    tipo_atributo = atributo["tipoAtributo"]
                    file.write(f"   {nombre_atributo}: {tipo_atributo}\n")

            file.write(f"\n")

            # Definicion del MODELO SALIDA
            file.write(f"#Definicion del modelo {nombre_entidad} UPDATE\n")
            file.write(f"class {nombre_entidad}Out(BaseModel):\n")
            file.write(f"   id: int\n")

            atributos = entidad["atributo"]
            if "nombreAtributo" in atributos:
                atributos = [atributos]
            if isinstance(atributos, list):
                for atributo in atributos:
                    nombre_atributo = atributo["nombreAtributo"]
                    tipo_atributo = atributo["tipoAtributo"]
                    file.write(f"   {nombre_atributo}: {tipo_atributo}\n")

            file.write(f"\n")

        # url_conexion = conexion["url"]
        # file.write(f"uri ='{url_conexion}'\n")
        file.write(
            f"uri ='mongodb+srv://usuarioGeneral:ZWxGjUdSO9zffFwP@ud.wbeofk5.mongodb.net/?retryWrites=true&w=majority'\n"
        )
        file.write(f"\n")
        file.write(f"# Crear un nuevo cliente y conectarse al servidor\n")
        file.write(f"client = MongoClient(uri, server_api=ServerApi('1'))\n")

        file.write(f"\n")
        file.write(
            f"# Enviar un ping para confirmar que la conexión se ha realizado correctamente\n"
        )
        file.write(f"try:\n")
        file.write(f"   client.admin.command('ping')\n")
        file.write(
            f"   print('Ping a su despliegue. Se ha conectado correctamente a MongoDB.')\n"
        )
        file.write(f"except Exception as e:\n")
        file.write(f"   print(e)\n")

        file.write(f"\n")
        database_conexion = conexion["database"]
        file.write(f"db = client['{database_conexion}']\n")

        for entidad in entidades:
            nombre_entidad = entidad["nombreEntidad"]
            file.write(f"collection_{nombre_entidad} = db['{nombre_entidad}']\n")

        file.write(f"\n")
        file.write(f"app = FastAPI()\n")

        file.write(f"\n")
        for entidad in entidades:
            servicios = entidad["Servicio"]
            if "tipoServicio" in servicios:
                servicios = [servicios]
            nombre_entidad = entidad["nombreEntidad"]
            nombre_servicio = nombre_entidad

            for servicio in servicios:
                if servicio["tipoServicio"] == "readAll":
                    if "nombreServicio" in servicio:
                        nombre_servicio = servicio["nombreServicio"]
                    file.write(f"@app.get('/{nombre_servicio}')\n")
                    file.write(f"def obtener_{nombre_servicio}_all():\n")
                    file.write(
                        f"   {nombre_entidad} = list(collection_{nombre_entidad}.find())\n"
                    )
                    file.write(
                        f"   return {llave_aux_izq}'{nombre_entidad}': {nombre_entidad}{llave_aux_der}\n"
                    )

                if servicio["tipoServicio"] == "readOne":
                    if "nombreServicio" in servicio:
                        nombre_servicio = servicio["nombreServicio"]
                    file.write(
                        f"@app.get('/{nombre_servicio}/{llave_aux_izq}id{llave_aux_der}')\n"
                    )
                    file.write(f"def obtener_{nombre_servicio}(id: int):\n")
                    file.write(
                        f"   {nombre_entidad} = list(collection_{nombre_entidad}.find_one({llave_aux_izq}'_id':id{llave_aux_der}))\n"
                    )
                    file.write(f"   if {nombre_entidad}:\n")
                    file.write(
                        f"       return {llave_aux_izq}'{nombre_entidad}': {nombre_entidad}{llave_aux_der}\n"
                    )
                    file.write(f"   else:\n")
                    file.write(
                        f"       raise HTTPException(status_code=404, detail='{nombre_entidad} no encontrado')\n"
                    )

                if servicio["tipoServicio"] == "create":
                    if "nombreServicio" in servicio:
                        nombre_servicio = servicio["nombreServicio"]
                    file.write(f"@app.post('/{nombre_servicio}')\n")
                    file.write(
                        f"def agregar_{nombre_servicio}({nombre_entidad}: {nombre_entidad}In):\n"
                    )
                    file.write(
                        f"   nuevo_{nombre_entidad} = {llave_aux_izq}'_id':{nombre_entidad}.id"
                    )
                    atributos = entidad["atributo"]
                    if "nombreAtributo" in atributos:
                        atributos = [atributos]
                    for atributo in atributos:
                        nombre_atributo = atributo["nombreAtributo"]
                        file.write(
                            f", '{nombre_atributo}': {nombre_entidad}.{nombre_atributo}"
                        )
                    file.write(f"{llave_aux_der}\n")
                    file.write(
                        f"   result = collection_{nombre_entidad}.insert_one(nuevo_{nombre_entidad})\n"
                    )
                    file.write(f"   if result.inserted_id:\n")
                    file.write(
                        f"       return {llave_aux_izq}'mensaje': '{nombre_entidad} agregado exitosamente'{llave_aux_der}\n"
                    )
                    file.write(f"   else:\n")
                    file.write(
                        f"       raise HTTPException(status_code=500, detail='Error al agregar {nombre_entidad}')\n"
                    )

                if servicio["tipoServicio"] == "update":
                    if "nombreServicio" in servicio:
                        nombre_servicio = servicio["nombreServicio"]
                    file.write(
                        f"@app.put('/{nombre_servicio}/{llave_aux_izq}id{llave_aux_der}')\n"
                    )
                    file.write(
                        f"def atualizar_{nombre_servicio}(id:int,{nombre_entidad}: {nombre_entidad}InUP):\n"
                    )
                    file.write(f"   filtro = {llave_aux_izq}'_id': id{llave_aux_der}\n")
                    file.write(
                        f"   nuevo_{nombre_entidad} = {llave_aux_izq}'$set': {llave_aux_izq}"
                    )
                    atributos = entidad["atributo"]
                    if "nombreAtributo" in atributos:
                        atributos = [atributos]
                    for atributo in atributos:
                        nombre_atributo = atributo["nombreAtributo"]
                        file.write(
                            f"'{nombre_atributo}': {nombre_entidad}.{nombre_atributo},"
                        )
                    file.write(f"{llave_aux_der}{llave_aux_der}\n")
                    file.write(
                        f"   result = collection_{nombre_entidad}.update_one(filtro,nuevo_{nombre_entidad})\n"
                    )
                    file.write(f"   if result.modified_count:\n")
                    file.write(
                        f"       {nombre_entidad}_atualizado = collection_{nombre_entidad}.find_one({llave_aux_izq}'_id':id{llave_aux_der})\n"
                    )
                    file.write(
                        f"       return {llave_aux_izq}'{nombre_entidad} Actualizado': {nombre_entidad}_atualizado {llave_aux_der}\n"
                    )
                    file.write(f"   else:\n")
                    file.write(
                        f"       raise HTTPException(status_code=500, detail='Error al buscar {nombre_entidad}')\n"
                    )

                if servicio["tipoServicio"] == "delete":
                    if "nombreServicio" in servicio:
                        nombre_servicio = servicio["nombreServicio"]
                    file.write(
                        f"@app.delete('/{nombre_servicio}/{llave_aux_izq}id{llave_aux_der}')\n"
                    )
                    file.write(f"def eliminar_{nombre_servicio}(id:int):\n")
                    file.write(f"   filtro = {llave_aux_izq}'_id':id{llave_aux_der}\n")
                    file.write(
                        f"   result = collection_{nombre_entidad}.delete_one(filtro)\n"
                    )
                    file.write(f"   if result.deleted_count:\n")
                    file.write(
                        f"       return {llave_aux_izq}'mensaje': '{nombre_entidad} eliminado correctamente.' {llave_aux_der}\n"
                    )
                    file.write(f"   else:\n")
                    file.write(
                        f"       raise HTTPException(status_code=500, detail='Error al buscar {nombre_entidad}')\n"
                    )

                file.write(f"\n")

        file.write(f"if __name__ == '__main__':\n")
        file.write(f"   uvicorn.run(app, host='0.0.0.0', port=8000)\n")


if __name__ == "__main__":
    app.run(debug=True)
