from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class Teacher(Base):
    __tablename__  = "teachers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    id_number = Column(String, nullable=False, unique=True)

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"),nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    class_name = Column(String, nullable=False)

