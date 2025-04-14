from flask import Blueprint, request, jsonify
from services.viagem_service import criar_viagem, listar_cidades
from utils.exceptions import APIError

viagem_bp = Blueprint('viagens', __name__, url_prefix='/api/viagens')

@viagem_bp.route('/', methods=['GET'])
def listar():
    return jsonify({
        'status': 'success',
        'viagens': []
    })

@viagem_bp.route('/', methods=['POST'])
def criar():
    try:
        data = request.get_json()
        viagem = criar_viagem(data)
        return jsonify({
            'status': 'success',
            'viagemId': viagem.id
        }), 201
    except APIError as e:
        return jsonify({'status': 'error', 'message': str(e)}), e.code
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Erro interno'}), 500

@viagem_bp.route('/cidades', methods=['GET'])
def cidades():
    try:
        cidades = listar_cidades()
        return jsonify([{
            'id': c.id,
            'nome': c.nome
        } for c in cidades])
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500