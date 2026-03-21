from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel): 
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Conifg:
        from_attributes = True


class PedidoSchema(BaseModel): 
    usuario: int 

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email:str 
    senha:str

    class Config:
        from_attributes = True

class Item_pedido_schema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float
    
    class Config:
        from_attributes = True