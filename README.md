## Table of Contents

- [Project Structure](##Structure)
- [React](##React)
- [Webpack](##Webpack)
- [Flask](##Flask)

## Structure
- app/
  - Proyecto Local/          
  - react-app/ # Frontend
  - API Flask/ # Backend
  
## React

### Iniciar el servidor de desarrollo local (http://localhost:3000/)

Para iniciar el servidor de desarrollo local, asegúrate de estar dentro de la carpeta react-app/ y ejecuta el siguiente comando en tu terminal:
  ```bash
   npm run start 
  ```
Este comando iniciará el servidor de desarrollo local, permitiéndote acceder a tu aplicación React en tu navegador web en la dirección http://localhost:3000/.

## Webpack
###  Compilar y construir la aplicación.

Para compilar y construir tu aplicación para producción, asegúrate de estar dentro de la carpeta react-app/ y ejecuta el siguiente comando en tu terminal:
  ```bash
   npm run build 
  ```
Este comando se encarga de utilizar Webpack para compilar y construir la aplicación, preparándola para ser desplegada en un entorno de producción. Durante este proceso, Webpack aplica optimizaciones para reducir el tamaño del código y mejorar el rendimiento de la aplicación.

###  Iniciar el servidor de desarrollo local.

Para iniciar el servidor de desarrollo local y comenzar a trabajar en tu proyecto, asegúrate de estar dentro de la carpeta react-app/ y ejecuta el siguiente comando en tu terminal:
  ```bash
   npm run dev  
  ```
Este comando utiliza Webpack en modo de desarrollo para compilar la aplicación y servirla localmente. Te permite desarrollar y probar tu aplicación en tiempo real mientras haces cambios en el código. Además, proporciona mensajes de error y advertencia detallados que te ayudan a depurar y mejorar tu aplicación durante el proceso de desarrollo.
