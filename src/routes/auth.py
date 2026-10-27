from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.banco.database import get_db
from src.modelos.modelo_banco import UsuarioDb
from src.modelos.servicos import auth_services

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    senha: str

@router.post("/registrar")
def registrar(dados: LoginRequest, db: Session = Depends(get_db)):
    usuario_existente = db.query(UsuarioDb).filter(UsuarioDb.email == dados.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    
    novo_usuario = UsuarioDb(
        email=dados.email, 
        senha_hash=auth_services.gerar_hash_senha(dados.senha)
    )
    db.add(novo_usuario)
    db.commit()
    return {"mensagem": "Usuário criado com sucesso!"}

@router.post("/login")
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioDb).filter(UsuarioDb.email == dados.email).first()
    
    if not usuario or not auth_services.verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
    
    token = auth_services.criar_token_acesso(usuario.email)
    return {"access_token": token, "token_type": "bearer"}