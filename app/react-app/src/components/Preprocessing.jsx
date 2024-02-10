import React, { useState } from 'react';
import '../static/css/preprocessing.css';

const Preprocessing = () => {
    const [resultado, setResultado] = useState('');
    const [rostrosRecortados, setRostrosRecortados] = useState([]);
    const [imagen, setImagen] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (event) => {
        setImagen(event.target.files[0]);
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setLoading(true);

        try {
            const formData = new FormData();
            formData.append('imagen', imagen);

            const response = await fetch('http://127.0.0.1:5000/preprocesamiento', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            setResultado(data.resultado);
            setRostrosRecortados(data.rostros_recortados);
        } catch (error) {
            console.error('Error al procesar la imagen:', error);
            setResultado('Error al procesar la imagen. Consulta la consola para más detalles.');
        }

        setLoading(false);
    };

    return (
        <section id="preprocessing">
            <h1>Preprocesamiento de Imágenes</h1>
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
                {rostrosRecortados.map((rostro, index) => (
                    <img key={index} src={`data:image/png;base64,${rostro.imagen_base64}`} alt={`Rostro ${index}`} />
                ))}
            </div>
        </section>
    );
};

export default Preprocessing;