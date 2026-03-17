from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix='/auth', tags=["auth"])

def criar_token(id_usuario, duracao_token=timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiração = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": id_usuario, "exp": data_expiração}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITM)
    return jwt_codificado

def autenticar_usuario(email, senha, session: Session = Depends(pegar_sessao)): 
    usuario = session.query(Usuario).filter(Usuario.email==email).first()

    if not usuario: 
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    else: 
        return usuario

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
        return {"mensagem": f"usuario cadastrado com sucesso {novo_usuario.email}"}
    
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario: 
        raise HTTPException(status_code=400, detail="usuario nao existe ou credenciais invalidas")
    else: 
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }

@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario=Depends(verificar_token)):
    #verificar token
    access_token = criar_token(usuario.id)
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }