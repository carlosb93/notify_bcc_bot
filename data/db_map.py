import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    arroba = Column(String(255))
    lang = Column(String(255))
    tgid = Column(Integer, nullable=True)
    phone = Column(String(255))
    rol = Column(String(255))
    status = Column(Integer, nullable=True)
    status_date = Column(Integer, nullable=True)
    
class Mensajes(Base):
    __tablename__ = 'mensajes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(255))
    phone = Column(String(255))
    text = Column(String(255))
    bank = Column(String(255))
    status = Column(Integer, nullable=True)
    created_at = Column(Integer, nullable=True) 
    
class Settings(Base):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    code = Column(String(255))
    setting_type = Column(String(255))
    # ---setting_type---
    # alert
    # basic
    # conf
    
class Settings4User(Base):
    __tablename__ = 'settings4user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    setting_id = Column(Integer, nullable=True) 
    user_id = Column(Integer, nullable=True) 
    