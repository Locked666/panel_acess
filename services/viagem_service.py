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
    # Converter strings para objetos datetime
    try:
        # Formato ISO 8601 (2025-04-15T16:46)
        data_inicio = datetime.fromisoformat(dados['dataSaida'])
        data_fim = datetime.fromisoformat(dados['dataRetorno'])
    except ValueError as e:
        raise APIError({'status': 'error', 'message': f'Formato de data inválido: {str(e)}'}, 400)
    try:
        viagem = RegistroViagens.query.get(dados['viagemId'])
        if not viagem:
            raise APIError('Viagem não encontrada', 404)
        
        # Atualizar os campos da viagem
        viagem.entidade_destino = dados['cidadeDestino']
        viagem.data_inicio = data_inicio
        viagem.tipo_viagem = dados['tipoViagem']
        viagem.n_diaria = dados['numeroDiarias']
        viagem.v_diaria = dados['valorDiaria']
        viagem.data_fim = data_fim
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
            query.data_inicio = query.data_inicio.strftime('%Y-%m-%d %H:%M')
        if query.data_fim:
            query.data_fim = query.data_fim.strftime('%Y-%m-%d %H:%M')    
            
    # if not query:
    #     raise APIError(f'Viagem não encontrada {query}', 404)
    return query

def parse_datetime(data_str):
    try:
        return datetime.strptime(data_str, "%Y-%m-%dT%H:%M")
    except (TypeError, ValueError):
        return None

def to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None    
# def listar_viagens(**kwargs):
#     viagens = RegistroViagens.query.filter_by(ativo=True).all()
#     if kwargs.get('usuario'):
#         viagens = RegistroViagens.query.filter_by(usuario=kwargs.get('usuario')).all()
#     if kwargs.get('entidade'):
#         viagens = RegistroViagens.query.filter_by(entidade_destino=kwargs.get('entidade')).all()
#     if kwargs.get('data_inicio'):
#         viagens = RegistroViagens.query.filter(RegistroViagens.data_inicio >= kwargs.get('data_inicio')).all()
#     if kwargs.get('data_fim'):
#         viagens = RegistroViagens.query.filter(RegistroViagens.data_fim <= kwargs.get('data_fim')).all()
        
#     for viagem in viagens:
#         if viagem.entidade_destino:
#             viagem.entidade_nome = Entidade.query.get(viagem.entidade_destino).nome
#         if viagem.usuario:
#             viagem.usuario_nome = Usuarios.query.get(viagem.usuario).usuario
#         if viagem.data_inicio:
#             viagem.data_inicio = viagem.data_inicio.strftime('%d/%m/%Y %H:%M') #('%Y-%m-%d %H:%M')
#         if viagem.data_fim:
#             viagem.data_fim = viagem.data_fim.strftime('%d/%m/%Y %H:%M')
#     return viagens
def listar_viagens(**kwargs):
    query = db.session.query(
        RegistroViagens,
        Entidade.nome.label('entidade_nome'),
        Usuarios.usuario.label('usuario_nome')
    ).outerjoin(Entidade, RegistroViagens.entidade_destino == Entidade.id)\
     .outerjoin(Usuarios, RegistroViagens.usuario == Usuarios.id)\
     .filter(RegistroViagens.ativo == True)

    if kwargs.get('usuario'):
        query = query.filter(RegistroViagens.usuario == kwargs['usuario'])
    if kwargs.get('entidade'):
        query = query.filter(RegistroViagens.entidade_destino == kwargs['entidade'])
    if kwargs.get('data_inicio'):
        query = query.filter(RegistroViagens.data_inicio >= kwargs['data_inicio'])
    if kwargs.get('data_fim'):
        query = query.filter(RegistroViagens.data_fim <= kwargs['data_fim'])
    if kwargs.get('tipo_viagem'):
        query = query.filter(RegistroViagens.tipo_viagem == kwargs['tipo_viagem'])
    if kwargs.get('id'):
        query = query.filter(RegistroViagens.id == kwargs['id'])
    if kwargs.get('n_intranet'):
        query = query.filter(RegistroViagens.n_intranet == kwargs['n_intranet'])

    results = query.all()

    viagens = []
    for viagem, entidade_nome, usuario_nome in results:
        viagens.append({
            'id': viagem.id,
            'entidade': entidade_nome,
            'entidade_id': viagem.entidade_destino,
            'data_inicio': viagem.data_inicio.strftime('%d/%m/%Y %H:%M') if viagem.data_inicio else '',
            'data_fim': viagem.data_fim.strftime('%d/%m/%Y %H:%M') if viagem.data_fim else '',
            'tipo_viagem': viagem.tipo_viagem,
            'n_diarias': int(viagem.n_diaria),
            'valor_diaria': float(viagem.v_diaria),
            'descricao': viagem.descricao,
            'n_intranet': viagem.n_intranet,
            'total_gasto': viagem.total_gasto,
            'usuario_nome': usuario_nome
        })

    return viagens

def listar_cidades():
    return Entidade.query.filter_by(ativo=True).all()