from models import Usuarios, GastosViagens, RegistroViagens, db


# def get_dashboard_data():
#     """
#     # Retrieve and aggregate data for the dashboard.
#     # """
#     # Total de Gastos por Viagem
    
#     gastos_por_viagem = (
#         db.session.query(
#             RegistroViagens.id,
#             db.func.sum(GastosViagens.valor).label('total_gastos')
#         )
#         .join(GastosViagens, RegistroViagens.id == GastosViagens.viagem)
#         .group_by(RegistroViagens.id)
#         .all()
#     )
    
#     # Total de Gastos Ultimos 30 dias
#     gastos_ultimos_30_dias = (
#         db.session.query(
#             db.func.sum(GastosViagens.valor).label('total_gastos')
#         )
#         .join(RegistroViagens, RegistroViagens.id == GastosViagens.viagem)
#         .filter(RegistroViagens.data >= db.func.datetime('now', '-30 days'))
#         .scalar()
#     )
#     # media de Gastos por Viagem
#     media_gastos_por_viagem = (
#         db.session.query(
#             db.func.avg(GastosViagens.valor).label('media_gastos')
#         )
#         .join(RegistroViagens, RegistroViagens.id == GastosViagens.viagem)
#         .scalar()
#     )
#     # Total de Gastos por Usuario
#     gastos_por_usuario = (
#         db.session.query(
#             Usuarios.id,
#             db.func.sum(GastosViagens.valor).label('total_gastos')
#         )
#         .join(RegistroViagens, RegistroViagens.id == GastosViagens.viagem)
#         .group_by(RegistroViagens.usuario)
#         .all()
#     )
    
#     return {
#         "gastos_por_viagem": gastos_por_viagem,
#         "gastos_ultimos_30_dias": gastos_ultimos_30_dias,
#         "media_gastos_por_viagem": media_gastos_por_viagem,
#         "gastos_por_usuario": gastos_por_usuario,
#     }
    
def get_dashboard_data():
    # Total de Gastos por Viagem
    gastos_por_viagem = (
        db.session.query(
            RegistroViagens.id,
            db.func.sum(GastosViagens.valor).label('total_gastos')
        )
        .join(GastosViagens, RegistroViagens.id == GastosViagens.viagem)
        .group_by(RegistroViagens.id)
        .all()
    )
    gastos_por_viagem = [
        {"viagem_id": row[0], "total_gastos": float(row[1]) if row[1] else 0.0}
        for row in gastos_por_viagem
    ]

    # Total de Gastos Últimos 30 dias
    gastos_ultimos_30_dias = (
        db.session.query(
            db.func.sum(GastosViagens.valor).label('total_gastos')
        )
        .join(RegistroViagens, RegistroViagens.id == GastosViagens.viagem)
        .filter(RegistroViagens.data >= db.func.datetime('now', '-30 days'))
        .scalar()
    )
    gastos_ultimos_30_dias = float(gastos_ultimos_30_dias) if gastos_ultimos_30_dias else 0.0

    # Média de Gastos por Viagem
    media_gastos_por_viagem = (
        db.session.query(
            db.func.avg(GastosViagens.valor).label('media_gastos')
        )
        .join(RegistroViagens, RegistroViagens.id == GastosViagens.viagem)
        .scalar()
    )
    media_gastos_por_viagem = float(media_gastos_por_viagem) if media_gastos_por_viagem else 0.0

    # Total de Gastos por Usuário
    gastos_por_usuario = (
        db.session.query(
            RegistroViagens.usuario,
            db.func.sum(GastosViagens.valor).label('total_gastos')
        )
        .join(GastosViagens, RegistroViagens.id == GastosViagens.viagem)
        .group_by(RegistroViagens.usuario)
        .all()
    )
    gastos_por_usuario = [
        {"usuario_id": row[0], "total_gastos": float(row[1]) if row[1] else 0.0}
        for row in gastos_por_usuario
    ]

    return {
        "gastos_por_viagem": gastos_por_viagem,
        "gastos_ultimos_30_dias": gastos_ultimos_30_dias,
        "media_gastos_por_viagem": media_gastos_por_viagem,
        "gastos_por_usuario": gastos_por_usuario,
    }
    
if __name__ == "__main__":
    #     # Total de Gastos Ultimos 30 dias
    g30 = get_dashboard_data()
    print(g30)       
    

    
    # # Total number of users
    # total_users = Usuarios.query.count()

    # # Total number of trips
    # total_trips = RegistroViagens.query.count()

    # # Total expenses
    # total_expenses = db.session.query(db.func.sum(GastosViagens.valor)).scalar() or 0

    # return {
    #     "total_users": total_users,
    #     "total_trips": total_trips,
    #     "total_expenses": total_expenses,
    # }
    pass