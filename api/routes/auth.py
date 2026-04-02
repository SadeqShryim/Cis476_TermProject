from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any
from services import auth_service
from patterns.singleton import SessionManager

router = APIRouter()

class SecurityQuestionModel(BaseModel):
    question: str
    answer: str

class RegisterModel(BaseModel):
    email: str
    password: str
    security_questions: List[SecurityQuestionModel]

class LoginModel(BaseModel):
    email: str
    password: str

class RecoverPasswordModel(BaseModel):
    email: str
    answers: List[str]
    new_password: str

@router.post("/register")
def register(data: RegisterModel):
    sqs = [{"question": q.question, "answer": q.answer} for q in data.security_questions]
    res = auth_service.register(data.email, data.password, sqs)
    if not res.get("success"):
        raise HTTPException(status_code=400, detail=res.get("message", "User with that email already exists."))
    user = res["user"]
    return {"message": "Registration successful", "user": {"id": user["id"], "email": user["email"]}}

@router.post("/login")
def login(data: LoginModel):
    res = auth_service.login(data.email, data.password)
    if not res.get("success"):
        raise HTTPException(status_code=401, detail=res.get("message", "Invalid email or password."))
    user = res["user"]
    # Use user ID as simple auth token for demo purposes
    return {"message": "Login successful", "user": {"id": user["id"], "email": user["email"]}, "token": user["id"]}

@router.get("/security-questions/{email}")
def get_security_questions(email: str):
    qs = auth_service.get_security_questions(email)
    if not qs:
        raise HTTPException(status_code=404, detail="User not found or no questions configured.")
    return {"questions": qs}

@router.post("/recover-password")
def recover_password(data: RecoverPasswordModel):
    success = auth_service.recover_password(data.email, data.answers, data.new_password)
    if success:
        return {"message": "Password updated successfully."}
    raise HTTPException(status_code=400, detail="Password recovery failed. Incorrect answers.")

@router.post("/logout")
def logout():
    auth_service.logout()
    return {"message": "Logged out successfully"}
