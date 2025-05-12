from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from peewee import IntegrityError
from app.database import db
from app.models import Time, Liga, Jogo, Estatistica, Odd, Usuario
from app.routers import auth_routes, times, ligas, jogos, estatisticas, odds

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Conecta ao banco no startup
    db.connect()
    
    # Cria as tabelas se não existirem
    if not db.get_tables():
        db.create_tables([Time, Liga, Jogo, Estatistica, Odd, Usuario])
    
    # Tenta criar o usuário "admin" se ele não existir
    try:
        usuario, created = Usuario.get_or_create(username="admin", senha="12345")
        if created:
            print(f"Usuário {usuario.username} criado com sucesso!")
        else:
            print(f"Usuário {usuario.username} já existe.")
    except IntegrityError as e:
        print(f"Erro ao criar o usuário: {e}")

    yield
    
    # Fecha a conexão no shutdown
    if not db.is_closed():
        db.close()

app = FastAPI(lifespan=lifespan)

# Monta a pasta de arquivos estáticos (CSS, HTML customizado, etc)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rota para servir a documentação customizada
@app.get("/docs-custom", response_class=HTMLResponse)
async def custom_docs():
    with open("static/docs.html", encoding="utf-8") as f:
        return f.read()

# Inclui o router de autenticação (rota /login)
app.include_router(auth_routes.router)

# Inclui os routers das demais funcionalidades, todos protegidos via JWT
app.include_router(times.router)
app.include_router(ligas.router)
app.include_router(jogos.router)
app.include_router(estatisticas.router)
app.include_router(odds.router)
