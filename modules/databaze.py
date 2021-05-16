from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


SQLITE = 'sqlite'
MYSQL = 'mysql'

Base = declarative_base()


class Game(Base):
    __tablename__ = 'games'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    review = Column(Integer)
    developer_name = Column(String(50), ForeignKey('companys.name'))
    platform_name = Column(String(50), ForeignKey('platforms.name'))


class Company(Base):
    __tablename__ = 'companys'

    name = Column(String(50), primary_key=True)
    employees = Column(Integer)
    place = Column(String(50))
    games = relationship('Game', backref='developer')


class Platform(Base):
    __tablename__ = 'platforms'

    name = Column(String(50), primary_key=True)
    games = relationship('Game', backref='platform')


class Db:
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}',
        MYSQL: 'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@localhost/{DB}'
    }

    def __init__(self, dbtype='sqlite', username='', password='', dbname='games'):
        dbtype = dbtype.lower()

        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname, USERNAME=username, PASSWORD=password)
            self.engine = create_engine(engine_url, echo=False)
        else:
            print('DBType is not found in DB_ENGINE')

        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def read_all(self, order=Game.name):
        result = self.session.query(Game).order_by(order).all()
        return result

    def read_by_id(self, id):
        try:
            result = self.session.query(Game).get(id)
            return result
        except:
            return False

    def read_by_platform(self, platform='PS4'):
        try:
            result = self.session.query(Game).join(Platform).filter(Platform.name.like(f'%{platform}%')).order_by(Game.name).all()
            return result
        except:
            return False

    def read_platforms(self):
        try:
            result = self.session.query(Platform).all()
            return result
        except:
            return False

    def create(self, game):
        try:
            self.session.add(game)
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

    def delete(self, id):
        try:
            game = self.read_by_id(id)
            self.session.delete(game)
            self.session.commit()
            return True
        except:
            return False

    def create_platform(self, platform):
        try:
            self.session.add(platform)
            self.session.commit()
            return True
        except:
            return False
