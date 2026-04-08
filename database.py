import sqlite3


def create_connection():

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row

    return conn

def execute(query, params=()):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(query, params)

    resultado = cursor.fetchall()

    conn.close()

    return resultado


def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL 
    
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS pergunta (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL,
    texto TEXT NOT NULL,
    enunciado TEXT NOT NULL,
    conclusao TEXT NOT NULL,
                   
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS alternativas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pergunta_id INTEGER NOT NULL,
    texto TEXT NOT NULL,
    correta BOOLEAN NOT NULL,
                 
    FOREIGN KEY (pergunta_id) REFERENCES pergunta(id)
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS resposta(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    alternativas_id INTEGER NOT NULL,
                 
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (alternativas_id) REFERENCES alternativas(id)
                 
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS progresso (
    user_id INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    concluido BOOLEAN NOT NULL,
                 
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
    )''')

    conn.commit()
    conn.close()


def get_respostas_usuario_quiz(user_id, quiz_id):
    query = """
    SELECT a.correta
    FROM resposta r
    JOIN alternativas a ON r.alternativas_id = a.id
    JOIN pergunta p ON a.pergunta_id = p.id
    WHERE r.user_id = ? AND p.quiz_id = ?
    """

    return execute(query, (user_id, quiz_id))
