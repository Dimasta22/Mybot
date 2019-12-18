from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

db_string = "postgres://postgres:1111@localhost/productsbot"
db = create_engine(db_string)  
base = declarative_base()


class User(base):  
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String)


class Products(base):  
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    discription = Column(String)

    
Session = sessionmaker(db)  
session = Session()
base.metadata.create_all(db)
