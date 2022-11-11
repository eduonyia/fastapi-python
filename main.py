from fastapi import FastAPI, status, HTTPException, Cookie, Header
from typing import Optional
import uvicorn
from pydantic import BaseModel, Field
from enum import Enum
from fastapi.middleware.cors import CORSMiddleware


class Department(str, Enum):
    MATH = "math"
    ENGLISH = "english"
    CHEMISTRY = "chemistry"


class Employee(BaseModel):
    id: int = Field(description="The distinct ID that the employee uses to login everywhere.")
    department: Department = Field(description="The employee's department")
    age: int = Field(description="Employee's age")
    gender: str = Field(default=None, description="Employee's gender")


class NotificationType(BaseModel):
    email: str
    notification_type: int


origins = ["http://localhost:5000"]
app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=[""]

)


@app.get("/status/")
async def check_status():
    return "Hello World"


@app.get("/employees/{employee_id}")
async def get_employees(employee_id: int, department: Department, gender: str = None):
    print(employee_id)
    print(gender)
    print(department)
    return [
        {
            "id": 1,
            "name": "Edu"
        },
        {
            "id": 2,
            "name": "Abby"
        }
    ]


@app.post("/employee/", response_model=Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: Employee):
    if employee.id in [200, 300, 400]:
        raise HTTPException(status_code=500, detail="Server does not recognize your employee id")
    print(employee)
    return employee


@app.post("/send_email/")
async def send_email(
        notification_payload: NotificationType,
        token: Optional[str] = Cookie(None),
        user_agent: Optional[str] = Header(None)
):
    print(notification_payload)
    print(token)
    print(user_agent)
    return {
        "cookie_received": token,
        "user_agent_received": user_agent,
        "custom_message": "I parsed everything"

    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
