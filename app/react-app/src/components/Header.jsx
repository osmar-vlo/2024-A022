import React from 'react';
import '../assets/css/header.css';

const Header = () => {
    return (
        <header>
            <nav>
                <ul>
                    <li><a href="/" title="Inicio"><i className="material-icons">home</i>Inicio</a></li>
                    <li><a href="/#preprocessing" title="Cargar Imagen"><i className="material-icons">upload</i>Cargar Imagen</a></li>
                </ul>
            </nav>
        </header>
    );
}

export default Header;