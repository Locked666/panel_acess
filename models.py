from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property

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
    n_diaria = db.Column(db.String(100), comment='Número da diária')
    v_diaria = db.Column(db.Float, comment='Valor da diária')
    descricao = db.Column(db.String(100))
    n_intranet = db.Column(db.String(100), comment='Número da visita na intranet', default='0')
    veiculo = db.Column(db.String(100), comment='veículo')
    placa = db.Column(db.String(100), comment='Placa do veículo')
    km_inicial = db.Column(db.String(100), comment='KM inicial')
    km_final = db.Column(db.String(100), comment='KM final')
    n_combustivel = db.Column(db.String(100), comment='Número do combustível')
    total_gasto = db.Column(db.Float, comment='Total gasto na viagem', default=0.0)
    usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), comment='ID do usuário que registrou a viagem')
    ativo = db.Column(db.Boolean, default=True)
    data = db.Column(db.DateTime, default=db.func.now())

    entidade_rel = db.relationship('Entidade', backref='viagens', lazy='joined')
    # Na model RegistroViagens

    usuario_rel = db.relationship('Usuarios', backref='viagens', lazy='joined', foreign_keys=[usuario])

    
    @hybrid_property
    def total_gasto_calculado(self):
        """Versão sempre atualizada do total"""
        return self.gastos.filter_by(ativo=True, estorno=False).with_entities(
            db.func.coalesce(db.func.sum(GastosViagens.valor), 0.0)
        ).scalar()

def setup_triggers():
    @event.listens_for(GastosViagens, 'after_insert')
    @event.listens_for(GastosViagens, 'after_update')
    @event.listens_for(GastosViagens, 'after_delete')
    def update_total(mapper, connection, target):
        viagem_id = target.viagem
        novo_total = db.session.query(
            db.func.coalesce(db.func.sum(GastosViagens.valor), 0.0)
        ).filter(
            GastosViagens.viagem == viagem_id,
            GastosViagens.ativo == True,
            GastosViagens.estorno == False
        ).scalar()
        
        db.session.execute(
            db.update(RegistroViagens)
            .where(RegistroViagens.id == viagem_id)
            .values(total_gasto=novo_total)
        )


class GastosViagens(db.Model):
    __tablename__ = 'gastos_viagens'
    id = db.Column(db.Integer, primary_key=True)
    viagem = db.Column(db.Integer,db.ForeignKey('registro_viagens.id') ,nullable=False)
    data_gasto = db.Column(db.DateTime, default=db.func.now(), comment='Data do gasto')
    tipo_gasto = db.Column(db.String(100))
    n_documento = db.Column(db.String(100), comment='Número do documento')
    tipo_documento = db.Column(db.String(100), comment='Tipo do documento')
    descricao = db.Column(db.String(100))
    valor = db.Column(db.Float)   
    arquivo = db.Column(db.Integer, db.ForeignKey('documentos_viagens.id'), comment='ID do arquivo')
    ativo = db.Column(db.Boolean, default=True)
    estorno = db.Column(db.Boolean, default=False, comment='Se o gasto tem que ser estornado')
    data = db.Column(db.DateTime, default=db.func.now())   

class DocumentosViagens(db.Model):
    __tablename__ = 'documentos_viagens'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), comment='Tipo do documento')
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

class Usuarios(db.Model):
    __tablename__= 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(1000), nullable=True)
    acesso = db.Column(db.String(100))
    admin = db.Column(db.Boolean, default=False)
    data = db.Column(db.DateTime, default=db.func.now())
    ativo = db.Column(db.Boolean, default=True)




if __name__=='__main__':
    db.create_all()
    exit() 