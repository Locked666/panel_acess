import os 
from flask import Flask, render_template, request, redirect, url_for, session,jsonify,send_from_directory,abort, make_response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from dotenv import load_dotenv
from reportlab.lib.units import cm
import io
# from flask import render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest
from functions import encrypt,decrypt
from models import db, Entidade,Log, ConfigAcesso,Usuarios, DocumentosViagens, RegistroViagens#, GastosViagens, DocumentosViagens
from config import Config
from routes.viagens import viagem_bp
from routes.gastos import gasto_bp
from routes.auth import auth_bp

load_dotenv(dotenv_path='.env')
app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')
# print('\napp.secret_key',app.secret_key)

socketio = SocketIO(app)
app.config.from_object(Config)
    
    # Registrar blueprints
app.register_blueprint(viagem_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(gasto_bp)


# Definindo o caminho absoluto para o banco de dados
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'database.db')
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)  # Garante que a pasta 'database/' exista
USERNAME = os.environ.get('APP_USERNAME')
PASSWORD = os.environ.get('APP_PASSWORD')

UPLOAD_FOLDER = 'uploads/documentos'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evita avisos desnecessários
db.init_app(app)



def gerar_relatorio_pdf(viagens, usuario_nome='', data_inicial=None, data_final=None):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)

    # HEADER
    pdf.setFont("Helvetica-Bold", 14)
    pdf.rect(1.5*cm, height - 4*cm, width - 3*cm, 3*cm, stroke=1, fill=0)
    pdf.drawString(2*cm, height - 2*cm, "Relatório de Viagens")
    
    pdf.setFont("Helvetica", 10)
    pdf.drawString(2*cm, height - 2.8*cm, f"Usuário: {usuario_nome}")
    pdf.drawString(2*cm, height - 3.4*cm, f"Data Inicial: {data_inicial.strftime('%d/%m/%Y') if data_inicial else '---'}")
    pdf.drawString(10*cm, height - 3.4*cm, f"Data Final: {data_final.strftime('%d/%m/%Y') if data_final else '---'}")
    
    

    # TABELA
    y = height - 5*cm
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(2*cm, y, "Código")
    pdf.drawString(4*cm, y, "Entidade")
    pdf.drawString(10*cm, y, "Saída")
    pdf.drawString(14*cm, y, "Retorno")
    pdf.drawString(18*cm, y, "Relatório")
    pdf.drawString(22*cm, y, "Qtd. Diária")
    pdf.drawString(26*cm, y, "Valor Total")

    y -= 0.7*cm
    pdf.setFont("Helvetica", 9)

    total_diarias = 0
    total_valor = 0.0

    for viagem in viagens:
        if y < 3.5*cm:
            pdf.showPage()
            y = height - 2*cm
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(2*cm, y, "Código")
            pdf.drawString(4*cm, y, "Entidade")
            pdf.drawString(10*cm, y, "Saída")
            pdf.drawString(14*cm, y, "Retorno")
            pdf.drawString(18*cm, y, "Relatório")
            pdf.drawString(22*cm, y, "Qtd. Diária")
            pdf.drawString(26*cm, y, "Valor Total")
            y -= 0.7*cm
            pdf.setFont("Helvetica", 9)

        n_diaria = int(viagem.n_diaria) if viagem.n_diaria and viagem.n_diaria.isdigit() else 0
        v_diaria = viagem.v_diaria or 0.0

        total_diarias += n_diaria
        total_valor += v_diaria

        pdf.drawString(2*cm, y, str(viagem.id))
        pdf.drawString(4*cm, y, viagem.entidade_rel.nome if viagem.entidade_rel else '---')
        pdf.drawString(10*cm, y, viagem.data_inicio.strftime('%d/%m/%Y %H:%M') if viagem.data_inicio else '---')
        pdf.drawString(14*cm, y, viagem.data_fim.strftime('%d/%m/%Y %H:%M') if viagem.data_fim else '---')
        pdf.drawString(18*cm, y, str(viagem.n_intranet) if viagem.n_intranet else '---')
        pdf.drawString(22.5*cm, y, str(n_diaria))
        pdf.drawString(26*cm, y, f"R$ {v_diaria:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

        y -= 0.6*cm

    # TOTALIZADORES
    pdf.setFont("Helvetica-Bold", 10)
    y -= 0.5*cm
    pdf.line(2*cm, y, width - 2*cm, y)
    y -= 0.7*cm
    pdf.drawString(17*cm, y, "Totais:")
    pdf.drawString(22.5*cm, y, str(total_diarias))
    pdf.drawString(26*cm, y, f"R$ {total_valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    # ASSINATURA
    y -= 5*cm
    pdf.line(11.5*cm, y, 17*cm, y)
    pdf.drawString(13.5*cm, y - 0.5*cm, usuario_nome)

    # FOOTER
    pdf.setFont("Helvetica", 8)
    
    # Adicionei o rodapé com a data atual
    data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
    pdf.drawString(24.5*cm, 1*cm, f"Gerado em: {data_atual}")
    pdf.drawString(24.5*cm, 0.5*cm, "Sistema de Controle de Viagens")
    pdf.setFont("Helvetica", 6)

    pdf.save()
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'inline', filename='relatorio_viagens.pdf')
    return response


@app.route('/login', methods=['GET', 'POST'])

def login_admin():
    if session.get('userAdminConnect'):
        return render_template('admin_viagens.html')
    else:
        return render_template('login.html')



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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        # Verifica se o arquivo foi enviado
        if 'arquivo' not in request.files:
            return jsonify({'status': 'error', 'message': 'Nenhum arquivo enviado'}), 400
        
        arquivo = request.files['arquivo']
        viagem_id = request.form.get('viagemId')
        tipo_documento = request.form.get('tipoDocumento')
        
        # Validações
        if arquivo.filename == '':
            return jsonify({'status': 'error', 'message': 'Nome de arquivo vazio'}), 400
            
        if not allowed_file(arquivo.filename):
            return jsonify({'status': 'error', 'message': 'Tipo de arquivo não permitido'}), 400
        
        # Cria diretório se não existir
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Gera nome seguro para o arquivo
        filename = secure_filename(f"{viagem_id}_{tipo_documento}_{arquivo.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Salva o arquivo
        arquivo.save(filepath)
        
        # Grava no banco de dados
        novo_documento = DocumentosViagens(
            arquivo=filepath,
            tipo=tipo_documento,
            data=datetime.now()
        )
        
        db.session.add(novo_documento)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'documentoId': novo_documento.id,
            'caminho': filepath
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': f'Erro no processamento do arquivo: {str(e)}'
        }), 500

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


