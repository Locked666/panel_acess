from models import RegistroViagens, Entidade, db
from utils.validators import validar_dados_viagem
from utils.exceptions import APIError
from datetime import datetime

def criar_viagem(dados):
    try:
        validar_dados_viagem(dados)
        # Converter datas
        try:
            data_inicio = datetime.strptime(dados['dataSaida'], '%Y-%m-%d')
            data_fim = datetime.strptime(dados['dataRetorno'], '%Y-%m-%d')
        except ValueError:
            raise APIError({'status': 'error', 'message': 'Formato de data inválido'},400) 
        viagem = RegistroViagens(
            entidade_destino=dados['cidadeDestino'],
            data_inicio=data_inicio,
            data_fim=data_fim,
            n_intranet=dados['codigoRelatorio'],
            tipo_viagem=dados.get('tipoViagem', ''),
            descricao=dados.get('descricao', '')
        )
        
        db.session.add(viagem)
        db.session.commit()
        return viagem
        
    except Exception as e:
        db.session.rollback()
        raise APIError(str(e), 400)

def listar_cidades():
    return Entidade.query.filter_by(ativo=True).all()