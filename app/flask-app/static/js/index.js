// Tu código JavaScript para manejar la respuesta del servidor y actualizar la tabla
fetch('http://127.0.0.1:5000/preprocesamiento', {
    method: 'POST',
    body: formData
})
.then(response => {
    if (!response.ok) {
        throw new Error('Error en la solicitud fetch');
    }
    return response.json();
})
.then(data => {
    console.log('Respuesta del servidor:', data); // Verifica la respuesta del servidor en la consola

    // Actualizar la tabla con los datos de las imágenes procesadas
    const tablaImagenes = document.getElementById('tablaImagenes');
    tablaImagenes.innerHTML = ''; // Limpiar la tabla antes de agregar nuevas filas

    data.rostros_recortados.forEach(rostro => {
        console.log('Rostro:', rostro); // Verifica los datos de cada rostro
        const fila = document.createElement('tr');
        fila.innerHTML = `
            <td>${rostro.rostro_id}</td>
            <td><img src="data:image/png;base64, ${rostro.imagen_base64}" alt="Rostro"></td>
            <td>${rostro.dimensiones}</td>
        `;
        tablaImagenes.appendChild(fila);
    });
})
.catch(error => console.error('Error:', error));
