from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configura tu conexión a la base de datos
conn = psycopg2.connect(
    dbname="mydatabase",
    user="myuser",
    password="mypassword",
    host="my_postgres_db",  # Nombre del servicio en docker-compose
    port="5432"
)

@app.route('/tables', methods=['GET'])
def get_tables():
    with conn.cursor() as cursor:
        # Ejecuta una consulta para obtener los nombres de las tablas
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        tables = cursor.fetchall()
    # Devuelve una lista de nombres de tablas
    return jsonify([table[0] for table in tables])  

@app.route('/table_data/<table_name>', methods=['GET'])
def get_table_data(table_name):
    with conn.cursor() as cursor:
        # Ejecuta una consulta para obtener todos los datos de la tabla especificada
        cursor.execute(f"SELECT * FROM {table_name};")
        data = cursor.fetchall()
        
        # Obtiene los nombres de las columnas
        columns = [desc[0] for desc in cursor.description]  
        
    # Devuelve una lista de diccionarios, donde cada diccionario representa una fila
    return jsonify([dict(zip(columns, row)) for row in data])  

@app.route('/s')
def home():
    return "Hello, Flask is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Asegúrate de que la aplicación se ejecute en la dirección y puerto correctos
