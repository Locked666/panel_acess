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