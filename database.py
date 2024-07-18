from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
import os

load_dotenv()  # Carregar variáveis de ambiente do arquivo .env

# Determinar o ambiente
ENVIRONMENT = os.getenv("ENVIRONMENT")

if ENVIRONMENT == "development":
    DATABASE_URL = os.getenv("DATABASE_URL_LOCAL")
elif ENVIRONMENT == "docker":
    DATABASE_URL = os.getenv("DATABASE_URL_DOCKER")
elif ENVIRONMENT == "production":
    DATABASE_URL = os.getenv("DATABASE_URL_PRODUCTION")
else:
    raise Exception("ENVIRONMENT variável não definida ou inválida!")

# Configuração do SQLAlchemy com base na URL do banco de dados
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Definição das tabelas
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    cpf = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    problems = relationship("Problem", back_populates="owner")


class Problem(Base):
    __tablename__ = "problems"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    tags = Column(String)
    description = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    state = Column(String)
    city = Column(String)
    zipcode = Column(String)
    street = Column(String)
    number = Column(String)
    reference = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="problems")


# Criação das tabelas
Base.metadata.create_all(bind=engine)


# Funções auxiliares
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_user(db, full_name, cpf, email, password):
    db_user = User(full_name=full_name, cpf=cpf, email=email, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db, email):
    return db.query(User).filter(User.email == email).first()


def create_problem(db, title, tags, description, latitude, longitude, state, city, zipcode, street, number, reference, owner_id):
    db_problem = Problem(
        title=title,
        tags=tags,
        description=description,
        latitude=latitude,
        longitude=longitude,
        state=state,
        city=city,
        zipcode=zipcode,
        street=street,
        number=number,
        reference=reference,
        owner_id=owner_id
    )
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem


def get_all_problems(db):
    return db.query(Problem).all()
