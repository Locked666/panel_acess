from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Entidade(db.Model):
    __tablename__ = 'entidades'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    ativo = db.Column(db.Boolean, default=True)




if __name__=='__main__':
    db.create_all()
    exit() 