from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

#cria conexão com o banco
db = create_engine('sqlite:///banco.db')

#cria a base do banco de dados
Base = declarative_base()

