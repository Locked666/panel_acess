import os 
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime
from functions import encrypt,decrypt
from models import db, Entidade,Log

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')
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
    e_filter = Entidade.query.filter(Entidade.ativo == False).all()

    if len(e_filter) == 0:
        qt_inativo = 0
    else :
        qt_inativo = 1     

    # print(f"{entidades.qt_inativo}" * 20)    

    return render_template('index.html', entidades=entidades, qt = qt_inativo  )




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


@app.route('/entidades', methods=['GET'])
def get_entidades():
    # Capturar os parâmetros da URL
    id = request.args.get('id')
    ativo = request.args.get('ativo')
    acesso = request.args.get('acesso')
    usuario = request.args.get('usuario')
    nome = request.args.get('nome')

    # Base da consulta
    query = Entidade.query

    # Aplicar filtros dinamicamente
    if id:
        query = query.filter_by(id=id)
    if ativo:
        ativo_bool = ativo.lower() == 'true'  # Converte string para booleano
        query = query.filter_by(ativo=ativo_bool)
    if acesso:
        query = query.filter(Entidade.acesso.ilike(f"%{acesso}%"))
    if usuario:
        query = query.filter(Entidade.usuario.ilike(f"%{usuario}%"))

    if nome:
        query = query.filter(Entidade.nome.ilike(f"%{nome}%"))    

    # Executar a consulta
    entidades = query.all()

    # Converter resultado para JSON
    entidades_json = [
        {
            "id": entidade.id,
            "nome": entidade.nome,
            "ativo": entidade.ativo,
            "acesso": entidade.acesso,
            "usuario": entidade.usuario,
            "data": entidade.data.strftime('%d/%m/%Y %H:%M:%S') if entidade.data else None
        }
        for entidade in entidades
    ]

    # Retornar resultado como JSON
    return jsonify(entidades_json)


@app.route('/CheckStatus', methods=['GET'])
def check_status():
    # Obtém usuário e senha dos parâmetros da requisição
    username = request.args.get('username')
    password = request.args.get('password')

    USERNAME = os.environ.get('APP_USERNAME')
    # PASSWORD = os.environ.get('APP_PASSWORD')
    PASSWORD = 123

    # Verifica se usuário e senha estão corretos
    if username == USERNAME and decrypt(password,os.environ.get('APP_SECRET_KEY'),os.environ.get('APP_SECRET_SALT')) == PASSWORD:
        return jsonify({'status': 'success', 'message': 'Credenciais corretas'})
    else:
        return jsonify({'status': 'error', 'message': 'Usuário ou senha incorretos'}), 401

@app.route('/attEntidades', methods=['POST'])
def update_entidades_api():
    # Capturar os parâmetros da URL
    id = request.args.get('id')  # Usando POST para obter parâmetros
    ativo = request.args.get('ativo')  # True ou False
    acesso = request.args.get('acesso')  # Tipo de acesso
    usuario = request.args.get('usuario')  # Usuário responsável pela alteração
    nome = request.args.get('nome')  # Nome opcional

    # Validação de ID
    if not id:
        return jsonify({'status': 'error', 'message': 'ID da entidade não fornecido'}), 400

    entidade = Entidade.query.get(id)

    if entidade:
        # Atualizar entidade com as informações fornecidas
        entidade.ativo = True if ativo.lower() == 'true' else False  # Converte para booleano
        entidade.acesso = acesso if acesso else entidade.acesso  # Atualiza somente se enviado
        entidade.usuario = usuario if usuario else entidade.usuario
        entidade.data = datetime.now()

        try:
            db.session.commit()

            # Criar registro de log
            log = Log(
                usuario=usuario,
                entidade=entidade.nome,
                acesso=entidade.acesso,
                data=datetime.now(),
                ativo=entidade.ativo
            )
            db.session.add(log)
            db.session.commit()

            # Dados da resposta em JSON para atualizar o front
            data = {
                'status': 'success',
                'message': 'Entidade atualizada com sucesso.',
                'entidade': {
                    'id': entidade.id,
                    'nome': entidade.nome,
                    'ativo': entidade.ativo,
                    'acesso': entidade.acesso,
                    'usuario': entidade.usuario,
                    'data': entidade.data.strftime('%d/%m/%Y %H:%M:%S')
                }
            }

            socketio.emit('update_page', data)  # Emite evento para atualizar o front
            return jsonify(data)

        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': f'Erro ao atualizar entidade: {str(e)}'}), 500

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

    
