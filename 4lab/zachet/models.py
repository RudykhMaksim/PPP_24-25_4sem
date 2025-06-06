from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel, Field
from typing import List

Base = declarative_base()

# Модели SQLAlchemy
class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    courses = relationship("Course", back_populates="teacher", cascade="all, delete-orphan")

class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    student_count = Column(Integer, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    teacher = relationship("Teacher", back_populates="courses")

# Модели Pydantic
class TeacherCreate(BaseModel):
    name: str

class TeacherResponse(BaseModel):
    id: int
    name: str

class CourseCreate(BaseModel):
    name: str
    student_count: int = Field(..., ge=0)
    teacher_id: int

class CourseResponse(BaseModel):
    id: int
    name: str
    student_count: int
    teacher_id: int