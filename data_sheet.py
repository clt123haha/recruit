from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql+pymysql://root:root@localhost:3306/recruit", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

#表信息
class Jobmessage(Base):
    __tablename__ = "Jobmessage"
    id = Column(Integer,primary_key=True)
    title = Column(String(50))
    money = Column(String(50))
    place = Column(String(50))
    im1 =  Column(String(20))
    im2 = Column(String(20))
    publisher = Column(String(130))

    def __repr__(self):
        ID = self.id
        TITLE = self.title
        PLACE = self.place
        MONEY = self.money
        IM1 = self.im1
        IM2 = self.im2
        PUBLISHER = self.publisher
        return f"User: title: {TITLE},money:{MONEY},place: {PLACE},im1:{IM1},im2:{IM2},id:{ID},publisher:{PUBLISHER}"

class User(Base):
    __tablename__ = "user"
    id = Column(Integer,primary_key=True)
    collection = Column(String(255))
    email = Column(String(50))
    phone = Column(String(20))
    password = Column(String(50))

    def __repr__(self):
        ID = self.id
        COLLECTION = self.collection
        EMAIL = self.email
        PHONE = self.phone
        PASSWORD = self.password
        return f"User: id:{ID},collection:{COLLECTION},email:{EMAIL},phone:{PHONE},password:{PASSWORD}"

class ShortMessage(Base):
    __tablename__ = "shortMessage"
    id = Column(Integer, primary_key=True)
    phonenumber = Column(String(20))
    meaasge = Column(String(10))
    time = Column(String(30))

    def __repr__(self):
        ID = self.id
        PHONENUMBER = self.phonenumber
        MESSAGE = self.meaasge
        TIME = self.time
        return f"User: phonenumber: {PHONENUMBER},message:{MESSAGE},time:{TIME},id: {ID}"


def get_sheet():
    Base.metadata.create_all(engine)  # 通过此语句创建表