from sqlalchemy import Integer, String, Column, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

SQLITE = 'sqlite'
MYSQL = 'mysql'

Base = declarative_base()


class Game(Base):
    __tablename__ = 'game'

    jmeno = Column(String(50), primary_key=True)
    hodnoceni = Column(Integer)
    vyvojar = relationship('Company', backref='Game')
    platforma = relationship('Platforma', backref='Game')


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    jmeno = Column(String(50), ForeignKey('jmeno'))
    pocetZamestnancu = Column(Integer)
    sidlo = Column(String(50))


class Platforma(Base):
    __tablename__ = 'platforma'

    id = Column(Integer, primary_key=True)
    jmeno = Column(String(50), ForeignKey('jmeno'))


class Start:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        MYSQL: 'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost/{DB}'
    }

    def __init__(self, dbtype='sqlite', username='', password='', dbname='persons'):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname, USERNAME=username, PASSWORD=password)
            self.engine = create_engine(engine_url, echo=True)
        else:
            print('Error! DBtype not found')

        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


db = Start()
