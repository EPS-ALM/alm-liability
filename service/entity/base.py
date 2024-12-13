from sqlalchemy import Column, Integer, Float, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

# Configuração da base e do banco de dados
Base = declarative_base()

class SelicData(Base):
    __tablename__ = "selic_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, unique=True, nullable=False)
    valor = Column(Float, nullable=False)

# Configuração da engine e da sessão do banco de dados
def get_engine():
    # Altere 'postgresql://user:password@localhost/dbname' para sua conexão
    return create_engine(config("DATABASE_URL"))

def get_session():
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    return Session()

if __name__ == "__main__":
    # Criação das tabelas no banco
    engine = get_engine()
    Base.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")
