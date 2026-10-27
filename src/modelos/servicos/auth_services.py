import jwt
import hashlib
from datetime import datetime, timedelta

SECRET_KEY = "chave_secreta_simples_para_o_trabalho"
ALGORITHM = "HS256"

def gerar_hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    return gerar_hash_senha(senha_plana) == senha_hash

def criar_token_acesso(email: str) -> str:
    dados = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=2)
    }
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)

def decodificar_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return None