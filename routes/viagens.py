from flask import Blueprint, request, jsonify,session
from services.viagem_service import criar_viagem, listar_cidades, update_viagem,consultar_viagens,listar_viagens
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
        
        if int(session.get('usuarioConnect')) != int(viagem.usuario):
            # print(f"\n{session.get('usuarioConnect')} != {viagem.usuario}\n")
            raise APIError('Usuário não autorizado', 403)
        
        
        
        return jsonify({
                "tecnico": viagem.usuario_nome,
                "entidade": viagem.entidade_nome,
                "entidade_id": viagem.entidade_destino,
                "data_inicio": viagem.data_inicio,
                "data_fim": viagem.data_fim,
                "tipo_viagem": viagem.tipo_viagem,
                "n_diarias": int(viagem.n_diaria),
                "valor_diaria": float(viagem.v_diaria),
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
        user = session.get('usuarioConnect')
        if not user:
            raise APIError('Usuário não autenticado', 401)
        # id_viagem =request.args.get('viagemId', '') 
        # print(f"Dados recebidos: {request.args.__dict__}")
        
        if int(user) != int(data['usuario']):   
            raise APIError('Usuário não autorizado', 403)
        
        if data.get('viagemId'):
        # if id_viagem:
            print(f'\nAtualizando viagem com ID: {data["viagemId"]}\n')
            # Verificar se a viagem existe
            # Atualizar viagem existente
            update_viagem(data)
            return jsonify({'status': 'success', 'message': 'Viagem atualizada com sucesso'}), 200
        else :
            print(f'\nCriando nova viagem com dados: {data}\n')
            viagem = criar_viagem(data)
        
        
        
        return jsonify({
            'status': 'success',
            'viagemId': viagem.id
        }), 201
    except APIError as e:
        return jsonify({'status': 'error', 'message': str(e)}), e.code
    except Exception as e:
        return jsonify({'status': 'error', 'message': 'Erro interno', 'exception': e}), 500


@viagem_bp.route('/consultaViagens', methods=['GET', 'POST'])
def consulta_viagens():
    try:
        if session.get('userAdminConnect') is None:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        
        if request.method == 'POST':
            
            data = request.get_json()
            
            if not data:
                raise APIError('Dados não informados', 400)

            viagens = listar_viagens(**data)
                
        if request.method == 'GET':
            viagens = listar_viagens()
            
        if not viagens:
            return jsonify({'status': 'ok', 'message': 'No data found'}), 404
            
        return jsonify(viagens), 200
        # return jsonify([{
        #     'id': c.id,
        #     'entidade': c.entidade_nome,
        #     'entidade_id': c.entidade_destino,
        #     'data_inicio': c.data_inicio,
        #     'data_fim': c.data_fim,
        #     'tipo_viagem': c.tipo_viagem,
        #     'n_diarias': int(c.n_diaria),
        #     'valor_diaria': float(c.v_diaria),
        #     'descricao': c.descricao,
        #     'n_intranet': c.n_intranet,
        #     'total_gasto': c.total_gasto
        # } for c in viagens])
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@viagem_bp.route('/relatorio/viagens', methods=['GET'])
def relatorio_viagens():
    try:
        if session.get('userAdminConnect') is None:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        
        viagens = listar_viagens()
        
        if not viagens:
            return jsonify({'status': 'ok', 'message': 'No data found'}), 404
        
        relatorio = [{
            'id': c.id,
            'tecnico': c.usuario_nome,
            'entidade': c.entidade_nome,
            'entidade_id': c.entidade_destino,
            'data_inicio': c.data_inicio,
            'data_fim': c.data_fim,
            'tipo_viagem': c.tipo_viagem,
            'n_diarias': int(c.n_diaria),
            'valor_diaria': float(c.v_diaria),
            'descricao': c.descricao,
            'n_intranet': c.n_intranet,
            'total_gasto': c.total_gasto
        } for c in viagens]
        
        return jsonify(relatorio), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

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