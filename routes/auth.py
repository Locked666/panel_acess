from flask import Blueprint, request, jsonify,session
from utils.exceptions import APIError
from services.auth_services import (criar_usuario, 
                                    consultar_usuario,
                                    login_usuario, 
                                    listar_usuarios, 
                                    excluir_usuario,
                                    update_viagem)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])

def login():
    try:
        data = request.get_json()
        login_usuario()
        u = consultar_usuario(data['username'])
        session['userAdminConnect'] = u['id']
        session['usuarioConnect'] = u['id']
        session['username'] = u['usuario']
        
        
        return jsonify({'status':'true'}), 200
        #return login_usuario()
    except APIError as e:
        return jsonify({'status': 'error', 'message': str(e)}), e.code
    except Exception as e:
        return jsonify({'status': 'error - 500', 'message': str(e)}), 500

@auth_bp.route('/consultaUsuarios', methods=['GET', 'POST'])
def consulta_usuarios():
    try:
        if session.get('userAdminConnect') is None:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        # print(f"\n{session.get('userAdminConnect')}\n")
        user = session.get('userAdminConnect')
        if not user:
            raise APIError('Usuário não autenticado', 401)
        
        usuarios = listar_usuarios()
        return usuarios, 200
    except APIError as e:
        return jsonify({'status': 'error', 'message': str(e)}), e.code
    except Exception as e:
        return jsonify({'status': 'error - 500', 'message': str(e)}), 500
   
@auth_bp.route('/criar', methods=['POST'])
def criar():
    try:
        data = request.get_json()
        if session.get('userAdminConnect') is None:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        # print(f"\n{session.get('userAdminConnect')}\n")
        user = session.get('userAdminConnect')
        if not user:
            raise APIError('Usuário não autenticado', 401)
        
        if not data:
            raise APIError('Dados não informados', 400)
        
        if data.get('id'):
            print(f'\nAtualizando usuario com ID: {data["id"]}\n')
            # Verificar se a viagem existe
            # Atualizar viagem existente
            update_viagem(data)
            return jsonify({'status': 'success', 'message': 'Viagem atualizada com sucesso'}), 200
        else:
            usuario = criar_usuario()
            return jsonify({'message': f'Usuário criado com sucesso!\n Codigo{usuario}'}), 201
    except APIError as e:
        return jsonify({'status': 'error', 'message': str(e)}), e.code
    except Exception as e:
        return jsonify({'status': 'error - 500', 'message': str(e)}), 500