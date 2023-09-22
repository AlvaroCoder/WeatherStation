from fastapi import FastAPI, APIRouter,status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from services.connectionHobolink import Connection
from routers import login

app=FastAPI(title="WeatherStation")

#routers
app.include_router(login.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

router=APIRouter(prefix="/home",
                tags=["Home page"],
                responses={status.HTTP_404_NOT_FOUND:{"message":"Page not found"}})

# Modificado por me!
template = Jinja2Templates(directory="templates")
@app.get("/", response_class=HTMLResponse)
async def root(request:Request):
    return template.TemplateResponse("index.html", {"request": request})

@app.get("/graficas")
async def root(request:Request):
    return template.TemplateResponse("graficas.html", {"request": request})

@app.get("/api_data")
async def root():
    conn = Connection()
    data = conn.dataSensors
    data['times'] = conn.timeStation
    return {"data":data}

""" @app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) 
"""