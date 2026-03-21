from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, Item_pedido_schema
from models import Pedido, Usuario, ItemPedido

order_router = APIRouter(prefix='/pedidos', tags=["pedidos"], dependencies=[Depends(verificar_token)])

@order_router.get("/")
async def get_pedidos(): #essa é a rota padrao de pedidos
    return {"mensagem": "rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido realizade com sucesso, ID do pedido: {novo_pedido.id}"}

@order_router.post('/pedido/cancelar/id_pedido')
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario=Depends(verificar_token)): 
    pedido_cancelado = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido_cancelado:
        raise HTTPException(status_code=400, detail="pedido nao encontrado")
    if not usuario.admin or usuario.id != pedido_cancelado.usuario:
        raise HTTPException(status_code=401, detail="voce nao tem autorizacao")
    pedido_cancelado.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido {id_pedido} cancelado com sucesso",
        "pedido": pedido_cancelado
    }

@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario=Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=400, detail="pedido nao encontrado")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
        }
    
@order_router.post('/pedido/adicionar_item/{id_pedido}')
async def adicionar_item_pedido(id_pedido: int, item_pedido_schema: Item_pedido_schema,
                                session: Session = Depends(pegar_sessao),
                                usuario: Usuario=Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="pedido nao encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="voce nao tem autorizacao")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, 
                             item_pedido_schema.tamanho, 
                             item_pedido_schema.preco_unitario, id_pedido)