from flask import Blueprint, request, jsonify,session
from utils.exceptions import APIError
from services.auth_services import (criar_usuario, 
                                    login_usuario, 
                                    listar_usuarios, 
                                    excluir_usuario)

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])

def login():
    try:
        data = request.get_json()
        login_usuario()
        session['userAdminConnect'] = 1
        return jsonify({'status':'true'}), 200
        #return login_usuario()
    except APIError as e:
        return jsonify({'status': 'error', 'message': str(e)}), e.code
    except Exception as e:
        return jsonify({'status': 'error - 500', 'message': str(e)}), 500


   
