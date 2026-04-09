from flask import Flask, redirect, render_template, request, session

import modules as m
import database as db
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')



@app.route('/', methods=['GET', 'POST'])
def login():
    mensagem = None
    if request.method == 'POST':
        
        username = request.form.get('username')
        password = request.form.get('password')

        user = m.get_user(username)
        if user:
            if user["password"] == password:
                session['user_id'] = user['id']
                return redirect("/Quiz", )
            else: 
                mensagem = "senha invalida"
        else:
            m.create_user(username, password)    
            mensagem = "Usuario criado! Faça login novamente"   
            return render_template('login.html', mensagem=mensagem)
        
    return render_template('login.html', mensagem=mensagem)
   
@app.route('/Quiz', methods=['GET', 'POST'])
def Quiz():
    user_id = session.get("user_id")
    quizzes = m.get_quizzes()
    progresso = {}

    for quiz in quizzes:
        acertos, total = m.get_progresso(user_id, quiz["id"])
        progresso[quiz["id"]] = f"{acertos}/{total}"


    return render_template('quiz.html', quizzes=quizzes, progresso=progresso)

@app.route('/quiz_<int:quiz_id>', methods=['GET', 'POST'])
def questoes(quiz_id):

    perguntas = m.get_perguntas(quiz_id)

    if request.method == 'POST':
        user_id = session.get('user_id')

        for pergunta in perguntas:
            resposta = request.form.get(f'pergunta_{pergunta["id"]}')
            if resposta:
                m.save_resposta(user_id, resposta) 

        m.marcar_progresso(user_id, quiz_id) 

        return redirect('/Quiz')

    quizzes = m.get_quizzes()
    perguntas = m.get_perguntas(quiz_id) 
    alternativas = [m.get_alternativas(pergunta['id']) for pergunta in perguntas]
    

    return render_template('questoes.html', quiz_id=quiz_id, quizzes=quizzes, perguntas=perguntas, alternativas=alternativas)

if __name__ == '__main__':
    app.run(debug=True)