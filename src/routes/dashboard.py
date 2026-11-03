from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.banco.database import get_db
from src.modelos.modelo_banco import CarroDb, ManutencaoDb, MotoristaDb
from src.modelos.servicos.services import (
    frota_com_mais_consumo,
    frota_com_mais_manutencoes,
    total_gasto_mes,
)
from src.routes.auth import get_current_user

orden = APIRouter()


@orden.get("/dashboard", dependencies=[Depends(get_current_user)])
def dashboard(db: Session = Depends(get_db)):
    return {
        "frotas": {
            "total": db.query(CarroDb).count(),
            "lista": db.query(CarroDb).all(),
        },
        "manutencoes": {
            "ultimas": (
                db.query(ManutencaoDb)
                .order_by(ManutencaoDb.data.desc())
                .limit(5).all()
            ),
            "frota_mais_manutencoes": frota_com_mais_manutencoes(db),
        },
        "combustivel": {
            "frota_mais_consumo": frota_com_mais_consumo(db),
            "total_gasto_mes": total_gasto_mes(db),
        },
        "motoristas": {"total": db.query(MotoristaDb).count()},
    }
