from flask import Blueprint, request, jsonify
from services.gastos_service import (criar_gasto, 
                                   listar_gastos_por_viagem, 
                                   excluir_gasto)
from utils.exceptions import APIError

gasto_bp = Blueprint('gastos', __name__, url_prefix='/api/gastos')

@gasto_bp.route('/', methods=['POST'])
def criar():
    try:
        data = request.get_json()
        
        print(f'Dados recebidos: {data}')
        gasto = criar_gasto(data)
        return jsonify({
            'status': 'success',
            'gastoId': gasto.id
        }), 201
    except APIError as e:
        return jsonify({'status': 'error', 'message': str(e)}), e.code
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Erro interno'}), 500

@gasto_bp.route('/', methods=['GET'])
def listar():
    try:
        viagem_id = request.args.get('viagemId')
        if not viagem_id:
            raise APIError('ID da viagem não informado', 400)
            
        gastos = listar_gastos_por_viagem(viagem_id)
        return jsonify({
            'status': 'success',
            'gastos': [{
                'id': g.id,
                'tipoGasto': g.tipo_gasto,
                'valor': g.valor,
                'data': g.data.isoformat()
            } for g in gastos]
        })
    except APIError as e:
        return jsonify({'status': 'error', 'message': str(e)}), e.code
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@gasto_bp.route('/total/<int:viagem_id>', methods=['GET'])
def calc_total(viagem_id):
    try:
        gastos = listar_gastos_por_viagem(viagem_id)
        
        if not gastos:
            return jsonify({
                'status': 'success',
                'total': 0,
                'estorno': 0
            })

        total = sum(g.valor for g in gastos )
        total_estorno = sum(g.valor for g in gastos if g.ativo and g.estorno)
        
        return jsonify({
            'status': 'success',
            'total': total,
            'estorno': total_estorno
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Erro ao calcular total: {str(e)}'
        }), 500
        
        
@gasto_bp.route('/<int:gasto_id>', methods=['DELETE'])
def excluir(gasto_id):
    try:
        excluir_gasto(gasto_id)
        return jsonify({'status': 'success'}), 200
    except APIError as e:
        return jsonify({'status': 'error', 'message': str(e)}), e.code
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500