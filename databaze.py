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
    jmeno = Column(String(50), ForeignKey('game'))
    pocetZamestnancu = Column(Integer)
    sidlo = Column(String(50))


class Platforma(Base):
    __tablename__ = 'platforma'

    id = Column(Integer, primary_key=True)
    jmeno = Column(String(50), ForeignKey('game'))


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

        def read_all_game(self, order=Game.jmeno):
            try:
                result = self.session.query(Game).all()
                return result
            except:
                return False

        def read_all_company(self, order=Company.jmeno):
            try:
                result = self.session.query(Company).all()
                return result
            except:
                return False

        def read_all_platforma(self, order=Platforma.jmeno):
            try:
                result = self.session.query(Platforma).all()
                return result
            except:
                return False

        def read_by_game_jmeno(self, jmeno):
            try:
                result = self.session.query(Game).get(jmeno)
                return result
            except:
                return False

        def read_by_game_hodnoceni(self, hodnoceni):
            try:
                result = self.session.query(Game).get(hodnoceni)
                return result
            except:
                return False

        def read_by_game_vyvojar(self, vyvojar):
            try:
                result = self.session.query(Game).get(vyvojar)
                return result
            except:
                return False

        def read_by_game_platforma(self, platforma):
            try:
                result = self.session.query(Game).get(platforma)
                return result
            except:
                return False

        def read_by_company_id(self, id):
            try:
                result = self.session.query(Company).get(id)
                return result
            except:
                return False

        def read_by_company_jmeno(self, jmeno):
            try:
                result = self.session.query(Company).get(jmeno)
                return result
            except:
                return False

        def read_by_company_pocetZamestnancu(self, pocetZamestnancu):
            try:
                result = self.session.query(Company).get(pocetZamestnancu)
                return result
            except:
                return False

        def read_by_company_sidlo(self, sidlo):
            try:
                result = self.session.query(Company).get(sidlo)
                return result
            except:
                return False

        def read_by_platforma_id(self, id):
            try:
                result = self.session.query(Platforma).get(id)
                return result
            except:
                return False

        def read_by_platforma_jmeno(self, jmeno):
            try:
                result = self.session.query(Platforma).get(jmeno)
                return result
            except:
                return False

        def create_game(self, Game):
            try:
                self.session.add(Game)
                self.session.commit()
                return True
            except:
                return False

        def create_company(self, Company):
            try:
                self.session.add(Company)
                self.session.commit()
                return True
            except:
                return False

        def create_platforma(self, Platforma):
            try:
                self.session.add(Platforma)
                self.session.commit()
                return True
            except:
                return False

        def update(self):
            try:
                self.session.commit()
                return True
            except:
                return False

        def delete(self, name):
            try:
                game = self.read_by_game_jmeno(name)
                self.session.delete(game)
                self.session.commit()
                return True
            except:
                return False


db = Start(dbtype='sqlite', dbname='persons.db')
