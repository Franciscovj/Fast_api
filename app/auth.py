from datetime import datetime, timedelta
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import InvalidTokenError
from app.models import Usuario  # Importando o modelo Usuario
from peewee import DoesNotExist

# OAuth2 scheme para obter o token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Chave secreta e algoritmo para assinatura
SECRET_KEY = "QZAfzZICsRboAXXG-fk79dtaC1RdrVhN_zP7rStlEPc"  # Idealmente, deveria ser carregada de uma variável de ambiente
ALGORITHM = "HS256"

# Função para criar o token JWT
def criar_token(data: dict, expires_delta: timedelta = None):
    """
    Função para criar um token JWT com base nos dados fornecidos.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=30))  # Expiração padrão de 30 minutos
    to_encode.update({"exp": expire, "sub": data.get("sub")})
    
    # Gerando o token
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    print(f"🔑 Token gerado: {token}")  # Apenas para debug, pode remover depois
    
    return token

# Função para obter o usuário a partir do banco de dados
def get_user_by_username(username: str):
    try:
        user = Usuario.get(Usuario.username == username)  # Tentando buscar o usuário
        return user
    except DoesNotExist:
        return None  # Retorna None se o usuário não for encontrado

# Função para extrair e validar o token JWT
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Falha na autenticação",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        # Decodificando o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        
        # Se o campo "sub" não estiver presente no payload, lança uma exceção
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    
    # Aqui é onde obtemos o usuário com o nome de usuário
    user = get_user_by_username(username)  # Agora esta função busca corretamente no banco
    
    if user is None:
        raise credentials_exception
    
    return user
