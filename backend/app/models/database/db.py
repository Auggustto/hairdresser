from sqlalchemy import Integer, String, create_engine, Column, Date, ForeignKey, Time, Float, DateTime
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    lastname = Column(String(40), nullable=False)
    telephone = Column(String(13), nullable=False)
    birthdata = Column(Date, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    scheduling = relationship("Scheduling", back_populates="user")


class Hairdressers(Base):
    __tablename__ = "hairdressers"

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    email = Column(String, unique=True, nullable=False)
    email_acess = Column(String, unique=True, nullable=False)
    specialization = Column(String(70), nullable=False)
    start_working_hours = Column(Time, nullable=False)
    end_of_office = Column(Time, nullable=False)
    password = Column(String, nullable=False)
    
    scheduling = relationship("Scheduling", back_populates="hairdresser")


class Services(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    name_service = Column(String(30), unique=True, nullable=False)
    description = Column(String(90), nullable=False)
    price = Column(Float, nullable=False)
    duration = Column(Time, nullable=False)

    scheduling = relationship("Scheduling", back_populates="service")


class Scheduling(Base):
    __tablename__ = "scheduling"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("users.id"))
    hairdresser_id = Column(Integer, ForeignKey("hairdressers.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

    #  relationship
    user = relationship("User", back_populates="scheduling")
    hairdresser = relationship("Hairdressers", back_populates="scheduling")
    service = relationship("Services", back_populates="scheduling")


    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "telephone": self.telephone,
            "services": [service.as_dict() for service in self.services]
        }

# Crie as tabelas no banco de dados
Base.metadata.create_all(engine)

# # Crie uma sessão para interagir com o banco de dados
Session = sessionmaker(bind=engine)
session = Session()
