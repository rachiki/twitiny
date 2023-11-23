from fastapi import FastAPI, Depends, Request, Form, status, HTTPException

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session

import data_models
from database import SessionLocal, engine

from urllib.parse import quote
import re


data_models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def entry_point(request: Request, db: Session = Depends(get_db)): # auto error gets thrown if connection fails
    return templates.TemplateResponse("entry.html", 
                                      {"request": request})

@app.get("/register")
def register(request: Request, db: Session = Depends(get_db)): 
    return templates.TemplateResponse("register.html", 
                                      {"request": request})

@app.post("/create_user")
def create_user(username: str = Form(""), password: str = Form((""),), email: str = Form((""),),
                 db: Session = Depends(get_db)):
    new_user = data_models.User(username=username, password=password, email=email)

    MIN_USERNAME_LENGTH = 3
    # Check if the username is long enough
    if len(new_user.username) < MIN_USERNAME_LENGTH:
        error_message = "Username too short."
        return RedirectResponse(url=f"/register_fail?error_message={quote(error_message)}", status_code=303)
    
    # Validate the email
    email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    if not email_regex.match(new_user.email):
        error_message = "Invalid E-Mail."
        return RedirectResponse(url=f"/register_fail?error_message={quote(error_message)}", status_code=303)

    # Check if the username already exists
    existing_user = db.query(data_models.User).filter(data_models.User.username == new_user.username).first()
    if existing_user:
        error_message = "Username already taken."
        return RedirectResponse(url=f"/register_fail?error_message={quote(error_message)}", status_code=303)
    
    # Check if the email already exists
    existing_mail = db.query(data_models.User).filter(data_models.User.email == new_user.email).first()
    if existing_mail:
        error_message = "E-Mail already registered."
        return RedirectResponse(url=f"/register_fail?error_message={quote(error_message)}", status_code=303)

    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/register_success", status_code=303)

@app.get("/register_success")
def register_success(request: Request): 
    return templates.TemplateResponse("register_success.html", 
                                      {"request": request})

@app.get("/register_fail")
def register_fail(request: Request):
    error_message = request.query_params.get('error_message', '')
    return templates.TemplateResponse("register_fail.html",
                                      {"request": request, "error_message": error_message})