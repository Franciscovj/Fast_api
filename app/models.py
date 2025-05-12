from peewee import *
from app.database import db
from enum import Enum

class BaseModel(Model):
    class Meta:
        database = db

class StatusJogo(Enum):
    AGENDADO = "agendado"
    EM_ANDAMENTO = "em_andamento"
    FINALIZADO = "finalizado"

class Time(BaseModel):
    nome = CharField(unique=True)
    pais = CharField()

class Liga(BaseModel):
    nome = CharField()
    pais = CharField()

class Jogo(BaseModel):
    data = DateField()
    time_casa = ForeignKeyField(Time, backref='jogos_casa')
    time_fora = ForeignKeyField(Time, backref='jogos_fora')
    liga = ForeignKeyField(Liga, backref='jogos')
    status = CharField(default=StatusJogo.AGENDADO.name, choices=[(status.name, status.value) for status in StatusJogo])

class Estatistica(BaseModel):
    jogo = ForeignKeyField(Jogo, backref='estatisticas')
    tempo_evento = CharField(default="jogo_inteiro")  
    gols_casa = IntegerField()
    gols_fora = IntegerField()
    escanteios_casa = IntegerField()
    escanteios_fora = IntegerField()

class Odd(BaseModel):
    jogo = ForeignKeyField(Jogo, backref='odds')
    casa_aposta = CharField()
    odd_1 = FloatField()
    odd_x = FloatField()
    odd_2 = FloatField()
    data_hora = DateTimeField()

    class Meta:
        indexes = (
            (('jogo', 'casa_aposta'), True),
        )
        
# Aqui acrescentamos o modelo de usuário
# para autenticação        
class Usuario(BaseModel):
    username = CharField(unique=True)
    senha = CharField()  # Aqui você pode armazenar hash da senha        
