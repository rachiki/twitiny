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

## The next functions are for login
@app.post("/login")
def login(username: str = Form(""), password: str = Form(), db: Session = Depends(get_db)):
    user = db.query(data_models.User).filter(data_models.User.username == username).first()
    if user and user.password == password: 
        return RedirectResponse(url="/user_homepage", status_code=status.HTTP_302_FOUND)
    else:
        # Redirect to an error page if username not found or password is wrong
        return RedirectResponse(url="/login_fail", status_code=status.HTTP_302_FOUND)

@app.get("/login_fail")
def login_fail(request: Request): 
    return templates.TemplateResponse("login_fail.html", 
                                      {"request": request})

## The next functions are for the user homepage


## The next functions are for registration/user creation
@app.get("/register")
def register(request: Request, db: Session = Depends(get_db)): 
    return templates.TemplateResponse("register.html",                
                                      {"request": request})

MIN_USERNAME_LENGTH = 3
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
@app.post("/create_user")
def create_user(username: str = Form(""), password: str = Form(""), email: str = Form(""), db: Session = Depends(get_db)):
    error_message = validate_user_data(username, email, db)
    if error_message:
        return redirect_to_error(error_message)

    hashed_password = hash_password(password)  # NOTE: This is not implemented yet
    new_user = data_models.User(username=username, password=hashed_password, email=email)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/register_success", status_code=303)

def validate_user_data(username, email, db):
    if len(username) < MIN_USERNAME_LENGTH:
        return "Username too short."

    if not EMAIL_REGEX.match(email):
        return "Invalid E-Mail."

    if db.query(data_models.User).filter(data_models.User.username == username).first():
        return "Username already taken."

    if db.query(data_models.User).filter(data_models.User.email == email).first():
        return "E-Mail already registered."

    return None

def redirect_to_error(message):
    return RedirectResponse(url=f"/register_fail?error_message={quote(message)}", status_code=303)

def hash_password(password):
    return password # TODO: Implement hashing

@app.get("/register_success")
def login_fail(request: Request): 
    return templates.TemplateResponse("register_success.html", 
                                      {"request": request})

@app.get("/register_fail")
def register_fail(request: Request):
    error_message = request.query_params.get('error_message', '')
    return templates.TemplateResponse("register_fail.html",
                                      {"request": request, "error_message": error_message})