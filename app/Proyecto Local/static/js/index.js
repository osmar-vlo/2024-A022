const displayElement = (elementId, display = true) => {
    let element = document.getElementById(elementId);
    if(!element)
        return;
    element.style.display = display ? 'block' : 'none';
}

document.getElementById('imagen').addEventListener('change', function(event) {
    var imagenMostrada = document.getElementById('imagenMostrada');
    var archivo = event.target.files[0];

    if (archivo) {
        var lector = new FileReader();

        lector.onload = function(e) {
            imagenMostrada.src = e.target.result;
            imagenMostrada.style.display = 'block';
            displayElement('resultados', true);
        };

        lector.readAsDataURL(archivo);
    } else {
        // Limpiar la vista previa si no se selecciona ninguna imagen
        imagenMostrada.src = '#';
        imagenMostrada.style.display = 'none';
    }
});