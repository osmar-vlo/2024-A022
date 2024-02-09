import React from 'react';
import '../static/css/home.css';

const Home = () => {
    return (
        <section>
            <h1>Futura Face</h1>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et
                dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip
                ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
                fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
                deserunt mollit anim id est laborum.</p>
            <label htmlFor="imagen">Selecciona una imagen:</label>
            <form id="formularioImagen" action="/preprocesamiento" method="post" encType="multipart/form-data">
                <input type="file" name="imagen" id="imagen" accept="image/*" />
                <input type="submit" value="Procesar Imagen" />
            </form>
        </section>
    );
}
export default Home;