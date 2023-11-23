from fastapi import FastAPI, Depends, Request, Form, status, HTTPException

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session

import data_models
from database import SessionLocal, engine

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
def create_user(username: str = Form(...), password: str = Form(...), email: str = Form(...),
                 db: Session = Depends(get_db)):
    new_user = data_models.User(username=username, password=password, email=email)

    # Check if the username already exists
    existing_user = db.query(data_models.User).filter(data_models.User.username == new_user.username).first()
    if existing_user:
        return RedirectResponse(url="/register_success")
        #raise HTTPException(status_code=400, detail="Username already taken")
    
    # Check if the email already exists
    existing_mail = db.query(data_models.User).filter(data_models.User.email == new_user.email).first()
    if existing_mail:
        return RedirectResponse(url="/register_success")
        #raise HTTPException(status_code=400, detail="E-Mail already registered")

    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/register_success", status_code=303)

@app.get("/register_success")
def register_success(request: Request, db: Session = Depends(get_db)): 
    return templates.TemplateResponse("register_success.html", 
                                      {"request": request})

@app.get("/register_fail")
def register_fail(error: str, request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("register_fail.html",
                                      {"request": request, "error": error})