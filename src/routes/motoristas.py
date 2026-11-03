from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.banco.database import get_db
from src.modelos.modelo_banco import MotoristaDb, CarroDb
from src.routes.auth import get_current_user

orden = APIRouter()


class CriaMotorista(BaseModel):
    nome: str
    cnh: str


@orden.get("/")
def listar_motoristas(db: Session = Depends(get_db)):
    return db.query(MotoristaDb).all()


@orden.post("/", dependencies=[Depends(get_current_user)])
def criar_motorista(dados: CriaMotorista, db: Session = Depends(get_db)):
    novo = MotoristaDb(nome=dados.nome, cnh=dados.cnh)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@orden.post("/{motorista_id}/atribuir-frota/{carro_id}", dependencies=[Depends(get_current_user)])
def atribuir_frota(motorista_id: int, carro_id: int, db: Session = Depends(get_db)):
    motorista = db.query(MotoristaDb).get(motorista_id)
    carro = db.query(CarroDb).get(carro_id)
    if not motorista or not carro:
        raise HTTPException(404, "Motorista ou carro não encontrado")
    if db.query(MotoristaDb).filter(MotoristaDb.carro_id == carro_id).first():
        raise HTTPException(400, "Frota já atribuída a outro motorista")
    motorista.carro_id = carro_id
    db.commit()
    return {"ok": True, "motorista": motorista.nome, "placa": carro.placa}
