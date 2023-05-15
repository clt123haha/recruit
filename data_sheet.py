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

    def __repr__(self):
        ID = self.id
        TITLE = self.title
        PLACE = self.place
        MONEY = self.money
        IM1 = self.im1
        IM2 = self.im2
        return f"User: title: {TITLE},money:{MONEY},place: {PLACE},im1:{IM1},im2:{IM2},id:{ID}"

class User(Base):
    __tablename__ = "user"
    openid = Column(String(130),primary_key=True)
    collection = Column(String(255))

    def __repr__(self):
        OPENID = self.openid
        COLLECTION = self.collection
        return f"User: openid:{OPENID},collection:{COLLECTION}"


def get_sheet():
    Base.metadata.create_all(engine)  # 通过此语句创建表