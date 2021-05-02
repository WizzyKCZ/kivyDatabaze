from sqlalchemy import Integer, String, Column, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

SQLITE = 'sqlite'
MYSQL = 'mysql'

Base = declarative_base()


class Game(Base):
    __tablename__ = 'game'

    jmeno = Column(String(50), primary_key=True)
    hodnoceni = Column(Integer)
    vyvojar = Column(String(50))
    platforma = Column(String(50))


class Company(Base):
    jmeno = Column(String(50), primary_key=True)
    pocetZamestnancu = Column(Integer)
    sidlo = Column(String(50))


class Platforma(Base):
    jmeno = Column(String(50), primary_key=True)