from models import GastosViagens, RegistroViagens,DocumentosViagens, db
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
            arquivo=dados.get('arquivo'),
            estorno=dados.get('estorno', False)
        )
        
        db.session.add(gasto)
        db.session.commit()
        return gasto
        
    except Exception as e:
        db.session.rollback()
        raise APIError(str(e), 400)

def listar_gastos_por_viagem(viagem_id):
    try:
        gastos = GastosViagens.query.filter_by(
            viagem=viagem_id,
            ativo=True
        ).all()
        if not gastos:
            raise APIError('Nenhum gasto encontrado para esta viagem', 404)
        for gasto in gastos:
            if gasto.arquivo:
                arquivo = DocumentosViagens.query.get(gasto.arquivo)
                if arquivo:
                    gasto.documento = arquivo.arquivo
                else:
                    gasto.documento = None

        # if gastos.arquivo:
        #     for gasto in gastos:
        #         arquivo = DocumentosViagens.query.get(gasto.arquivo)
        #         if arquivo:
        #             gasto.arquivo = arquivo.arquivo
        #             gasto.tipo_documento = arquivo.tipo
        #         else:
        #             gasto.arquivo = None
        #             gasto.tipo_documento = None
        
        return gastos
    except Exception as e:
        db.session.rollback()
        raise APIError(str(e), 400)
    
    
    
    return 

def excluir_gasto(gasto_id):
    gasto = GastosViagens.query.get(gasto_id)
    if not gasto:
        raise APIError('Gasto não encontrado', 404)
    
    gasto.ativo = False
    db.session.commit()
    
if __name__ == '__main__':
    g = listar_gastos_por_viagem(60)
    print(g)