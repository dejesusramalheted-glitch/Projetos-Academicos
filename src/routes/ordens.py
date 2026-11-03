from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.modelos.modelos import (
    CarroBase, CarroResposta, CriaAbastecimento,
     MediaVeiculo, CriaManutencao, ManutencaoResposta,
)
from src.modelos.modelo_banco import CarroDb, AbastecimentoDb, ManutencaoDb
from src.banco.database import get_db
from src.modelos.servicos.services import calcular_media
from src.routes.auth import get_current_user

orden = APIRouter()


@orden.get("/inicial")
def teste():
    return {"MINHA API ESTA NO AR!!"}


@orden.get("/", response_model=list[CarroResposta])
def listar_frotas(db: Session = Depends(get_db)):
    return db.query(CarroDb).all()


@orden.get("/buscar/placa/{placa}", response_model=CarroResposta)
def buscar_por_placa(placa: str, db: Session = Depends(get_db)):
    carro = db.query(CarroDb).filter(CarroDb.placa == placa).first()
    if not carro:
        raise HTTPException(404, "Placa não encontrada")
    return carro


@orden.post("/cadastro_frota", response_model=CarroResposta, status_code=201)
def criar_veiculo(veiculo: CarroBase, db: Session = Depends(get_db)):
    novo = CarroDb(**veiculo.model_dump())
    db.add(novo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Placa já cadastrada")
    db.refresh(novo)
    return novo


@orden.get("/{carro_id}", response_model=CarroResposta)
def carros(carro_id: int, db: Session = Depends(get_db)):
    carro = db.query(CarroDb).get(carro_id)
    if not carro:
        raise HTTPException(404, "Carro nao cadastrado")
    return carro


@orden.post("/abastecimento", response_model=MediaVeiculo, status_code=201)
def abastecimento_veiculo(
    veiculo_abastecido: CriaAbastecimento,
    db: Session = Depends(get_db),
):
    carro = db.query(CarroDb).get(veiculo_abastecido.carro_id)
    if not carro:
        raise HTTPException(404, "Carro não encontrado.")

    litros = veiculo_abastecido.valor_abastecido / veiculo_abastecido.preco_litro

    novo = AbastecimentoDb(
        km_inicial=veiculo_abastecido.km_inicial,
        km_atual=veiculo_abastecido.km_atual,
        valor_abastecido=veiculo_abastecido.valor_abastecido,
        preco_litro=veiculo_abastecido.preco_litro,
        litros=litros,
        carro_id=veiculo_abastecido.carro_id,
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)

    calculo = calcular_media(novo)

    return MediaVeiculo(
        id=novo.id,
        carro_id=novo.carro_id,
        km_inicial=novo.km_inicial,
        km_atual=novo.km_atual,
        valor_abastecido=float(novo.valor_abastecido),
        preco_litro=float(novo.preco_litro),
        litros=float(novo.litros),
        **calculo,
    )
    


@orden.post("/manutencao", response_model=ManutencaoResposta, status_code=201)
def criar_manutencao(dados: CriaManutencao, carro_id: int, db: Session = Depends(get_db)):
    carro = db.query(CarroDb).get(carro_id)
    if not carro:
        raise HTTPException(404, "Carro não encontrado")
    nova = ManutencaoDb(
        servico_feito=dados.servico,
        valor_cobrado=dados.valor,
        tempo_garantia=dados.garantia,
        carro_id=carro_id,
    )
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


@orden.patch("/{carro_id}", response_model=CarroResposta)
def atualizar_carro(carro_id: int, dados: CarroBase, db: Session = Depends(get_db)):
    carro = db.query(CarroDb).get(carro_id)
    if not carro:
        raise HTTPException(404, "Carro não encontrado")
    for campo, valor in dados.model_dump().items():
        setattr(carro, campo, valor)
    db.commit()
    db.refresh(carro)
    return carro


@orden.delete("/{carro_id}", status_code=204, dependencies=[Depends(get_current_user)])
def deletar_carro(carro_id: int, db: Session = Depends(get_db)):
    carro = db.query(CarroDb).get(carro_id)
    if not carro:
        raise HTTPException(404, "Carro não encontrado")
    db.delete(carro)
    db.commit()
