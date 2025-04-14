from models import GastosViagens, RegistroViagens, db
from utils.validators import validar_dados_gasto
from utils.exceptions import APIError

def criar_gasto(dados):
    try:
        validar_dados_gasto(dados)
        
        gasto = GastosViagens(
            viagem=dados['viagemId'],
            tipo_gasto=dados['tipoGasto'],
            descricao=dados['descricao'],
            valor=dados['valor'],
            estorno=dados.get('estorno', False)
        )
        
        db.session.add(gasto)
        db.session.commit()
        return gasto
        
    except Exception as e:
        db.session.rollback()
        raise APIError(str(e), 400)

def listar_gastos_por_viagem(viagem_id):
    return GastosViagens.query.filter_by(
        viagem=viagem_id,
        ativo=True
    ).all()

def excluir_gasto(gasto_id):
    gasto = GastosViagens.query.get(gasto_id)
    if not gasto:
        raise APIError('Gasto não encontrado', 404)
    
    gasto.ativo = False
    db.session.commit()