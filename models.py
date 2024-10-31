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
    ativo = db.Column(db.Boolean, default=True)


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