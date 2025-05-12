from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

# Modelos para criar
class TimeCreate(BaseModel):
    nome: str
    pais: str

class LigaCreate(BaseModel):
    nome: str
    pais: str

class JogoCreate(BaseModel):
    data: date
    time_casa: int
    time_fora: int
    liga: int
    status: str = "agendado"

class EstatisticaCreate(BaseModel):
    jogo: int
    tempo_evento: str = "jogo_inteiro"
    gols_casa: int
    gols_fora: int
    escanteios_casa: int
    escanteios_fora: int

class OddCreate(BaseModel):
    jogo: int
    casa_aposta: str
    odd_1: float
    odd_x: float
    odd_2: float
    data_hora: datetime

# Modelos para atualização (permitindo campos opcionais)
class TimeUpdate(BaseModel):
    nome: Optional[str] = None
    pais: Optional[str] = None

class LigaUpdate(BaseModel):
    nome: Optional[str] = None
    pais: Optional[str] = None

class JogoUpdate(BaseModel):
    data: Optional[date] = None
    time_casa: Optional[int] = None
    time_fora: Optional[int] = None
    liga: Optional[int] = None
    status: Optional[str] = "agendado"

class EstatisticaUpdate(BaseModel):
    jogo: Optional[int] = None
    tempo_evento: Optional[str] = "jogo_inteiro"
    gols_casa: Optional[int] = None
    gols_fora: Optional[int] = None
    escanteios_casa: Optional[int] = None
    escanteios_fora: Optional[int] = None

class OddUpdate(BaseModel):
    jogo: Optional[int] = None
    casa_aposta: Optional[str] = None
    odd_1: Optional[float] = None
    odd_x: Optional[float] = None
    odd_2: Optional[float] = None
    data_hora: Optional[datetime] = None
