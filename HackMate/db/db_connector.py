# db/db_connector.py
import mysql.connector

def get_db_connection():
    # Configura tus credenciales y parámetros de conexión
    connection = mysql.connector.connect(
        host="localhost",
        user="tu_usuario",
        password="tu_contraseña",
        database="business_matchmaking"
    )
    return connection

def fetch_users():
    """Recupera los perfiles de usuarios desde la tabla users."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT user_id, business_description, skills_description, looking_for FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

if __name__ == "__main__":
    users = fetch_users()
    print(users)
