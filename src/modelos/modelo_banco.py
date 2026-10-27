from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from src.banco.database import Base


class CarroDb(Base):
    __tablename__="frotas"

    id = Column(Integer, primary_key=True, index=True)
    modelo = Column(String, nullable=False)
    placa = Column(String, unique=True, nullable=False)
    ano = Column(Integer, nullable=False)


class ManutencaoDb(Base):
    __tablename__="Manutencoes"

    id = Column(Integer, primary_key=True, index=True)
    servico_feito = Column(String, nullable=False)
    valor_cobrado = Column(Numeric, nullable=False)
    tempo_garantia = Column(String, nullable=False)


class AbastecimentoDb(Base):
    __tablename__ = "Abastecimento"
    id = Column(Integer, primary_key=True, index=True)
    km_inicial = Column(Integer, nullable=False)
    km_atual = Column(Integer, nullable=False)
    litros = Column(Numeric, nullable=False)
    valor_abastecido = Column(Numeric, nullable=False)
    preco_litro = Column(Numeric, nullable=False)  
    carro_id = Column(Integer, ForeignKey("frotas.id"), nullable=False)

class UsuarioDb(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    senha_hash = Column(String)

