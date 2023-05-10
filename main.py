from fastapi import FastAPI,status, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from routers import login,grafics

app=FastAPI()

#routers
app.include_router(login.router)
app.include_router(grafics.router)
template=Jinja2Templates("templates")
app.mount("/templates",StaticFiles(directory="static"),name="static")

@app.get("/",response_class=HTMLResponse)
async def root(request:Request):
    response={"request":request}
    return template.TemplateResponse("index.html",response)

