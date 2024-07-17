from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Configuração do SQLAlchemy
DATABASE_URL = "sqlite:///data.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Definição das tabelas
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    problems = relationship("Problem", back_populates="owner")


class Problem(Base):
    __tablename__ = "problems"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
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


def create_user(db, username, password):
    db_user = User(username=username, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db, username):
    return db.query(User).filter(User.username == username).first()


def create_problem(db, name, description, latitude, longitude, owner_id):
    db_problem = Problem(name=name, description=description, latitude=latitude, longitude=longitude, owner_id=owner_id)
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)
    return db_problem


def get_problems(db, owner_id):
    return db.query(Problem).filter(Problem.owner_id == owner_id).all()
