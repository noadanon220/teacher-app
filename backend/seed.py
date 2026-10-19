# Adds a sample teacher with five students, so you can log in and see data right away.
# Run from the backend folder: python seed.py  (safe to run more than once)
from database import Base, engine, SessionLocal
import models

TEACHER = {"name": "Dana Cohen", "id_number": "318452769"}

STUDENTS = [
    {"name": "רעות כהן", "class_name": "ה׳5", "phone": "0524817365"},
    {"name": "שירה לוי", "class_name": "ה׳5", "phone": "0546093128"},
    {"name": "עומר רז", "class_name": "ה׳3", "phone": "0587241950"},
    {"name": "נועה דנון", "class_name": "ד׳2", "phone": "0503658472"},
    {"name": "איתי רז", "class_name": "ד׳5", "phone": "0539175604"},
]

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Find the teacher by ID number, or create it if it doesn't exist yet
teacher = db.query(models.Teacher).filter(
    models.Teacher.id_number == TEACHER["id_number"]
).first()
if not teacher:
    teacher = models.Teacher(**TEACHER)
    db.add(teacher)
    db.commit()
    db.refresh(teacher)  # Loads the new teacher.id from the database

# Add only students that this teacher doesn't already have (avoids duplicates)
existing_names = {
    s.name for s in db.query(models.Student).filter(models.Student.teacher_id == teacher.id)
}
for data in STUDENTS:
    if data["name"] not in existing_names:
        db.add(models.Student(teacher_id=teacher.id, **data))
db.commit()

print(f"Teacher: {teacher.name} / {teacher.id_number}")
db.close()
