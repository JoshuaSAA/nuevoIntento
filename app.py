from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import errorcode
import os

app = Flask(__name__)

# Configuración de la base de datos usando variables de entorno
config = {
    'user': os.getenv('chilemorron'),
    'password': os.getenv('123'),
    'host': os.getenv('barcodedb-api.azurewebsites.net'),
    'database': os.getenv('barcodedb'),
    'raise_on_warnings': True
}

def connect_to_database():
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Algo está mal con tu usuario o contraseña")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La base de datos no existe")
        else:
            print(err)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consulta', methods=['GET'])
def consulta():
    query = request.args.get('query')
    conn = connect_to_database()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
