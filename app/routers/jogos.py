from fastapi import APIRouter, HTTPException, Depends
from app.models import Jogo
from app.schemas import JogoCreate
from app.auth import get_current_user  # import do verificador de token

# Aplica autenticação em todas as rotas deste router
router = APIRouter(
    prefix="/jogos",
    tags=["jogos"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/")
def criar_jogo(jogo: JogoCreate):
    return Jogo.create(**jogo.model_dump())

@router.get("/")
def listar_jogos():
    return [j.__data__ for j in Jogo.select()]

@router.get("/{id}")
def obter_jogo(id: int):
    jogo = Jogo.get_or_none(Jogo.id == id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return jogo.__data__

@router.put("/{id}")
def atualizar_jogo(id: int, dados: JogoCreate):
    jogo = Jogo.get_or_none(Jogo.id == id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    jogo.data = dados.data
    jogo.time_casa = dados.time_casa
    jogo.time_fora = dados.time_fora
    jogo.liga = dados.liga
    jogo.status = dados.status
    jogo.save()
    return jogo.__data__

@router.delete("/{id}")
def deletar_jogo(id: int):
    jogo = Jogo.get_or_none(Jogo.id == id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    jogo.delete_instance()
    return {"detail": "Jogo deletado com sucesso"}
