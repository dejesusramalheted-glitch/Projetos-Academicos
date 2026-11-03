# API de Controle de Frota

Trabalho da Uninter - Arquitetura e Desenvolvimento de APIs.

API em FastAPI para gerenciar frotas: cadastro de veiculos, abastecimentos, manutencoes, motoristas e atribuicao de veiculo ao motorista.

## Como rodar

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py

Abre em http://127.0.0.1:8000/docs. O banco carros.db e criado sozinho na primeira execucao.

## Endpoints

- POST /api/auth/registrar - cria usuario
- POST /api/auth/login - retorna token JWT
- GET /api/veiculos/ - lista frotas
- GET /api/veiculos/{id} - busca por id
- GET /api/veiculos/buscar/placa/{placa} - busca por placa
- POST /api/veiculos/cadastro_frota - cadastra (201)
- PATCH /api/veiculos/{id} - atualiza
- DELETE /api/veiculos/{id} - remove (204, precisa token)
- POST /api/veiculos/abastecimento - registra abastecimento
- POST /api/veiculos/manutencao - registra manutencao
- GET /api/motoristas/ - lista motoristas
- POST /api/motoristas/ - cadastra motorista
- POST /api/motoristas/{id}/atribuir-frota/{carro_id} - atribui
- GET /api/dashboard - resumo geral

## Exemplos

Cadastrar frota:
curl -X POST http://127.0.0.1:8000/api/veiculos/cadastro_frota -H 'Content-Type: application/json' -d '{"modelo":"Fiat Uno","placa":"ABC1234","ano":2020}'

Login:
curl -X POST http://127.0.0.1:8000/api/auth/login -H 'Content-Type: application/json' -d '{"email":"a@a.com","senha":"123"}'

Deletar (precisa token):
curl -X DELETE http://127.0.0.1:8000/api/veiculos/1 -H 'Authorization: Bearer SEU_TOKEN'

## Autenticacao

Login retorna token JWT com validade de 2h. A rota DELETE /api/veiculos/{id} esta protegida: sem token retorna 401, com token retorna 204. No Swagger, use o botao Authorize.

Senha e hasheada com SHA-256.

## Teste

Com a API rodando: python tests/teste_fluxo.py

## Repositorio

https://github.com/dejesusramalheted-glitch/Projetos-Academicos
