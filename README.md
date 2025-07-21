# Sistema de de Gestión de Pacientes con Panel Clínico

Este proyecto es un sistema web en Flask que permite:

- Registrar signos vitales de un paciente: nombre, edad, CURP, frecuencia cardíaca, temperatura, respiración, presión.
- Autorrellenado del nombre cuando el CURP ya existe en la base de datos.
- Buscar registros clínicos mediante el CURP.
- Visualizar el panel clínico con todos los registros históricos.
- Generación de gráficas de los signos vitales.
- Listado de todos los pacientes registrados.

## Tecnologías

- Python
- Flask
- MySQL
- HTML, CSS, JavaScript

## Instalación

1. Clona el repositorio o descarga el ZIP.
2. Crear un entorno virtual e instalar dependencias:
   pip install -r requirements.txt
3. Configure la base de datos MySQL
4. Actualice las credenciales en `app.py`.
5. Ejecute la aplicación:
   python app.py

## Uso

- Accede a la URL `http://127.0.0.1:5000` para registrar pacientes.
- Autorrellenado de Nombre por CURP: Cuando se ingresa un CURP en el formulario de registro, el frontend envía una petición AJAX a la ruta `/obtener_nombre`, si el CURP ya existe en la base de datos, se devuelve el nombre registrado previamente para autocompletar el campo nombre.

## Autor

Julia Valeria Vignola Sánchez
