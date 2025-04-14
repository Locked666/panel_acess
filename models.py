from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

db = SQLAlchemy()

class Entidade(db.Model):
    __tablename__ = 'entidades'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    usuario = db.Column(db.String(100))
    data = db.Column(db.DateTime)
    acesso = db.Column(db.String(100))
    tipo = db.Column(db.String(100))
    ativo = db.Column(db.Boolean, default=True)

class ConfigAcesso(db.Model):
    __tablename__ = 'config_acesso'

    id = db.Column(db.Integer, primary_key=True)
    entidade = db.Column(db.Integer,db.ForeignKey('entidades.id') ,nullable=False)
    tipo_conexao = db.Column(db.Integer, nullable=False, comment='Tipo de conexão: 1 - TeamViewer, 2 - QSConnect, 3 - AnyDesk, etc.')
    id_conexao = db.Column(db.String(100), comment = 'ID da conexão ou código de acesso ou host remoto no caso do QSConnect')
    port_conexao = db.Column(db.Integer, comment = 'Porta de conexão no caso do QSConnect')
    usuario = db.Column(db.String(100), comment = 'Usuário de acesso')
    senha = db.Column(db.String(100), comment = 'Senha de acesso')
    data = db.Column(db.DateTime, default=db.func.now())
    ativo = db.Column(db.Boolean, default=True)    

    entidade_rel = db.relationship('Entidade', backref='acessos', lazy='joined')

class RegistroViagens(db.Model):
    __tablename__ = 'registro_viagens'

    id = db.Column(db.Integer, primary_key=True)
    entidade_destino = db.Column(db.Integer,db.ForeignKey('entidades.id') ,nullable=False)
    data_inicio = db.Column(db.DateTime)
    data_fim = db.Column(db.DateTime)
    tipo_viagem = db.Column(db.String(100))
    descricao = db.Column(db.String(100))
    n_intranet = db.Column(db.String(100), comment='Número da visita na intranet', default='0')
    veiculo = db.Column(db.String(100), comment='veículo')
    placa = db.Column(db.String(100), comment='Placa do veículo')
    km_inicial = db.Column(db.String(100), comment='KM inicial')
    km_final = db.Column(db.String(100), comment='KM final')
    n_combustivel = db.Column(db.String(100), comment='Número do combustível')
    usuario = db.Column(db.String(100))
    ativo = db.Column(db.Boolean, default=True)
    data = db.Column(db.DateTime, default=db.func.now())

    entidade_rel = db.relationship('Entidade', backref='viagens', lazy='joined')


class GastosViagens(db.Model):
    __tablename__ = 'gastos_viagens'
    id = db.Column(db.Integer, primary_key=True)
    viagem = db.Column(db.Integer,db.ForeignKey('registro_viagens.id') ,nullable=False)
    tipo_gasto = db.Column(db.String(100))
    descricao = db.Column(db.String(100))
    valor = db.Column(db.Float)   
    arquivo = db.Column(db.Integer, db.ForeignKey('documentos_viagens.id'), comment='ID do arquivo')
    ativo = db.Column(db.Boolean, default=True)
    estorno = db.Column(db.Boolean, default=False, comment='Se o gasto tem que ser estornado')
    data = db.Column(db.DateTime, default=db.func.now())   

class DocumentosViagens(db.Model):
    __tablename__ = 'documentos_viagens'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=db.func.now())
    arquivo = db.Column(db.String(300)) # Caminho do arquivo.

class Log(db.Model):
    __tablename__= 'log'

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), nullable=False)
    entidade = db.Column(db.String(100), nullable=False)
    acesso = db.Column(db.String(100))
    data = db.Column(db.DateTime, default=db.func.now())
    ativo = db.Column(db.Boolean, default=True)




if __name__=='__main__':
    db.create_all()
    exit() 