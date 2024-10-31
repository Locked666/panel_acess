import os 
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime
from models import db, Entidade,Log

app = Flask(__name__)
app.secret_key = 'chave_secreta'
socketio = SocketIO(app)

# Definindo o caminho absoluto para o banco de dados
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'database.db')
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)  # Garante que a pasta 'database/' exista

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evita avisos desnecessários
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        if request.method == 'POST':
            session['username'] = request.form['username']
        else:
            return render_template('welcome.html')

    filtro = request.args.get('filtro', '')
    entidades = Entidade.query.filter(
        Entidade.nome.like(f'%{filtro}%')
    ).order_by(Entidade.ativo.asc()).all()

    # Formate a data de cada entidade antes de passar ao template
    for entidade in entidades:
        if entidade.data:  # Verifique se a data existe para evitar erros
            entidade.data_formatada = entidade.data.strftime('%d/%m/%Y %H:%M:%S')
        else:
            entidade.data_formatada = 'Data não disponível'

    return render_template('index.html', entidades=entidades)




@app.route('/toggle/<int:entidade_id>', methods=['POST'])
def toggle(entidade_id):
    entidade = Entidade.query.get(entidade_id)
    if entidade:
        entidade.ativo = not entidade.ativo  # Alterna o status da entidade
        # Captura as informações adicionais do formulário
        entidade.acesso = request.form.get('tool')
        entidade.usuario = session.get('username', 'Desconhecido')
        entidade.data = datetime.now()
        db.session.commit()

        log = Log(
                usuario=session['username'],
                entidade=entidade.nome,
                acesso = entidade.acesso,
                data=datetime.now(),
                ativo= entidade.ativo if entidade else not entidade.ativo 
        )
        db.session.add(log)
        db.session.commit()
        
        data = {}

        socketio.emit('update_page')  # Emite o evento de atualização
        return jsonify(data)

    return jsonify({'status': 'error', 'message': 'Entidade não encontrada'}), 404




@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        nome = request.form['nome']
        if nome:
            nova_entidade = Entidade(nome=nome)
            db.session.add(nova_entidade)
            db.session.commit()
            socketio.emit('update_page')  # Emite o evento de atualização
            return redirect(url_for('admin'))

    entidades = Entidade.query.all()
    return render_template('admin.html', entidades=entidades)

@app.route('/log', methods=['GET', 'POST'])
def log():
    if request.method == 'POST':
        nome = request.form['nome']
        if nome:
            nova_entidade = Log(nome=nome)
            db.session.add(nova_entidade)
            db.session.commit()
            socketio.emit('update_page')  # Emite o evento de atualização
            return redirect(url_for('admin'))

    filtro = request.args.get('filtro', '')
    logs = Log.query.filter(
        Log.usuario.like(f'%{filtro}%')
    ).order_by(Log.data.desc()).all()

    # Formate a data de cada entidade antes de passar ao template
    for log in logs:
        if log.data:  # Verifique se a data existe para evitar erros
            log.data_formatada = log.data.strftime('%d/%m/%Y %H:%M:%S')
        else:
            log.data_formatada = 'Data não disponível'



    return render_template('log.html', logs=logs)

@socketio.on('connect')
def on_connect():
    print(f"Usuário conectado: {session['username']}.")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000,debug=True)

    
