import requests
import random

BASE = "http://127.0.0.1:8000"

requests.post(f"{BASE}/api/auth/registrar", json={"email": "a@a.com", "senha": "123"})
r = requests.post(f"{BASE}/api/auth/login", json={"email": "a@a.com", "senha": "123"})
token = r.json()["access_token"]
H = {"Authorization": f"Bearer {token}"}

placa = f"ABC{random.randint(1000, 9999)}"
r = requests.post(f"{BASE}/api/veiculos/cadastro_frota", json={
    "modelo": "Fiat Uno", "placa": placa, "ano": 2020
})
print("cadastro frota:", r.status_code)
carro_id = r.json()["id"]

r = requests.post(f"{BASE}/api/veiculos/abastecimento", json={
    "km_inicial": 0, "km_atual": 500,
    "valor_abastecido": 200, "preco_litro": 5, "carro_id": carro_id
})
print("abastecimento:", r.status_code)

r = requests.get(f"{BASE}/api/dashboard")
print("dashboard:", r.status_code)

r = requests.delete(f"{BASE}/api/veiculos/{carro_id}")
print("delete sem token:", r.status_code, "(esperado 401)")

r = requests.delete(f"{BASE}/api/veiculos/{carro_id}", headers=H)
print("delete com token:", r.status_code, "(esperado 204)")
