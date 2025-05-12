# app/routers/ligas.py
from fastapi import APIRouter, HTTPException, Depends
from app.models import Liga
from app.schemas import LigaCreate
from app.auth import get_current_user   # import do verificador de token

# Todas as rotas deste router exigirão token válido
router = APIRouter(
    prefix="/ligas",
    tags=["ligas"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/")
def criar_liga(liga: LigaCreate):
    return Liga.create(**liga.model_dump())

@router.get("/")
def listar_ligas():
    return [l.__data__ for l in Liga.select()]

@router.get("/{id}")
def obter_liga(id: int):
    liga = Liga.get_or_none(Liga.id == id)
    if not liga:
        raise HTTPException(status_code=404, detail="Liga não encontrada")
    return liga.__data__

@router.put("/{id}")
def atualizar_liga(id: int, dados: LigaCreate):
    liga = Liga.get_or_none(Liga.id == id)
    if not liga:
        raise HTTPException(status_code=404, detail="Liga não encontrada")
    liga.nome = dados.nome
    liga.pais = dados.pais
    liga.save()
    return liga.__data__

@router.delete("/{id}")
def deletar_liga(id: int):
    liga = Liga.get_or_none(Liga.id == id)
    if not liga:
        raise HTTPException(status_code=404, detail="Liga não encontrada")
    liga.delete_instance()
    return {"detail": "Liga deletada com sucesso"}
