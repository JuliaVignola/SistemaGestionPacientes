from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Configuración de conexión MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'insert your password',
    'database': 'pacientes'
}

# Tabla en MySQL


def inicializar():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS signos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            CURP VARCHAR(100),
            nombre VARCHAR(100),
            edad INT,
            frecuencia INT,
            temperatura FLOAT,
            respiracion INT,
            presion VARCHAR(100),
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()


# Inicializar la base al iniciar la aplicación
inicializar()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        datos = (
            request.form['CURP'],
            request.form['nombre'],
            request.form['edad'],
            request.form['frecuencia'],
            request.form['temperatura'],
            request.form['respiracion'],
            request.form['presion']
        )
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO signos (CURP, nombre, edad, frecuencia, temperatura, respiracion, presion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', datos)

        conn.commit()
        cursor.close()
        conn.close()

        return redirect('/pacientes')
    return render_template('index.html')


@app.route('/pacientes')
def pacientes():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT nombre, CURP FROM signos')
    lista = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('pacientes.html', pacientes=lista)


@app.route('/panel/<CURP>')
def panel(CURP):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT fecha, frecuencia, temperatura, respiracion, presion
        FROM signos
        WHERE CURP = %s
        ORDER BY fecha DESC
    ''', (CURP,))
    historial = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('panel.html', CURP=CURP, historial=historial)


@app.route('/buscar')
def buscar():
    CURP = request.args.get('CURP')
    if not CURP:
        return "CURP no proporcionado", 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT nombre, fecha, frecuencia, temperatura, respiracion, presion
        FROM signos
        WHERE CURP = %s
        ORDER BY fecha DESC
    ''', (CURP,))
    registros = cursor.fetchall()
    cursor.close()
    conn.close()

    if not registros:
        return f"No se encontraron registros para el CURP: {CURP}"

    return render_template('busqueda.html', registros=registros, CURP=CURP)


@app.route('/obtener_nombre', methods=['POST'])
def obtener_nombre():
    curp = request.json.get('CURP')

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT nombre FROM signos WHERE CURP = %s LIMIT 1', (curp,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()

    if resultado:
        return {'nombre': resultado[0]}
    else:
        return {'nombre': ''}


if __name__ == '__main__':
    app.run(debug=True)
