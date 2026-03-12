from fastapi import APIRouter, Depends
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context

auth_router = APIRouter(prefix='/auth', tags=["auth"])

@auth_router.get("/")
async def home(): #rota padrao de autenticação do sistema
    return {"mensagem": "rota de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(email: str, senha: str, nome: str, session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    
    if usuario:
        return {"mensagem": "ja existe um usuario com esse email"}
    else:
        senha_crypto= bcrypt_context.hash(senha)
        novo_usuario = Usuario(nome, email, senha_crypto)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "usuario cadastrado com sucesso"}