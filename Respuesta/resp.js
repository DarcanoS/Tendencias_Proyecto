function loadDoc(e) {
    const file = e.target.files[0];
    if (!file) {
        throw new Error('Necesitas un Archivo XML primero')
        alert('Necesitas un Archivo XML primero')
        return false
    }
    const reader = new FileReader();
    reader.readAsText(file);
    reader.onload = function () {
        reader.result;
        var content = document.getElementById('respuesta');
        var dato = document.createTextNode(reader.result);
        content.appendChild(dato);
        var doc = new DOMParser().parseFromString(reader.result, 'application/xml')
       // console.log(doc);



        const xmlData = `<?xml version="1.0" encoding="UTF-8"?>
<root>
  <element>Contenido del elemento</element>
</root>`;

        fetch('http://localhost:5000/validate-xml', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/xml'
            },
            body: dato
        })
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
    }
}