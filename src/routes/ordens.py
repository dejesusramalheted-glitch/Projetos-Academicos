from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Importações padronizadas começando com 'src.'
from src.modelos.modelos import CarroBase, CarroResposta, CriaAbastecimento, AbastecimentoCriado, MediaVeiculo
from src.modelos.modelo_banco import CarroDb, AbastecimentoDb
from src.banco.database import get_db
from src.modelos.servicos.services import calcular_media  


orden = APIRouter()

# Leitura
@orden.get("/inicial")
def teste():
    return {"MINHA API ESTA NO AR!!"}


@orden.get("/{carro_id}", response_model=CarroResposta)
def carros(carro_id: int, db: Session = Depends(get_db)):
    carro = db.query(CarroDb).get(carro_id)
    if not carro:
        raise HTTPException(status_code=404, detail="Carro nao cadastrado")
    return carro

# Criacao
@orden.post("/cadastro_frota", response_model=CarroResposta)
def criar_veiculo(veiculo: CarroBase, db: Session = Depends(get_db)):
    novo = CarroDb(**veiculo.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@orden.post("/abastecimento", response_model=MediaVeiculo)
def abastecimento_veiculo(
    veiculo_abastecido: CriaAbastecimento,
    db: Session = Depends(get_db),
):
    carro = db.query(CarroDb).get(veiculo_abastecido.carro_id)
    if not carro:
        raise HTTPException(status_code=404, detail="Carro não encontrado.")

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
        **calculo
    )

# Delete
@orden.delete("/{carro_id}")
def deletar_carro(carro_id: int, db: Session = Depends(get_db)):
    carro = db.query(CarroDb).get(carro_id)
    if not carro:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    db.delete(carro)
    db.commit()
    return {"ok": True}