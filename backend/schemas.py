from pydantic import BaseModel

class TeacherLogin(BaseModel):
    name: str
    id_number: str

class TeacherCreate(BaseModel):
    name: str
    id_number: str

class StudentCreate(BaseModel):
    name: str
    phone: str
    class_name: str

# Same fields as create; kept separate so the two can evolve independently
class StudentUpdate(BaseModel):
    name: str
    phone: str
    class_name: str