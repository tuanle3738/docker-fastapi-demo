import uvicorn
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel, field_validator

app = FastAPI()

students = {
    1: {
        "name": "John",
        "age": 17,
        "class": "year 12"
    }
}


class Student(BaseModel):
    name: str
    age: int
    year: str


    @field_validator("age")
    @classmethod
    def validate_age(cls, age_value):
        if age_value <= 21:
            raise ValueError('age must be larger than 21')
        return age_value


# Optional vi cai para nao ko co thi giu nguyen ban dau
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None

    @field_validator("age")
    @classmethod
    def validate_age(cls, age_value):
        if age_value <= 21:
            raise ValueError('age must be larger than 21')
        return age_value

@app.get("/")
def index():
    return {"name": "First Data"}


@app.get("/get-student/{student_id}")
def get_student(student_id: int):
    return students[student_id]


@app.get("/get-by-name/{student_id}")
def get_student(*, student_id: int, name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]
    return {"Data": "Not found"}


@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "Student exists"}

    students[student_id] = dict(student)
    return students[student_id]


@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}

    if student.name is not None:
        students[student_id]["name"] = student.name
    if student.age is not None:
        students[student_id]["age"] = student.age
    if student.year is not None:
        students[student_id]["year"] = student.year

    return students[student_id]


@app.delete("/delete-student/{student_id}")
def delete_student(student_id: int):
    if student_id not in students:
        return {"Error": "Student does not exist"}

    del students[student_id]
    return {"Message": "Student deleted successfully"}


@app.get("/get-odd-id")
def get_odd_id():
    for student_id in students:
        if student_id % 2 > 0:
            return students[student_id]

    return {"Error": "None"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)