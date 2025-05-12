import requests
import json
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("API_KEY")

endpoint = [ 
    'jogos',
    'times',
    'ligas',
    'estatisticas',
    'odds'
            
            ]

def main(endpoint):
    # Token de autorização
    token = API_KEY
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(f"http://127.0.0.1:8000/{endpoint}", headers=headers)

    if response.status_code == 200:
        data = response.json()
        if not os.path.exists("json_files"):
            os.makedirs("json_files")
        with open(f"json_files/{endpoint}.json", "w") as f: 
            json.dump(data, f, indent=4)
        #print(data)

    else:
        print(f"Erro ao fazer requisição: {response.status_code}")

if __name__ == "__main__":
   for i in endpoint:
        main(i)
        print('final da coleta')