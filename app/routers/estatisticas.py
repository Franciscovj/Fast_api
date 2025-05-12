from fastapi import APIRouter, HTTPException, Depends
from app.models import Estatistica
from app.schemas import EstatisticaCreate
from app.auth import get_current_user  # importe seu verificador de token

# Todas as rotas aqui exigirão token válido
router = APIRouter(
    prefix="/estatisticas",
    tags=["estatisticas"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/")
def criar_estatistica(est: EstatisticaCreate):
    return Estatistica.create(**est.model_dump())

@router.get("/")
def listar_estatistica():
    return [stats.__data__ for stats in Estatistica.select()]

@router.get("/{id}")
def obter_estatistica(id: int):
    stats = Estatistica.get_or_none(Estatistica.id == id)
    if not stats:
        raise HTTPException(status_code=404, detail="Estatística não encontrada")
    return stats.__data__

@router.put("/{id}")
def atualizar_estatistica(id: int, dados: EstatisticaCreate):
    stats = Estatistica.get_or_none(Estatistica.id == id)
    if not stats:
        raise HTTPException(status_code=404, detail="Estatística não encontrada")
    stats.jogo = dados.jogo
    stats.tempo_evento = dados.tempo_evento
    stats.gols_casa = dados.gols_casa
    stats.gols_fora = dados.gols_fora
    stats.escanteios_casa = dados.escanteios_casa
    stats.escanteios_fora = dados.escanteios_fora
    stats.save()
    return stats.__data__

@router.delete("/{id}")
def deletar_estatistica(id: int):
    stats = Estatistica.get_or_none(Estatistica.id == id)
    if not stats:
        raise HTTPException(status_code=404, detail="Estatística não encontrada")
    stats.delete_instance()
    return {"detail": "Estatística deletada com sucesso"}
