from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_utils import database_exists, create_database


# declare a base for database
Base = declarative_base()

# declare engine
engine = create_engine('\
postgres+psycopg2:///test_chema', echo=True)
if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(bind=engine)


class Server(Base):
    __tablename__ = 'server'
    name = Column(String, primary_key=True)
    enabled = Column(Boolean)
    info = relationship("ServerInfo", back_populates="server")
    owners = relationship("ServerOwner", back_populates="servers")

    def __repr__(self):
        return 'Server<name=%s, enabled=%s>' % (self.name, self.enabled)


class ServerInfo(Base):
    __tablename__ = "server_info"
    server_name = Column(String, ForeignKey('server.name'), primary_key=True)
    ram = Column(Integer)
    cpu = Column(Integer)
    server = relationship("Server", back_populates="info")

    def __repr__(self):
        return "ServerInfo<server_name=%s, ram=%d, cpu=%d>" % (self.server_name, self.ram, self.cpu)


class ServerOwner(Base):
    __tablename__ = "server_owner"
    id = Column(Integer, primary_key=True)
    server_name = Column(String, ForeignKey('server.name'))
    owner_name = Column(String)
    servers = relationship("Server", back_populates="owners")

    def __repr__(self):
        return "ServerOwner<server_name=%s, owner_name=%s>" %(self.server_name, self.owner_name)

Base.metadata.create_all(engine)


