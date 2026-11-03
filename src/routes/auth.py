from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import BaseModel

from src.banco.database import get_db
from src.modelos.modelo_banco import UsuarioDb
from src.modelos.servicos import auth_services

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


class LoginRequest(BaseModel):
    email: str
    senha: str


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credenciais_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = auth_services.decodificar_token(token)
    if payload is None:
        raise credenciais_invalidas

    email = payload.get("sub")
    if email is None:
        raise credenciais_invalidas

    usuario = db.query(UsuarioDb).filter(UsuarioDb.email == email).first()
    if usuario is None:
        raise credenciais_invalidas
    return usuario


@router.post("/registrar")
def registrar(dados: LoginRequest, db: Session = Depends(get_db)):
    if db.query(UsuarioDb).filter(UsuarioDb.email == dados.email).first():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado")
    novo = UsuarioDb(
        email=dados.email,
        senha_hash=auth_services.gerar_hash_senha(dados.senha),
    )
    db.add(novo)
    db.commit()
    return {"mensagem": "Usuário criado com sucesso!"}


@router.post("/login")
def login(dados: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioDb).filter(UsuarioDb.email == dados.email).first()
    if not usuario or not auth_services.verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
    token = auth_services.criar_token_acesso(usuario.email)
    return {"access_token": token, "token_type": "bearer"}
