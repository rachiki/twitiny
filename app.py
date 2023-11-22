from fastapi import FastAPI, Depends, Request, Form, status

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
def index(request: Request, db: Session = Depends(get_db)): # auto error gets thrown if connection fails
    login = db.query(data_models.User).first()
    return templates.TemplateResponse("login.html", 
                                      {"request": request, "login": login})

@app.get("/")
def index(request: Request, db: Session = Depends(get_db)): # auto error gets thrown if connection fails
    login = db.query(data_models.User).first()
    return templates.TemplateResponse("login.html", 
                                      {"request": request, "login": login})