from sqlalchemy import Column, Integer, String

from app.database import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, default="Aluno")
    xp = Column(Integer, default=0)
    nivel = Column(Integer, default=1)
