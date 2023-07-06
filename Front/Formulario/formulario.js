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
  formData.forEach((value, key, parent) => {
    const element = xmlDoc.createElement(key);
    element.textContent = value;



    rootElement.setAttributeNode(encabezado1);
    rootElement.setAttributeNode(encabezado2);
    rootElement.appendChild(element);


  });
  const serializer = new XMLSerializer();
  const xmlString = serializer.serializeToString(xmlDoc);
  console.log(xmlString);
  console.log(xmlDoc);
  return xmlString;
}

/*
function agregarNodosPadre(xmlVariable) {
  // Crear un objeto DOMParser para analizar el XML
  var parser = new DOMParser();

  // Analizar la variable XML en un objeto Document
  var xmlDoc = parser.parseFromString(xmlVariable, "text/xml");

  // Obtener el elemento raíz del XML
  var rootElement = xmlDoc.documentElement;

  // Crear un nuevo nodo padre
  var enti = xmlDoc.createElement("Entidades");
  var noditos = rootElement.childNodes;
  // Mover los nodos hijos existentes al nuevo nodo padre
  //while (rootElement.firstChild) {
    for (var i =0;i<noditos.length;i++){
      if(noditos[i].textContent=="nombreEntidad"){
        console.log(noditos[i].textContent);
      }

    }
      enti.appendChild(rootElement.firstChild);
  //}
  // Agregar el nuevo nodo padre como hijo del elemento raíz
  rootElement.appendChild(enti);

  // Serializar el documento XML modificado de vuelta a una cadena XML
  var xmlModificado = new XMLSerializer().serializeToString(xmlDoc);

  // Devolver el XML modificado
  return xmlModificado;
}*/



// function crearXML() {



//   // Obtener las claves y valores del formulario
//   var clavesValores = [];
//   for (var i = 0; i < formulario.elements.length; i++) {
//     var elemento = formulario.elements[i];
//     if (elemento.type !== "submit") {
//       clavesValores.push({
//         clave: elemento.name,
//         valor: elemento.value
//       });
//     }
//   }
//   // Crear un objeto XMLDocument

//   var xmlDoc = document.implementation.createDocument(null, 'App');

//   // Obtener el formulario y los nodos contenedores
//   var nodosContenedores = document.getElementsByClassName("cl");
//   var nodoContenedor;
//   var nodito = [];
//   for (var i = 0; i < nodosContenedores.length; i++) {
//     nodito[i] = nodosContenedores[i].id;
//     console.log(nodito[i]);
//     nodoContenedor = xmlDoc.createElement(nodito[i]);
//   }
//   //console.log(nodoContenedor);
//   // Recorrer las claves y valores
//   for (var i = 0; i < clavesValores.length; i++) {

//     var clave = clavesValores[i].clave;
//     var valor = clavesValores[i].valor;

//     // Crear un nodo para la clave
//     var nodoClave = xmlDoc.createElement(clave);
//     // Asignar el valor al nodo de la clave
//     nodoClave.appendChild(xmlDoc.createTextNode(valor));

//     if (i == 0) {
//       nodoContenedor.appendChild(nodoClave);
//     } else if (i == 1 || i == 2) {
//       nodoContenedor.appendChild(nodoClave);
//     } else if (i == 3 || i == 4) {
//       nodoContenedor.appendChild(nodoClave);
//     } else if (i == 5 || i == 6) {
//       nodoContenedor.appendChild(nodoClave);
//     } else {
//       nodoContenedor.appendChild(nodoClave);
//     }


//     // Agregar el nodo clave al nodo contenedor

//     //console.log(nodoContenedor);

//   }
//   // Serializar el objeto XMLDocument a una cadena XML
//   var serializer = new XMLSerializer();
//   var xmlString = serializer.serializeToString(xmlDoc);

//   // Aquí puedes guardar o hacer algo con la cadena XML generada
//   console.log(xmlDoc);
//   console.log(xmlString);
// }





formulario.addEventListener("submit", (e) => {
  e.preventDefault();
  //const datos = crearXML(e);

  // Llamar a la función para crear el archivo XML
  const datos = crearXML();
 /* var xmlModificado = agregarNodosPadre(datos);
  console.log(xmlModificado);
*/

  var myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/xml");

  var requestOptions = {
    method: 'POST',
    headers: myHeaders,
    body: datos.textContent,
    redirect: 'follow'
  };

  fetch('http://localhost:5000/validate-xml', requestOptions)
    .then(response => {
      if (response.ok) {
        return response.text();
      }
      throw new Error('Error en la petición POST');
    })
    .then(data => {
      console.log('Respuesta del servidor:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });

});




