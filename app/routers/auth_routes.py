from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.models import Usuario
from app.auth import criar_token  # A função criar_token é a que você já tem

router = APIRouter()

# Modelo de dados para login
class Login(BaseModel):
    username: str
    senha: str

# Rota de login
@router.post("/login")
async def login(credentials: Login):
    # Tenta encontrar o usuário pelo username
    user = Usuario.get_or_none(Usuario.username == credentials.username)
    
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    # Verifica se a senha fornecida é correta
    if user.senha != credentials.senha:
        raise HTTPException(status_code=400, detail="Senha incorreta")
    
    # Cria um token JWT com as informações do usuário
    token = criar_token({"sub": user.username})
    
    return {"access_token": token, "token_type": "bearer"}

