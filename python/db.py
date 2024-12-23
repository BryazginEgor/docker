import psycopg2
import os


DATABASE_URL = "postgresql://postgres:postgres@postgres:5432/postgres"

def get_db_connection():
    """Создает подключение к базе данных PostgreSQL."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def init_db():
    """Инициализирует базу данных (создает таблицы)."""
    conn = get_db_connection()
    cur = conn.cursor()
    with open("schema.sql", "r") as f:
        cur.execute(f.read())
    conn.commit()
    cur.close()
    conn.close()


def store_data(user_id, processed_data):
    """Сохраняет обработанные данные в базу данных."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO processed_data (user_id, data) VALUES (%s, %s)",
        (user_id, processed_data)
    )
    conn.commit()
    cur.close()
    conn.close()

def retrieve_data(user_id):
    """Получает данные из базы данных по user_id."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT data FROM processed_data WHERE user_id = %s", (user_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        return result[0]
    else:
        return None
