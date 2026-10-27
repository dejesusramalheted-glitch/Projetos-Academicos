# API de Controle de Frota e Abastecimento
Atividade Prática - Uninter (Arquitetura e Desenvolvimento de APIs)

## Tecnologias
* Python 3, FastAPI, SQLite, SQLAlchemy (ORM), PyJWT, Pydantic.

## Como executar
1. Ative o ambiente virtual: `source venv/bin/activate`
2. Instale as dependências: `pip install -r requirements.txt`
3. Rode o projeto: `python run.py`
4. Acesse o Swagger: http://127.0.0.1:8000/docs

## Autenticação
1. Cadastre-se em `POST /api/auth/registrar`.
2. Faça login em `POST /api/auth/login` e copie o `access_token`.
3. No Swagger, clique em "Authorize" e insira o token.

## Endpoints Principais
* POST /api/auth/registrar - Criar usuário
* POST /api/auth/login - Login (gera token)
* GET /api/veiculos/{id} - Buscar veículo
* POST /api/veiculos/cadastro_frota - Criar veículo (Protegido)
* POST /api/veiculos/abastecimento - Registrar abastecimento (Protegido)
* DELETE /api/veiculos/{id} - Deletar veículo (Protegido)
