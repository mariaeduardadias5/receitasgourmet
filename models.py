import sqlite3
from pathlib import Path

# Caminho do arquivo do banco de dados
DB_PATH = Path(__file__).parent / "receitas.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Retorna dicionários
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()

    # Tabela de usuários
    c.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
    ''')

    # Tabela de receitas
    c.execute('''
    CREATE TABLE IF NOT EXISTS receitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        ingredientes TEXT NOT NULL,
        preparo TEXT NOT NULL,
        tempo TEXT,
        autor_id INTEGER,
        FOREIGN KEY (autor_id) REFERENCES usuarios(id)
    )
    ''')

    conn.commit()
    conn.close()
    print("✅ Banco de dados criado com sucesso!")

if __name__ == "__main__":
    init_db()
