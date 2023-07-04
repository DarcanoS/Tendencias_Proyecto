from flask import Flask, request, jsonify
from lxml import etree
import xmltodict
import json


app = Flask(__name__)


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
            # print(json_data)

            # nombre_entidades = xml_data.xpath("//nombreEntidad/text()")
            # servicios = xml_data.xpath("//Servicio")
            # entidades = []

            # for entidad in xml_data.xpath("//Entidades"):
            #     nombre_entidad = entidad.xpath(".//nombreEntidad/text()")[0]
            #     atributos = []

            #     for atributo in entidad.xpath(".//atributo"):
            #         nombre_atributo = atributo.xpath(".//nombreAtributo/text()")[0]
            #         tipo_atributo = atributo.xpath(".//tipoAtributo/text()")[0]
            #         restricciones = atributo.xpath(".//restricionAtributo/text()")

            #         atributos.append(
            #             {
            #                 "nombreAtributo": nombre_atributo,
            #                 "tipoAtributo": tipo_atributo,
            #                 "restricciones": restricciones,
            #             }
            #         )

            #     entidad_primaria = entidad.xpath(".//atributoPrimario")[0]
            #     nombre_primario = entidad_primaria.xpath(".//nombreAtributo/text()")[0]
            #     tipo_primario = entidad_primaria.xpath(".//tipoAtributo/text()")[0]
            #     restricciones_primario = entidad_primaria.xpath(
            #         ".//restricionAtributo/text()"
            #     )

            #     servicios_entidad = []
            #     for servicio in entidad.xpath(".//Servicio"):
            #         tipo_servicio = servicio.xpath(".//tipoServicio/text()")[0]
            #         nombre_servicio = servicio.xpath(".//nombreServicio/text()")[0]

            #         servicios_entidad.append(
            #             {
            #                 "tipoServicio": tipo_servicio,
            #                 "nombreServicio": nombre_servicio,
            #             }
            #         )

            #     entidades.append(
            #         {
            #             "nombreEntidad": nombre_entidad,
            #             "atributos": atributos,
            #             "atributoPrimario": {
            #                 "nombreAtributo": nombre_primario,
            #                 "tipoAtributo": tipo_primario,
            #                 "restricciones": restricciones_primario,
            #             },
            #             "servicios": servicios_entidad,
            #         }
            #     )

            print(json_data)

            # Crear la respuesta JSON con la información extraída
            response = {
                "status": "success",
                "message": "El archivo XML es válido.",
                "JSON":json_data
                # "nombreEntidades": nombre_entidades,
                # "entidades": entidades,
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

    return json_data

if __name__ == "__main__":
    app.run()