@app.route('/api/documentos/info/<int:documento_id>', methods=['GET'])
def get_documento_info(documento_id):
    documento = DocumentosViagens.query.get_or_404(documento_id)
    return jsonify({
        'id': documento.id,
        'arquivo': documento.arquivo,
        'tipo': documento.tipo,
    })

@app.route('/api/documentos/<int:documento_id>', methods=['GET'])
def get_documento_file(documento_id):
    documento = DocumentosViagens.query.get_or_404(documento_id)
    directory = os.path.dirname(documento.arquivo)
    filename = os.path.basename(documento.arquivo)
    return send_from_directory(directory, filename)


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

@app.route('/admin_viagens', methods=['POST', 'GET'])
def admin_viagens():
    if session.get('userAdminConnect'):
        return render_template('admin_viagens.html')
    else:
        return render_template('login.html')

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
    data_inicio = None
    data_fim = None
    query_usuarios = Usuarios.query.all()

    # POST: define usuário na sessão
    if request.method == 'POST':
        usuario_id = request.form.get('usuarioConnect')
        if usuario_id:
            session['usuarioConnect'] = usuario_id
            return redirect(url_for('viagens'))
        return render_template('registro_viagens.html')

    # GET: exibe viagens com ou sem filtros
    if 'usuarioConnect' not in session:
        return render_template('setUser.html', users=query_usuarios)


    usuario_id = session['usuarioConnect']
    query = RegistroViagens.query.filter(RegistroViagens.usuario == usuario_id).order_by(RegistroViagens.id.desc())

    # Aplica filtros (via GET)
    data_inicio_str = request.args.get('filtro-data-inicial')
    data_fim_str = request.args.get('filtro-data-final')
    entidade_id = request.args.get('filtro-entidade')
    relatorio = request.args.get('filtro-relatorio')


    if data_inicio_str:
        try:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d')
            query = query.filter(RegistroViagens.data_inicio >= f"{data_inicio}")
            print(f"{data_inicio}")
        except ValueError as e:
            print(f"Erro ao converter data de início: {data_inicio_str}\n{e}")
            pass

    if data_fim_str:
        try:
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d')
            query = query.filter(RegistroViagens.data_fim <= f"{datetime.strftime(data_fim, '%Y-%m-%d 23:59:59')}")
            print(f"{datetime.strftime(data_fim, '%Y-%m-%d 23:59:59')}")
        except ValueError as e:
            print(f"Erro ao converter data de final: {data_fim}\n{e}")
            pass
        
    if entidade_id:
        query = query.filter(RegistroViagens.entidade_destino == entidade_id)

    if relatorio:
        query = query.filter(RegistroViagens.n_intranet.ilike(f'%{relatorio}%'))

    query_viagens = query.limit(20).all()
    query_entidades = Entidade.query.all()
    usuario_logado = Usuarios.query.get(usuario_id)
    
    

    # Formatação das viagens
    for viagem in query_viagens:
        viagem.usuario_nome = viagem.usuario_rel.usuario if viagem.usuario_rel else 'Usuário não encontrado'
        viagem.entidade_nome = viagem.entidade_rel.nome if viagem.entidade_rel else 'Entidade não encontrada'
        viagem.data_formatada = viagem.data_inicio.strftime('%d/%m/%Y %H:%M:%S') if viagem.data_inicio else 'Data Não Disponível'
        viagem.data_final_formatada = viagem.data_fim.strftime('%d/%m/%Y %H:%M:%S') if viagem.data_fim else 'Data Não Disponível'

    if request.args.get('imprimir') == 'true':
        return gerar_relatorio_pdf(query_viagens, usuario_nome=usuario_logado.usuario, data_inicial=data_inicio, data_final=data_fim)

    
    # Renderiza o template com as viagens filtradas
    return render_template(
        'registro_viagens.html',
        viagens=query_viagens,
        usuario=usuario_logado,
        entidades=query_entidades
    )




