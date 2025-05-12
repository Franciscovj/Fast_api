from fastapi import APIRouter, HTTPException, Depends
from app.models import Time
from app.schemas import TimeCreate, TimeUpdate
from app.auth import get_current_user

# Todas as rotas deste router exigirão token válido
router = APIRouter(
    prefix="/times",
    tags=["times"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/")
def criar_time(time: TimeCreate):
    return Time.create(**time.model_dump())

@router.get("/")
def listar_times():
    return [time.__data__ for time in Time.select()]

@router.get("/{id}")
def obter_time(id: int):
    time = Time.get_or_none(Time.id == id)
    if not time:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    return time.__data__

@router.put("/{id}")
def atualizar_time(id: int, time_dados: TimeUpdate):
    time = Time.get_or_none(Time.id == id)
    if not time:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    time.nome = time_dados.nome
    time.pais = time_dados.pais
    time.save()
    return time.__data__

@router.delete("/{id}")
def deletar_time(id: int):
    time = Time.get_or_none(Time.id == id)
    if not time:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    time.delete_instance()
    return {"detail": "Time deletado com sucesso"}
