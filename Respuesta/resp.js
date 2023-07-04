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
        console.log("dato",dato)
        console.log("doc",doc);

        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/xml");

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: dato.textContent,
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
    }
}