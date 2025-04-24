from models import RegistroViagens, Entidade, db, Usuarios
from utils.validators import validar_dados_viagem
from utils.exceptions import APIError
from datetime import datetime

def criar_viagem(dados):
    try:
        validar_dados_viagem(dados)
        # Converter datas
    
        
        # Converter strings para objetos datetime
        try:
            # Formato ISO 8601 (2025-04-15T16:46)
            data_inicio = datetime.fromisoformat(dados['dataSaida'])
            data_fim = datetime.fromisoformat(dados['dataRetorno'])
        except ValueError as e:
            raise APIError({'status': 'error', 'message': f'Formato de data inválido: {str(e)}'}, 400)
        
        viagem = RegistroViagens(
            entidade_destino=dados['cidadeDestino'],
            data_inicio=data_inicio,
            tipo_viagem = dados['tipoViagem'],
            n_diaria = dados['numeroDiarias'],
            v_diaria = dados['valorDiaria'],
            data_fim=data_fim,
            n_intranet=dados['codigoRelatorio'],
            usuario=dados['usuario'],
            descricao=dados.get('descricao', '')
        )
        
        db.session.add(viagem)
        db.session.commit()
        return viagem
        
    except Exception as e:
        db.session.rollback()
        raise APIError(str(e), 400)

def update_viagem(dados):
    try:
        viagem = RegistroViagens.query.get(dados['viagemId'])
        if not viagem:
            raise APIError('Viagem não encontrada', 404)
        
        # Atualizar os campos da viagem
        viagem.entidade_destino = dados['cidadeDestino']
        viagem.data_inicio = dados['dataSaida']
        viagem.tipo_viagem = dados['tipoViagem']
        viagem.n_diaria = dados['numeroDiarias']
        viagem.v_diaria = dados['valorDiaria']
        viagem.data_fim = dados['dataRetorno']
        viagem.n_intranet = dados['codigoRelatorio']
        viagem.usuario = dados['usuario']
        viagem.descricao = dados.get('descricao', '')
        
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        raise APIError(str(e), 400)
    
    
def deletar_viagem(viagem_id):
    try:
        viagem = RegistroViagens.query.get(viagem_id)
        if not viagem:
            raise APIError('Viagem não encontrada', 404)
        viagem.ativo = False
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise APIError(str(e), 400)

def consultar_viagens(viagemid):
    query = RegistroViagens.query.filter(RegistroViagens.id == int(viagemid)).first()
    
    if query:
        if query.entidade_destino:
            query.entidade_nome = Entidade.query.get(query.entidade_destino).nome
        if query.usuario:
            query.usuario_nome = Usuarios.query.get(query.usuario).usuario
        if query.data_inicio:
            query.data_inicio = query.data_inicio.strftime('%d/%m/%Y %H:%M')
        if query.data_fim:
            query.data_fim = query.data_fim.strftime('%d/%m/%Y %H:%M')    
            
    # if not query:
    #     raise APIError(f'Viagem não encontrada {query}', 404)
    return query
def listar_cidades():
    return Entidade.query.filter_by(ativo=True).all()