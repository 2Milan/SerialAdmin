from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqladmin import ModelView

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)


class Key(Base):
    __tablename__ = "key"

    id = Column(Integer, primary_key=True)
    hwid = Column(String)
    key = Column(String)
    ip = Column(String)
    experiance_time = Column(String)


class Log(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True)
    auth = Column(String)


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.password]


class UserKeys(ModelView, model=Key):
    column_list = [Key.id, Key.hwid, Key.key, Key.ip, Key.experiance_time]


class LogView(ModelView, model=Log):
    column_list = [Log.id, Log.auth]
