from pydantic import BaseModel
from typing import Optional

class Person(BaseModel):
    name:str
    age:int
    city:str
person = Person(name="Kritika",age=21,city="Jaipur")
print(person)
class Employee(BaseModel):
    id : int 
    name : str
    department : str
    salary : Optional[float] = None
    is_active : Optional[bool] = True
emp1=Employee(id=1,name="John",department="IT")
print(emp1)
class Classroom(BaseModel):
    room_number:str
    students:list[str]
    capacity:int
classroom = Classroom(
    room_number="A101",
    students=('Kritika','Sarita','Kamala'),
    capacity=30
)
print(classroom)
try:
    invalid_val = Classroom(
        room_number = "A1",
        students = ("Krish",123),
        capacity = 30
    )
except ValueError as e:
    print(e)