from fastapi import FastAPI, APIRouter,status
from routers import login

app=FastAPI()

#routers
app.include_router(login.router)

router=APIRouter(prefix="/home",
                tags=["Home page"],
                responses={status.HTTP_404_NOT_FOUND:{"message":"Page not found"}})

@app.get("/")
async def root():
    return {"message":"Welcome"}


""" @app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) 
"""
