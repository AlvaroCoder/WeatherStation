from fastapi import FastAPI
from routers import login
""" , Request, templates """

app=FastAPI()
app.include_router(router=login.router)
@app.get("/")
async def root():
    return {"message":"Welcome"}

""" @app.get("/")
async def login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) """

