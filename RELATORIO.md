# Relatorio - API de Controle de Frota

**Aluno:** Daniel de Jesus Ramalhete - RU 5382406
**Disciplina:** Arquitetura e Desenvolvimento de APIs

## 1. Objetivo

API para gerenciar frotas: cadastro de veiculos, abastecimentos, manutencoes, motoristas e atribuicao de veiculo ao motorista.

## 2. Tecnologias

Python + FastAPI, SQLAlchemy (ORM), SQLite, Pydantic, PyJWT, Uvicorn.

## 3. Por que essas escolhas

- FastAPI: gera Swagger automatico e valida com Pydantic.
- SQLAlchemy: evita SQL na mao, cada classe vira tabela.
- SQLite: banco em arquivo, nao precisa instalar nada.
- Pydantic: valida os dados de entrada automaticamente.
- PyJWT: autenticacao com token de 2h.
- PATCH em vez de PUT: atualiza so os campos que mudaram.

## 4. Organizacao

src/banco/ conexao com o banco
src/modelos/ tabelas, schemas e regras de negocio
src/routes/ endpoints separados por tema
src/main/ configuracao do FastAPI

## 5. Banco e ORM

Tabelas: frotas, Abastecimento, Manutencoes, motoristas, usuarios.
Cada classe em modelo_banco.py vira tabela. FKs ligam abastecimentos e manutencoes ao carro. motoristas.carro_id e unique para garantir um motorista por carro.

## 6. Endpoints

| Metodo | Endpoint | O que faz | Respostas |
|---|---|---|---|
| POST | /api/auth/registrar | cria usuario | 200 / 400 |
| POST | /api/auth/login | gera token | 200 / 401 |
| GET | /api/veiculos/ | lista frotas | 200 |
| GET | /api/veiculos/{id} | busca por id | 200 / 404 |
| GET | /api/veiculos/buscar/placa/{placa} | busca por placa | 200 / 404 |
| POST | /api/veiculos/cadastro_frota | cadastra | 201 / 400 |
| PATCH | /api/veiculos/{id} | atualiza | 200 / 400 / 404 |
| DELETE | /api/veiculos/{id} | remove | 204 / 401 / 404 |
| POST | /api/veiculos/abastecimento | abastecimento | 201 / 404 |
| POST | /api/veiculos/manutencao | manutencao | 201 / 404 |
| GET | /api/motoristas/ | lista motoristas | 200 |
| POST | /api/motoristas/ | cria motorista | 201 |
| POST | /api/motoristas/{id}/atribuir-frota/{carro_id} | atribui | 200 / 400 / 404 |
| GET | /api/dashboard | resumo | 200 |

## 7. Validacao e erros

Pydantic valida entrada. Exemplos: placa repetida retorna 400, id inexistente retorna 404, DELETE sem token retorna 401, valor negativo retorna 422.

## 8. Autenticacao e CORS

JWT HS256 com 2h de validade. O DELETE e a evidencia de endpoint protegido: 401 sem token, 204 com token. Senha com SHA-256. CORS com allow_origins=["*"] para facilitar teste; em producao ficaria restrito.

## 9. Testes

tests/teste_fluxo.py testa cadastro, abastecimento, dashboard e DELETE com/sem token.

## 10. Como rodar

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py

Acesse http://127.0.0.1:8000/docs

## 11. Repositorio

https://github.com/dejesusramalheted-glitch/Projetos-Academicos

## 12. Consideracoes finais

Dificuldades: JWT (pacote jwt vs PyJWT), alinhar Pydantic com SQLAlchemy, retorno None no DELETE 204. Limitacoes: SHA-256 em vez de bcrypt, CORS aberto, sem paginacao. Melhorias: bcrypt, paginacao, pytest, deploy.
