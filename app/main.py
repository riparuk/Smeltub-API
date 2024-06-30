from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from .routers import gas
from app.db import models
from app.db.database import engine
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# For web app
templates = Jinja2Templates(directory="app/templates")
# end For web app

app.include_router(gas.router)


@app.get("/")
async def root():
    return {"message": "Welcome Smeltub API"}

@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