@app.route('/adicionar_viagem', methods=['GET', 'POST'])
def adicionar_viagem():
    if request.method == 'GET':
        entidades = Entidade.query.all()
        if 'usuarioConnect' not in session:
            return redirect(url_for('viagens'))
        
        if request.args.get('viagemId') != None:
            if request.args.get('viagemId') == '0':
                return render_template('adicionar_viagem.html', entidades=entidades)
            if session['usuarioConnect'] == None:
                return redirect(url_for('viagens'))
            if session['usuarioConnect'] == '':
                return redirect(url_for('viagens'))
            if session['usuarioConnect'] == 0:
                return redirect(url_for('viagens'))
            
            query_viagem = RegistroViagens.query.filter(
                RegistroViagens.id == request.args.get('viagemId'),
                RegistroViagens.usuario == session['usuarioConnect']
            ).first()
            if not query_viagem:
                return redirect(url_for('viagens'))
            
            if query_viagem:
                # Formate a data de cada entidade antes de passar ao template
                if query_viagem.data_inicio:
                    query_viagem.data_formatada = query_viagem.data_inicio.strftime('%d/%m/%Y %H:%M:%S') if query_viagem.data_inicio else 'Data não disponível'
                if query_viagem.data_fim:
                    query_viagem.data_final_formatada = query_viagem.data_fim.strftime('%d/%m/%Y %H:%M:%S') if query_viagem.data_fim else 'Data não disponível'

                # query_viagem = query_viagem.json()
            return render_template('adicionar_viagem.html', viagem=query_viagem, entidades=entidades)
        else : 
            
            return render_template('adicionar_viagem.html', entidades=entidades)
        

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.pop('usuarioConnect', None)
    session.pop('username', None)
    return redirect(url_for('home'))

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

    