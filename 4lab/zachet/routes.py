from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session as SQLAlchemySession
from typing import List
from database import get_db
from models import Teacher, Course, TeacherCreate, TeacherResponse, CourseCreate, CourseResponse

router = APIRouter()

# Инициализация таблиц в базе данных
from database import engine
from models import Base
Base.metadata.create_all(bind=engine)

# Эндпоинты для преподавателей
@router.get("/teachers", response_model=List[TeacherResponse])
def get_teachers(db: SQLAlchemySession = Depends(get_db)):
    teachers = db.query(Teacher).all()
    return [{"id": t.id, "name": t.name} for t in teachers]

@router.post("/teachers", response_model=TeacherResponse, status_code=201)
def create_teacher(teacher: TeacherCreate, db: SQLAlchemySession = Depends(get_db)):
    db_teacher = Teacher(name=teacher.name)
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return {"id": db_teacher.id, "name": db_teacher.name}

@router.delete("/teachers/{id}", status_code=204)
def delete_teacher(id: int, db: SQLAlchemySession = Depends(get_db)):
    db_teacher = db.query(Teacher).filter(Teacher.id == id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db.delete(db_teacher)
    db.commit()
    return {"detail": "Teacher deleted"}

# Эндпоинты для курсов
@router.get("/courses", response_model=List[CourseResponse])
def get_courses(db: SQLAlchemySession = Depends(get_db)):
    courses = db.query(Course).all()
    return [{"id": c.id, "name": c.name, "student_count": c.student_count, "teacher_id": c.teacher_id} for c in courses]

@router.post("/courses", response_model=CourseResponse, status_code=201)
def create_course(course: CourseCreate, db: SQLAlchemySession = Depends(get_db)):
    db_teacher = db.query(Teacher).filter(Teacher.id == course.teacher_id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    db_course = Course(name=course.name, student_count=course.student_count, teacher_id=course.teacher_id)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return {"id": db_course.id, "name": db_course.name, "student_count": db_course.student_count, "teacher_id": db_course.teacher_id}

@router.delete("/courses/{id}", status_code=204)
def delete_course(id: int, db: SQLAlchemySession = Depends(get_db)):
    db_course = db.query(Course).filter(Course.id == id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(db_course)
    db.commit()
    return {"detail": "Course deleted"}

@router.get("/teachers/{id}/courses", response_model=List[CourseResponse])
def get_teacher_courses(id: int, db: SQLAlchemySession = Depends(get_db)):
    db_teacher = db.query(Teacher).filter(Teacher.id == id).first()
    if not db_teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    courses = db.query(Course).filter(Course.teacher_id == id).all()
    return [{"id": c.id, "name": c.name, "student_count": c.student_count, "teacher_id": c.teacher_id} for c in courses]