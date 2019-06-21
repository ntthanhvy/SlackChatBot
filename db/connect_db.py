from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# declare a base for database
Base = declarative_base()

# declare engine
engine = create_engine('\
postgres+psycopg2:///test_chema',  pool_use_lifo=True, pool_pre_ping=True)

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


class Escalate(Base):
    __tablename__ = "escalate"
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    reporter = Column(String)
    type = Column(String)

    def __repr__(self):
        return "Escalate<time=%s, reporter=%s, type=%s>" % (self.time, self.reporter, self.type)


class ContactInfo(Base):
    __tablename__ = 'contact_info'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    owner_name = Column(String, nullable=False)
    tel = Column(String, nullable=False)

    def __repr__(self):
        return "ContactInfo<name=%s, tel=%s, from=%s, to=%s>" % (self.owner_name, self.tel, self.start_time, self.end_time)


Base.metadata.create_all(engine)


