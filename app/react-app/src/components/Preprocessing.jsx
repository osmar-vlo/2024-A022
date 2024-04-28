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
                dolore magna aliqua...</p>
            <form onSubmit={handleSubmit}>
                <input type="file" name="imagen" onChange={handleFileChange} />
                <button type="submit" disabled={!imagen || loading}>
                    {loading ? 'Procesando...' : 'Aceptar'}
                </button>
            </form>
            <div>
            <h2>Resultado:</h2>
            <p>{resultado}</p>
            {responseDataList.map((data, index) => (
                <div key={index}>
                    <img src={`data:image/jpeg;base64,${data.landmarks}`} alt={`Imagen ${index}`} />
                    <p>Distancias Euclideanas:</p>
                    <table>
                        <thead>
                            <tr>
                                <th>Ojo Derecho</th>
                                <th>Ojo Izquierdo</th>
                                <th>Ceja Derecha</th>
                                <th>Ceja Izquierda</th>
                                <th>Nariz</th>
                                <th>Estructura</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>
                                    {data.dist_ojo_der.map((value, idx) => (
                                        <div key={idx}><li>{value}</li></div>
                                    ))}
                                </td>
                                <td>
                                    {data.dist_ojo_izq.map((value, idx) => (
                                        <div key={idx}><li>{value}</li></div>
                                    ))}
                                </td>
                                <td>
                                    {data.dist_ceja_der.map((value, idx) => (
                                        <div key={idx}><li>{value}</li></div>
                                    ))}
                                </td>
                                <td>
                                    {data.dist_ceja_izq.map((value, idx) => (
                                        <div key={idx}><li>{value}</li></div>
                                    ))}
                                </td>
                                <td>
                                    {data.dist_nariz.map((value, idx) => (
                                        <div key={idx}><li>{value}</li></div>
                                    ))}
                                </td>
                                <td>
                                    {data.dist_forma.map((value, idx) => (
                                        <div key={idx}><li>{value}</li></div>
                                    ))}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            ))}
        </div>
        </section>
    );
};
export default Preprocessing;