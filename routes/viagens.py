from flask import Blueprint, request, jsonify
from services.viagem_service import criar_viagem, listar_cidades, update_viagem,consultar_viagens
from utils.exceptions import APIError

viagem_bp = Blueprint('viagens', __name__, url_prefix='/api/viagens')

@viagem_bp.route('/', methods=['GET'])
def listar():
    return jsonify({
        'status': 'success',
        'viagens': []
    })

@viagem_bp.route('/consulta', methods=['GET'])
def consulta():
    try:
        viagem_id = request.args.get('viagemId')
        if not viagem_id:
            raise APIError('ID da viagem não informado', 400)
        
        # Aqui você pode implementar a lógica para consultar uma viagem específica
        # Exemplo: viagem = consultar_viagem(viagem_id)
        viagem = consultar_viagens(int(viagem_id))
        if not viagem:
            raise APIError('Viagem não encontrada', 404)
        
        return jsonify({
                "tecnico": viagem.usuario_nome,
                "entidade": viagem.entidade_nome,
                "data_inicio": viagem.data_inicio,
                "data_fim": viagem.data_fim,
                "tipo_viagem": viagem.tipo_viagem,
                "n_diarias": viagem.n_diaria,
                "valor_diaria": viagem.v_diaria,
                "descricao": viagem.descricao,
                "n_intranet": viagem.n_intranet,
                "total_gasto": viagem.total_gasto,
        })
    except APIError as e:
        return jsonify({'status': 'error', 'message': str(e)}), e.code
    except Exception as e:
        return jsonify({'status': 'error - 500', 'message': str(e)}), 500    

@viagem_bp.route('/', methods=['POST'])
def criar():
    try:
        data = request.get_json()
        print(f"\nDados recebidos: {data}\n")
        
        if data.get('viagemId'):
            # Atualizar viagem existente
            update_viagem(data)
            return jsonify({'status': 'success', 'message': 'Viagem atualizada com sucesso'}), 200
        else :
            viagem = criar_viagem(data)
        
        
        
        return jsonify({
            'status': 'success',
            'viagemId': viagem.id
        }), 201
    except APIError as e:
        return jsonify({'status': 'error', 'message': str(e)}), e.code
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Erro interno', 'exception': e}), 500

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