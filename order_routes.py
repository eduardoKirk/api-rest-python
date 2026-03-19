from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter(prefix='/pedidos', tags=["pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def get_pedidos(): #essa é a rota padrao de pedidos
    return {"mensagem": "rota de pedidos"}

@order_router.post("/pedidos/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido realizade com sucesso, ID do pedido: {novo_pedido.id}"}

@order_router.post('/pedido/cancelar/id_pedido')
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao)):
    pedido_cancelado = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido_cancelado:
        raise HTTPException(status_code=400, detail="pedido nao encontrado")
    pedido_cancelado.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido {id_pedido} cancelado com sucesso",
        "pedido": pedido_cancelado
    }