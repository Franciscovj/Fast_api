from fastapi import APIRouter, HTTPException, Depends
from app.models import Odd
from app.schemas import OddCreate
from app.auth import get_current_user

# Renomeei de outer para router
router = APIRouter(
    prefix="/odds",
    tags=["odds"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/")
def criar_odd(odd: OddCreate):
    return Odd.create(**odd.model_dump())

@router.get("/")
def listar_odds():
    return [o.__data__ for o in Odd.select()]

@router.get("/{id}")
def obter_odd(id: int):
    odd = Odd.get_or_none(Odd.id == id)
    if not odd:
        raise HTTPException(status_code=404, detail="Odd não encontrada")
    return odd.__data__

@router.put("/{id}")
def atualizar_odd(id: int, dados: OddCreate):
    odd = Odd.get_or_none(Odd.id == id)
    if not odd:
        raise HTTPException(status_code=404, detail="Odd não encontrada")
    odd.jogo = dados.jogo
    odd.casa_aposta = dados.casa_aposta
    odd.odd_1 = dados.odd_1
    odd.odd_x = dados.odd_x
    odd.odd_2 = dados.odd_2
    odd.data_hora = dados.data_hora
    odd.save()
    return odd.__data__

@router.delete("/{id}")
def deletar_odd(id: int):
    odd = Odd.get_or_none(Odd.id == id)
    if not odd:
        raise HTTPException(status_code=404, detail="Odd não encontrada")
    odd.delete_instance()
    return {"detail": "Odd deletada com sucesso"}
