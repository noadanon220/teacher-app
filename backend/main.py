# ---------- Imports ----------
import jwt
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
import models  # Must be imported, otherwise create_all won't know about the tables
import schemas
import auth

# ---------- Database setup ----------
Base.metadata.create_all(bind=engine)

def get_db():
    # Opens a new session for each request
    db = SessionLocal()
    try:
        yield db  # Hands the session to the route function
    finally:
        db.close()  # Always runs, even if the request failed

# ---------- App creation ----------
app = FastAPI()

# Allow the React dev server (Vite) to call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Authentication helper ----------
bearer_scheme = HTTPBearer()

def get_current_teacher(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    # Reads the token from the Authorization header and returns the logged-in teacher
    try:
        teacher_id = auth.decode_token(credentials.credentials)
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    teacher = db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()
    if not teacher:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return teacher

# ---------- Routes: authentication ----------
@app.post("/register")
def register(data: schemas.TeacherCreate, db: Session = Depends(get_db)):
    # Helper route for creating a teacher so login can be tested
    existing = db.query(models.Teacher).filter(
        models.Teacher.id_number == data.id_number
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Teacher with this ID number already exists")

    teacher = models.Teacher(name=data.name, id_number=data.id_number)
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return {"id": teacher.id, "name": teacher.name}

@app.post("/login")
def login(data: schemas.TeacherLogin, db: Session = Depends(get_db)):
    # Look for a teacher matching both name and ID number
    teacher = db.query(models.Teacher).filter(
        models.Teacher.name == data.name,
        models.Teacher.id_number == data.id_number
    ).first()

    # Same generic message for any failure, so we don't reveal which part was wrong
    if not teacher:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_token(teacher.id)
    return {"access_token": token, "token_type": "bearer"}

# ---------- Routes: students (require a logged-in teacher) ----------
def student_to_dict(student: models.Student):
    return {
        "id": student.id,
        "name": student.name,
        "phone": student.phone,
        "class_name": student.class_name,
    }

@app.get("/students")
def list_students(
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    # Only the students that belong to the logged-in teacher
    students = db.query(models.Student).filter(models.Student.teacher_id == teacher.id).all()
    return [student_to_dict(s) for s in students]

@app.post("/students")
def create_student(
    data: schemas.StudentCreate,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    # teacher_id comes from the token, never from the client
    student = models.Student(
        teacher_id=teacher.id,
        name=data.name,
        phone=data.phone,
        class_name=data.class_name,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student_to_dict(student)

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    data: schemas.StudentUpdate,
    teacher: models.Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    # Match both the student id and the teacher, so teachers can't edit each other's students
    student = db.query(models.Student).filter(
        models.Student.id == student_id,
        models.Student.teacher_id == teacher.id,
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    student.name = data.name
    student.phone = data.phone
    student.class_name = data.class_name
    db.commit()
    db.refresh(student)
    return student_to_dict(student)