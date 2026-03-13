from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix='/auth', tags=["auth"])

@auth_router.get("/")
async def home(): #rota padrao de autenticação do sistema
    return {"mensagem": "rota de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schemas: UsuarioSchema,  session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schemas.email).first()
    
    if usuario:
        raise HTTPException(status_code=400, detail="Usuario ja cadastrado")
    else:
        senha_crypto= bcrypt_context.hash(usuario_schemas.senha)
        novo_usuario = Usuario(usuario_schemas.nome, usuario_schemas.email, senha_crypto, usuario_schemas.ativo, usuario_schemas.admin)
        session.add(novo_usuario)
        session.commit()
        return {f"mensagem": "usuario cadastrado com sucesso {novo_usuario.email}"}