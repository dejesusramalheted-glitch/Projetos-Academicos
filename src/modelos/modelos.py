
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from .modelo_banco import CarroDb


class Login(BaseModel):
    email: str
    senha: str
    

class CarroBase(BaseModel):
    modelo: str
    placa: str
    ano: int

class CriaCarro(CarroBase):
    pass

class CarroResposta(CarroBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
   

class ManutencaoBase(BaseModel):
    servico: str
    valor: float = Field(..., gt=0) 
    garantia: str

class CriaManutencao(ManutencaoBase):
    pass 

class ManutencaoResposta(CriaManutencao): 
    id: int
    model_config = ConfigDict(from_attributes=True)

class CriaAbastecimento(BaseModel):
    km_inicial: int
    km_atual: int
    valor_abastecido: float = Field(..., gt=0, description="Valor pago em R$")
    preco_litro: float = Field(..., gt=0, description="Preço do combustível em R$/litro")
    carro_id: int

    model_config = ConfigDict(from_attributes=True)

class AbastecimentoCriado(CriaAbastecimento):
    pass 


class MediaVeiculo(BaseModel):
    id: int
    carro_id: int
    km_inicial: int
    km_atual: int
    km_percorrido: int
    valor_abastecido: float
    preco_litro: float
    litros: float
    media_veiculo: float 

    model_config = ConfigDict(from_attributes=True)


