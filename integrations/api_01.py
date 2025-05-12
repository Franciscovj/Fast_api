import requests

# URLs da API
BASE_URL = "http://127.0.0.1:8000"
jogos_url = f"{BASE_URL}/times/"

# Token de acesso
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc0NzA2ODMxMn0.JPyyNzGlsVCL0OZVIRcwLZ0-yAGUCq9bNExaeShLbtM"
headers = {"Authorization": f"Bearer {token}"}

# Solicita dados protegidos usando o token
jogos_response = requests.get(jogos_url, headers=headers)
if jogos_response.status_code == 200:
    print("Jogos:", jogos_response.json())
else:
    print("Falha ao obter jogos:", jogos_response.status_code)