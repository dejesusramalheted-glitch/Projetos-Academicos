from sqlalchemy import func
from src.modelos.modelo_banco import AbastecimentoDb, CarroDb, ManutencaoDb


def calcular_media(abastecimento):
    km_percorrido = abastecimento.km_atual - abastecimento.km_inicial
    media = km_percorrido / abastecimento.litros if abastecimento.litros > 0 else 0
    return {
        "km_percorrido": km_percorrido,
        "media_veiculo": round(float(media), 2),
    }


def calcular_media_frota(carro_id: int, db):
    abastecimentos = (
        db.query(AbastecimentoDb)
        .filter(AbastecimentoDb.carro_id == carro_id)
        .order_by(AbastecimentoDb.km_atual.asc())
        .all()
    )
    if len(abastecimentos) < 2:
        return {"media_veiculo": 0.0, "total_litros": 0.0, "km_percorrido": 0}
    primeiro = abastecimentos[0]
    ultimo = abastecimentos[-1]
    km_total = ultimo.km_atual - primeiro.km_inicial
    litros_total = sum(float(a.litros) for a in abastecimentos[1:])
    media = km_total / litros_total if litros_total > 0 else 0.0
    return {
        "media_veiculo": round(media, 2),
        "total_litros": round(litros_total, 2),
        "km_percorrido": km_total,
    }


def frota_com_mais_consumo(db):
    resultado = (
        db.query(
            CarroDb.placa, CarroDb.modelo,
            func.sum(AbastecimentoDb.litros).label("total_litros"),
        )
        .join(AbastecimentoDb, AbastecimentoDb.carro_id == CarroDb.id)
        .group_by(CarroDb.id)
        .order_by(func.sum(AbastecimentoDb.litros).desc())
        .first()
    )
    if not resultado:
        return None
    return {"placa": resultado.placa, "modelo": resultado.modelo,
            "total_litros": float(resultado.total_litros)}


def frota_com_mais_manutencoes(db):
    resultado = (
        db.query(
            CarroDb.placa, CarroDb.modelo,
            func.count(ManutencaoDb.id).label("total"),
        )
        .join(ManutencaoDb, ManutencaoDb.carro_id == CarroDb.id)
        .group_by(CarroDb.id)
        .order_by(func.count(ManutencaoDb.id).desc())
        .first()
    )
    if not resultado:
        return None
    return {"placa": resultado.placa, "modelo": resultado.modelo,
            "total_manutencoes": resultado.total}


def total_gasto_mes(db):
    total = db.query(func.sum(AbastecimentoDb.valor_abastecido)).scalar()
    return float(total) if total else 0.0
