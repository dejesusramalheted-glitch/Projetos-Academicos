# Relatório Técnico - API de Controle de Frota

## 1. Introdução
A API resolve o problema de gestão de frotas, permitindo cadastrar veículos, registrar abastecimentos e calcular a média de consumo (km/l).

## 2. Tecnologias e Justificativas
* **FastAPI:** Escolhido pela documentação automática (Swagger) e alta performance.
* **SQLAlchemy (ORM):** Mapeia as classes Python para o banco SQLite, garantindo integridade relacional (1:N de Carro para Abastecimento).
* **SQLite:** Banco leve, ideal para reprodução do projeto sem instalar servidores.
* **JWT:** Autenticação stateless e segura.

## 3. Arquitetura
O código está dividido em: `src/banco` (conexão), `src/modelos` (SQLAlchemy e Pydantic), `src/routes` (endpoints) e `src/main` (configuração FastAPI e CORS).

## 4. Banco de Dados e ORM
* `CarroDb`: id, modelo, placa, ano.
* `AbastecimentoDb`: id, km_inicial, km_atual, litros, valor, carro_id (FK).
* `UsuarioDb`: id, email, senha_hash.
O ORM garante que a exclusão e criação respeitem as regras do banco.

## 5. Endpoints e HTTP
| Método | Endpoint | Finalidade | Status |
|---|---|---|---|
| POST | /api/auth/registrar | Cadastrar usuário | 201/400 |
| POST | /api/auth/login | Login e Token | 200/401 |
| GET | /api/veiculos/{id} | Buscar veículo | 200/404 |
| POST | /api/veiculos/cadastro_frota | Criar veículo | 201/401 |
| POST | /api/veiculos/abastecimento | Registrar abastecimento | 201/401 |
| DELETE | /api/veiculos/{id} | Excluir veículo | 204/401 |

## 6. Validação, Autenticação e CORS
* **Validação:** Realizada pelo Pydantic. Dados inválidos retornam 400.
* **Autenticação:** Via JWT. O token é validado no Header `Authorization: Bearer <token>`.
* **CORS:** Configurado como `allow_origins=["*"]` para permitir testes. Em produção, seria restrito.

## 7. Evidências e Execução
Para executar: `python run.py`. O Swagger está disponível em `/docs` e serve como evidência de funcionamento e testes.

## 8. Repositório
(LINK DO SEU GITHUB AQUI)
