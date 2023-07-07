var x = 0;
window.duplicar = function duplicar(id) {
  let contador = 0;

  // Bucle para buscar el segundo hermano siguiente
  let nodoSiguiente = id.nextElementSibling;
  while (nodoSiguiente) {
    contador++;
    if (contador === 2) {
      // Se encontró el segundo hermano siguiente
      break;
    }
    nodoSiguiente = nodoSiguiente.nextElementSibling;
  }
  let clonado = id.nextElementSibling;
  let clon = clonado.cloneNode(true);
  clon.firstElementChild.value = "";

  let titulito = id.previousElementSibling.textContent;
  const tit = document.createElement("h2");
  const cont = document.createTextNode(titulito);
  tit.className = "formulario__titulo";
  tit.appendChild(cont);
  clon.insertBefore(tit, clon.firstElementChild);

  nodoSiguiente.appendChild(clon);
  x = x + 1;

  const newNode = document.createElement("span");
  newNode.className = "ocultar";
  newNode.textContent = "Eliminar";
  newNode.id = x;
  newNode.onclick = function (id) {
    borrar(id);
  };

  nodoSiguiente.insertBefore(newNode, null);
};

window.borrar = function borrar(id) {
  let contenedor = id.target;
  contenedor.previousSibling.remove();
  contenedor.remove();
};

var inputs = document.getElementsByClassName("formulario__input"); //arrive varios datos en una variable
for (var i = 0; i < inputs.length; i++) {
  //length cuantos elementos hay
  inputs[i].addEventListener("keyup", function () {
    //addEventListener=escuchar un evento 'keyup' deje de teclear una tecla
    if (this.value.length >= 1) {
      this.nextElementSibling.classList.add("fijar");
    } else {
      this.nextElementSibling.classList.remove("fijar");
    }
  });
};
var formulario = document.getElementById("datos_form");
//let formulario = document.getElementById("datos_form");


function crearXML() {
  const formData = new FormData(document.getElementById('datos_form'));
  const xmlDoc = document.implementation.createDocument(null, 'App');


  var encabezado1 = xmlDoc.createAttribute('xmlns:xsi');
  encabezado1.value = "http://www.w3.org/2001/XMLSchema-instance";
  var encabezado2 = xmlDoc.createAttribute('xsi:noNamespaceSchemaLocation');
  encabezado2.value = "./MicroSerFor.xsd";

  var titulo = xmlDoc.createProcessingInstruction('xml', 'version="1.0"');
  xmlDoc.insertBefore(titulo, xmlDoc.firstChild);
  const rootElement = xmlDoc.documentElement;

  var a = document.querySelectorAll("h2");
  var elementPadre = xmlDoc.createElement("Entidades");
  var elementHijo = xmlDoc.createElement("atributo");
  formData.forEach((value, key, parent) => {
    console.log("KEY:", key, "VALUE:", value);
    if (key === "nombreEntidad") {
      elementPadre = xmlDoc.createElement("Entidades");
    } else if (key === "url") {
      elementPadre = xmlDoc.createElement("Conexion");
    } else if (key === "nombreAtributo") {
      elementHijo = xmlDoc.createElement("atributo");
    } else if (key === "tipoServicio") {
      elementHijo = xmlDoc.createElement("Servicio");
    }

    if (value) {
      const element = xmlDoc.createElement(key);
      element.textContent = value;

      if (key === "nombreAtributo" || key === "tipoAtributo" || key === "tipoServicio" || key === "nombreServicio") {
        elementHijo.appendChild(element);
        elementPadre.appendChild(elementHijo);
      } else {
        elementPadre.appendChild(element);
        rootElement.appendChild(elementPadre);
      }
    }

    rootElement.setAttributeNode(encabezado1);
    rootElement.setAttributeNode(encabezado2);
  });
  const serializer = new XMLSerializer();
  const xmlString = serializer.serializeToString(xmlDoc);
  console.log(xmlString)
  console.log(xmlDoc);
  return xmlString;
}


formulario.addEventListener("submit", (e) => {
  e.preventDefault();

  const datos = crearXML();

  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/xml");

  var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: datos,
    redirect: 'follow'
  };

  fetch('http://localhost:5000/validate-xml', requestOptions)
    .then(response => {
      if (response.headers.get('content-type') === 'application/json') {
        return response.json();
      } else {
        // Si la respuesta es un archivo, crear un enlace de descarga y descargarlo automáticamente
        return response.blob().then(blob => {
          // Crear un objeto URL para el blob del archivo recibido
          const url = window.URL.createObjectURL(blob);

          // Crear un elemento de enlace de descarga
          const link = document.createElement('a');
          link.href = url;

          // Establecer el nombre del archivo
          link.download = 'archivo.zip';

          // Simular un clic en el enlace para iniciar la descarga
          link.click();

          // Liberar el objeto URL
          window.URL.revokeObjectURL(url);
        });
      }
    })
    .then(data => {
      if (data) {
        console.log("Data Response:", data);
        alerta = "Status: " + data.status + ".\nMensaje: " + data.message.replace('XML', 'FORMULARIO');
        if (data.error) {
          alerta = alerta + "\nERROR: " + data.error.replace('XML', 'FORMULARIO');
        }
        alert(alerta);
      }
    })
    .catch(error => {
      // Manejar cualquier error
      console.error(error);
      alert(error);
    });

});




