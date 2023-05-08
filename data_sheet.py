from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine("mysql+pymysql://root:yueye13084030!@gz-cynosdbmysql-grp-ro694ctz.sql.tencentcdb.com:28492/exchange", echo=True)
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
        return f"User: title: {TITLE},money:{MONEY},place: {PLACE},im1:{IM2},im2:{IM2},id:{ID}"


def get_sheet():
    Base.metadata.create_all(engine)  # 通过此语句创建表