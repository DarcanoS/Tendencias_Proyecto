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
        console.log("dato", dato)
        console.log("doc", doc);

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
                    alerta = "Status: " + data.status + ".\nMensaje: " + data.message;
                    if (data.error) {
                        alerta = alerta + "\nERROR: " + data.error;
                    }
                    alert(alerta);
                }
            })
            .catch(error => {
                // Manejar cualquier error
                console.error(error);
                alert(error);
            });
    }
}