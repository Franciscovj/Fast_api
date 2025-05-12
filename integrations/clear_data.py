import json
import pandas as pd
import os

# Caminho onde os arquivos JSON estão armazenados
base_path = "json_files"

# Carrega o arquivo JSON com os dados dos jogos
with open(os.path.join(base_path, "jogos.json"), encoding="utf-8") as f:
    jogos = json.load(f)

# Carrega o arquivo JSON com os dados dos times
with open(os.path.join(base_path, "times.json"), encoding="utf-8") as f:
    times = json.load(f)

# Carrega o arquivo JSON com os dados das ligas
with open(os.path.join(base_path, "ligas.json"), encoding="utf-8") as f:
    ligas = json.load(f)

# Carrega o arquivo JSON com os dados das estatísticas dos jogos
with open(os.path.join(base_path, "estatisticas.json"), encoding="utf-8") as f:
    estatisticas = json.load(f)

# Carrega o arquivo JSON com os dados das odds dos jogos
with open(os.path.join(base_path, "odds.json"), encoding="utf-8") as f:
    odds = json.load(f)

# Cria dicionários com os times e ligas, indexados pelo ID, para acesso rápido
times_dict = {t["id"]: t for t in times}
ligas_dict = {l["id"]: l for l in ligas}

# Lista onde serão armazenados os dados finais combinando todas as informações relacionadas
dados_relacionados = []

# Itera sobre cada jogo para combinar os dados dos relacionamentos
for jogo in jogos:
    jogo_id = jogo["id"]

    # Busca os dados do time da casa, do time visitante e da liga usando os dicionários
    time_casa = times_dict.get(jogo["time_casa"], {})
    time_fora = times_dict.get(jogo["time_fora"], {})
    liga = ligas_dict.get(jogo["liga"], {})

    # Busca estatística relacionada ao jogo atual (assume que só há uma por jogo)
    estatistica = next((e for e in estatisticas if e["jogo"] == jogo_id), {})

    # Busca todas as odds associadas a esse jogo
    odds_do_jogo = [o for o in odds if o["jogo"] == jogo_id]

    # Para cada odd do jogo, monta um dicionário com todos os dados relacionados
    # Caso não tenha odds, ainda assim adiciona uma linha (com odds em branco)
    for odd in odds_do_jogo or [{}]:
        dados_relacionados.append({
            "Data": jogo["data"],
            "Liga": liga.get("nome"),
            "País Liga": liga.get("pais"),
            "Time Casa": time_casa.get("nome"),
            "Time Fora": time_fora.get("nome"),
            "Gols Casa": estatistica.get("gols_casa"),
            "Gols Fora": estatistica.get("gols_fora"),
            "Escanteios Casa": estatistica.get("escanteios_casa"),
            "Escanteios Fora": estatistica.get("escanteios_fora"),
            "Casa Aposta": odd.get("casa_aposta"),
            "Odd 1": odd.get("odd_1"),
            "Odd X": odd.get("odd_x"),
            "Odd 2": odd.get("odd_2"),
            "Data Odd": odd.get("data_hora"),
        })

# Converte a lista de dados combinados em um DataFrame do pandas
df = pd.DataFrame(dados_relacionados)

# Exporta o DataFrame para um arquivo Excel
df.to_excel("dados_relacionados.xlsx", index=False)

# Mensagem final indicando sucesso na geração do arquivo
print("✔ Arquivo Excel 'dados_relacionados.xlsx' criado com sucesso.")

