import React, { useState } from 'react';
import '../assets/css/preprocessing.css';

const Preprocessing = () => {
    const [resultado, setResultado] = useState('');
    const [imagen, setImagen] = useState(null);
    const [loading, setLoading] = useState(false);
    const [responseDataList, setResponseDataList] = useState([]); // Nuevo estado para almacenar los datos del servidor

    const handleFileChange = (event) => {
        setImagen(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault(); // Evita la recarga de la página al enviar el formulario
        setLoading(true); // Activa el estado de carga

        try {
            const formData = new FormData();
            formData.append('imagen', imagen);

            const response = await fetch('http://127.0.0.1:5000/preprocesamiento', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            console.log(data);
            // Aquí asumimos que la respuesta del servidor es una lista de objetos
            // donde cada objeto tiene propiedades como landmarks, dist_ojo_der, etc.
            // Puedes iterar sobre esta lista para mostrar los datos en el frontend.
            setResponseDataList(data); // Suponiendo que `data` es la lista recibida del servidor
        } catch (error) {
            console.error('Error al procesar la imagen:', error);
            setResultado('Error al procesar la imagen. Consulta la consola para más detalles.');
        }

        setLoading(false); // Desactivar el estado de carga al finalizar el procesamiento
    };

    return (
        <section id="preprocessing">
            <h1>Preprocesamiento de Imagen</h1>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
                dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
                ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
                fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
                deserunt mollit anim id est laborum.</p>
            <form onSubmit={handleSubmit}>
                <input type="file" name="imagen" onChange={handleFileChange} />
                <button type="submit" disabled={!imagen || loading}>
                    {loading ? 'Procesando...' : 'Aceptar'}
                </button>
            </form>
            <div>
                <h2>Resultado:</h2>
                <p>{resultado}</p>
            </div>
            <div>
                <p>Rostros Detectados:</p>
                <table>
                    <thead>
                        <tr>
                            <th>Landmarks</th>
                            <th>Distancia Ojo Derecho</th>
                            <th>Distancia Ojo Izquierdo</th>
                            <th>Imagen</th>
                        </tr>
                    </thead>
                    <tbody>
                        {responseDataList.map((data, index) => (
                            <tr key={index}>
                                <td>{data.dist_ojo_der}</td>
                                <td>{data.dist_ojo_izq}</td>
                                <td>
                                    {data.imagen_url && (
                                        <img src={`data:image/jpeg;base64,${data.landmarks}`} alt={`Rostro ${index}`} />
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </section>
    );
};
export default Preprocessing;
