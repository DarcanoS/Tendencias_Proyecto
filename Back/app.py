from flask import Flask, request, jsonify
from flask_cors import CORS
from lxml import etree
import xmltodict
import json



app = Flask(__name__)
CORS(app)  # Configura CORS para permitir todas las solicitudes desde cualquier origen


@app.route("/validate-xml", methods=["POST"])
def validate_xml():
    xml_data = request.data.decode('utf-8')  # Obtener el XML enviado en el cuerpo de la solicitud
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

            # Crear la respuesta JSON con la información extraída
            response = {
                "status": "success",
                "message": "El archivo XML es válido.",
                "Entidades":conexion_XML["Entidades"],
                "Conexion":conexion_XML["Conexion"]
            }

            return jsonify(response)

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

if __name__ == "__main__":
    app.run(debug=True)
