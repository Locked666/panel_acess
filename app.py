import os 
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest
from functions import encrypt,decrypt
from models import db, Entidade,Log, ConfigAcesso#, RegistroViagens, GastosViagens, DocumentosViagens
from config import Config
from routes.viagens import viagem_bp
from routes.gastos import gasto_bp

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')
socketio = SocketIO(app)
app.config.from_object(Config)
    
    # Registrar blueprints
app.register_blueprint(viagem_bp)
app.register_blueprint(gasto_bp)


# Definindo o caminho absoluto para o banco de dados
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'database.db')
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)  # Garante que a pasta 'database/' exista
USERNAME = os.environ.get('APP_USERNAME')
PASSWORD = os.environ.get('APP_PASSWORD')

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

# @app.route('/cadastro_acesso', methods=['GET', 'POST'])
# def cadastro_acesso():
#     if request.method == 'POST':
#         entidade_id = request.form.get('entidade-id')
#         tipo_conexao = request.form.get('tipo_conexao')
#         id_conexao = request.form.get('id_conexao')
#         port_conexao = request.form.get('port_conexao')
#         usuario = request.form.get('usuario')
#         senha = request.form.get('senha')
#         ativo = request.form.get('ativo')

#         config_acesso = ConfigAcesso(
#             entidade=entidade_id,
#             tipo_conexao=tipo_conexao,
#             id_conexao=id_conexao,
#             port_conexao=port_conexao,
#             usuario=usuario,
#             senha=senha,
#             ativo=ativo
#         )
#         db.session.add(config_acesso)
#         db.session.commit()

#         # return redirect(url_for('home'))
        

#     entidades = Entidade.query.all()
#     acessos = ConfigAcesso.query.all()
#     return render_template('cadastro_acesso.html', acessos=acessos, entidades=entidades)



@app.route('/cadastro_acesso', methods=['GET', 'POST'])
def cadastro_acesso():
    if request.method == 'POST':
        data = request.json
        d_password = encrypt(data['senha'],os.environ.get('APP_SECRET_KEY'), os.environ.get('APP_SECRET_SALT')) if data['senha'] else None
        try:
            # Obter a entidade associada
            entidade = Entidade.query.get(data['entidade-id'])
            if not entidade:
                return jsonify({'status': 'error', 'message': 'Entidade não encontrada'}), 400

            # Criar um novo acesso
            novo_acesso = ConfigAcesso(
                entidade=data['entidade-id'],
                tipo_conexao=data['tipo_conexao'],
                id_conexao=data.get('id_conexao'),
                port_conexao=data.get('port_conexao'),
                usuario=data.get('usuario'),
                # senha=data.get('senha'),
                senha=d_password,
                ativo=data.get('ativo', True)
            )
            db.session.add(novo_acesso)
            db.session.commit()

            return jsonify({
                'status': 'success',
                'id': novo_acesso.id,
                'entidade': entidade.nome
            }), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 500    

    entidades = Entidade.query.all()
    acessos = ConfigAcesso.query.all()
    return render_template('cadastro_acesso.html', acessos=acessos, entidades=entidades)

@app.route('/api/entidades', methods=['GET'])
def autocomplete_entidades():
    query = request.args.get('q', '')  # O parâmetro 'q' contém o texto digitado
    entidades = Entidade.query.filter(Entidade.nome.like(f"%{query}%")).all()
    results = [{"id": e.id, "nome": e.nome} for e in entidades]
    return jsonify(results)

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
    username = request.args.get('username')
    password = request.args.get('password')
    d_password = decrypt(password,os.environ.get('APP_SECRET_KEY'), os.environ.get('APP_SECRET_SALT'))
    usuario = request.args.get('usuario')
    nome = request.args.get('nome')

    if username != USERNAME or  d_password != PASSWORD:
        return jsonify({'status': 'error', 'message': 'Usuário ou senha incorretos' }), 401

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
    PASSWORD = os.environ.get('APP_PASSWORD')
    # PASSWORD = '123'
    d_password = decrypt(password,os.environ.get('APP_SECRET_KEY'), os.environ.get('APP_SECRET_SALT'))
    # Verifica se usuário e senha estão corretos
    if username == USERNAME and  d_password== PASSWORD:
        return jsonify({'status': 'success', 'message': 'Credenciais corretas'})
    else:
        return jsonify({'status': 'error', 'message': 'Usuário ou senha incorretos' }), 401

@app.route('/attEntidades', methods=['POST'])
def update_entidades_api():
    # Capturar os parâmetros da URL
    id = request.args.get('id')  # Usando POST para obter parâmetros
    ativo = request.args.get('ativo')  # True ou False
    acesso = request.args.get('acesso')  # Tipo de acesso
    usuario = request.args.get('usuario')  # Usuário responsável pela alteração
    nome = request.args.get('nome')  # Nome opcional
    username = request.args.get('username') # Usuário de Acesso
    password = request.args.get('password') # senha de acesso
    d_password = decrypt(password,os.environ.get('APP_SECRET_KEY'), os.environ.get('APP_SECRET_SALT'))

    if username != USERNAME or  d_password != PASSWORD:
        return jsonify({'status': 'error', 'message': 'Usuário ou senha incorretos' }), 401
        
        
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

@app.route('/viagens', methods=['GET', 'POST'])
def viagens():
    if request.method == 'GET': 
        return render_template('registro_viagens.html')
    # Aqui você pode adicionar lógica para lidar com o envio de dados

@app.route('/adicionar_viagem', methods=['GET', 'POST'])
def adicionar_viagem():
    if request.method == 'GET':
        entidades = Entidade.query.all()
        return render_template('adicionar_viagem.html', entidades=entidades)
    


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

@app.errorhandler(404)
def not_found(e):
    return render_template('page_404.html'), 404

@socketio.on('connect')
def on_connect():
    print(f"Usuário conectado: {session['username']}.")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000,debug=True)

    