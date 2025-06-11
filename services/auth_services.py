from models import Usuarios, db
from utils.exceptions import APIError
from utils.validators import validar_dados_usuario
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


def consultar_usuario(username):
    try:
        usuario = username
        usuario = Usuarios.query.filter_by(usuario=usuario).first()
        if not usuario:
            return print(f"\n Usuario não encontrado.\n")

        user = {'id': usuario.id,
                'usuario': usuario.usuario,
                'admin': usuario.admin,
                'acesso': usuario.acesso}
        return user
    except Exception as e:
        return print(f"\nerro a consultar usuario: {e}\n")
    

def update_viagem(usuario_id, dados):
    usuario = Usuarios.query.get(usuario_id)
    if not usuario:
        raise APIError('Usuário não encontrado', 404)
    # Atualiza os dados do usuário
    usuario.usuario = dados['usuario']
    usuario.admin = True if  dados['admin'] == 'true' else False,
    usuario.acesso = dados.get('acesso')
    usuario.senha = generate_password_hash(dados['senha'], method='pbkdf2:sha256')
    usuario.ativo = dados['ativo']
    usuario.diaria = True if  dados.get('diaria') == 'true' else False,
    usuario.email = dados.get('email')
    usuario.foto = dados.get('foto')
    usuario.setor = dados.get('setor')
    
    # Salva as alterações no banco de dados
    db.session.commit()
    return usuario

def criar_usuario():
    dados = request.get_json()
    validar_dados_usuario(dados)

    # Verifica se o usuário já existe
    usuario_existente = Usuarios.query.filter_by(usuario=dados['usuario']).first()
    usuario_existente_email = Usuarios.query.filter_by(email=dados['email']).first()
    if usuario_existente:
        raise APIError('Usuário já existe', 400)
    
    if usuario_existente_email:
        raise APIError('Email já cadastrado', 400)

    # Cria um novo usuário
    novo_usuario = Usuarios(
        usuario=dados['usuario'],
        admin= True if  dados['admin'] == True else False,
        acesso=dados.get('acesso'),
        email=dados.get('email'),
        foto=dados.get('foto'),
        setor=dados.get('setor'),
        ativo=True if  dados['ativo'] == True else False,
        diaria=True if  dados.get('diaria') == True else False,
        
        
        
        senha=generate_password_hash(dados['senha'], method='pbkdf2:sha256')
    )
    db.session.add(novo_usuario)
    db.session.commit()

    return novo_usuario.id

def login_usuario():
    dados = request.get_json()
    
    usuario = Usuarios.query.filter_by(usuario=dados['username']).first()
    
    if not usuario or not usuario.admin or not usuario.ativo:
        raise APIError('Usuário ou senha inválidos', 403)

    if not usuario or not check_password_hash(usuario.senha, dados['password']):
        raise APIError('Usuário ou senha inválidos', 401)

    access_token = create_access_token(identity=usuario.usuario)
    return jsonify({'access_token': access_token}), 200

def listar_usuarios():
    usuarios = Usuarios.query.all()
    if not usuarios:
        raise APIError('Nenhum usuário encontrado', 404)

    usuarios_list = []
    for usuario in usuarios:
        usuarios_list.append({
            'id': usuario.id,
            'usuario': usuario.usuario,
            'acesso': usuario.acesso,
            'admin': usuario.admin,
            'diaria': usuario.diaria,
            'email': usuario.email,
            'setor': usuario.setor,
            'foto': usuario.foto,
            'ativo': usuario.ativo,
            'data': usuario.data.strftime('%Y-%m-%d') if usuario.data else None,
        })

    return usuarios_list

def excluir_usuario(usuario_id):
    usuario = Usuarios.query.get(usuario_id)
    if not usuario:
        raise APIError('Usuário não encontrado', 404)

    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'message': 'Usuário excluído com sucesso!'}), 200


if __name__=='__main__':
    pas = generate_password_hash('123456789', method='sha256')
    print(pas)
    #app.run(debug=True)