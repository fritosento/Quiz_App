from database import create_connection, create_table

import database as db


def get_quizzes():
    conn = create_connection()
    quizzes = conn.execute('SELECT * FROM quizzes').fetchall()
    conn.close()
    return quizzes


def get_perguntas(quiz_id):
    conn = create_connection()
    perguntas = conn.execute('SELECT * FROM pergunta WHERE quiz_id = ?', (quiz_id,)).fetchall()
    conn.close()
    return perguntas


def get_alternativas(pergunta_id):
    conn = create_connection()
    alternativas = conn.execute('SELECT * FROM alternativas WHERE pergunta_id = ?', (pergunta_id,)).fetchall()
    conn.close()
    return alternativas


def get_progresso(user_id):
    conn = create_connection()
    dados = conn.execute('SELECT * FROM progresso WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return dados

def get_user(login_user):
    conn = create_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (login_user,)).fetchone()
    conn.close()
    return user

def delete_respostas_quiz(user_id, quiz_id):
    query = """
    SELECT a.id
    FROM alternativas a
    JOIN pergunta p ON a.pergunta_id = p.id
    WHERE p.quiz_id = ?
    """
    
    alternativas = db.execute(query, (quiz_id,))

    for alt in alternativas:
        db.execute(
            "DELETE FROM resposta WHERE user_id = ? AND alternativas_id = ?",
            (user_id, alt["id"])
        )

def save_resposta(user_id, alternativas_id):
    conn = create_connection()
    conn.execute('INSERT INTO resposta (user_id, alternativas_id) VALUES (?, ?)', (user_id, alternativas_id))
    conn.commit()
    conn.close()

def marcar_progresso(user_id, quiz_id):
    conn = create_connection()
    conn.execute('INSERT INTO progresso (user_id, quiz_id, concluido) VALUES (?, ?, ?)', (user_id, quiz_id, True))
    conn.commit()
    conn.close()

def create_user(login_user, login_pass):
    conn = create_connection()
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (login_user, login_pass))
    conn.commit()
    conn.close()

def get_progresso(user_id, quiz_id):
    respostas = db.get_respostas_usuario_quiz(user_id, quiz_id)

    acertos = 0
    total = len(respostas)

    for r in respostas:
        if r["correta"]:
            acertos += 1

    return acertos, total