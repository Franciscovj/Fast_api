import random
from datetime import datetime, timedelta
from faker import Faker
from app.models import Time, Liga, Jogo, Estatistica, Odd
from app.database import db

fake = Faker()
PAISES_FIXOS = ["Brasil", "Espanha", "Inglaterra", "Alemanha"]
CASAS_FIXAS = ["Bet365", "Betfair", "Sportingbet", "Pinnacle"]

def criar_times(n=40):
    times = []
    for _ in range(n):
        nome = fake.company()
        pais = random.choice(PAISES_FIXOS)
        time = Time.create(nome=nome, pais=pais)
        times.append(time)
    return times

def criar_ligas(n=5):
    ligas = []
    for _ in range(n):
        nome = fake.word().capitalize() + " League"
        pais = random.choice(PAISES_FIXOS)
        liga = Liga.create(nome=nome, pais=pais)
        ligas.append(liga)
    return ligas

def criar_jogos(times, ligas, n=100):
    jogos = []
    for _ in range(n):
        time_casa = random.choice(times)
        time_fora = random.choice([t for t in times if t != time_casa])
        liga = random.choice(ligas)
        dias = random.randint(-180, 180)  # Jogos passados ou futuros
        data = datetime.now() + timedelta(days=dias)
        jogo = Jogo.create(data=data, time_casa=time_casa.id, time_fora=time_fora.id, liga=liga.id)
        jogos.append(jogo)
    return jogos

def criar_estatisticas(jogos):
    estatisticas = []
    tempos_evento = ["jogo_inteiro", "primeiro_tempo", "segundo_tempo"]
    for jogo in jogos:
        estatistica = Estatistica.create(
            jogo=jogo.id,
            tempo_evento=random.choice(tempos_evento),
            gols_casa=random.randint(0, 5),
            gols_fora=random.randint(0, 5),
            escanteios_casa=random.randint(0, 10),
            escanteios_fora=random.randint(0, 10)
        )
        estatisticas.append(estatistica)
    return estatisticas

def criar_odds(jogos):
    odds = []
    for jogo in jogos:
        odd = Odd.create(
            jogo=jogo.id,
            casa_aposta=random.choice(CASAS_FIXAS),
            odd_1=round(random.uniform(1.5, 3.0), 2),
            odd_x=round(random.uniform(2.0, 3.5), 2),
            odd_2=round(random.uniform(1.5, 3.0), 2),
            data_hora=datetime.now() + timedelta(days=random.randint(-90, 90))  # Odds recentes e futuras
        )
        odds.append(odd)
    return odds

def run_seed():
    db.connect()
    db.create_tables([Time, Liga, Jogo, Estatistica, Odd])

    times = criar_times()
    ligas = criar_ligas()
    jogos = criar_jogos(times, ligas)
    estatisticas = criar_estatisticas(jogos)
    odds = criar_odds(jogos)

    print(f"{len(times)} times, {len(ligas)} ligas, {len(jogos)} jogos, {len(estatisticas)} estatísticas e {len(odds)} odds criados com sucesso.")
    db.close()

if __name__ == "__main__":
    run_seed()
