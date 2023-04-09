from fastapi import FastAPI
from routers import login


app=FastAPI()
app.include_router(router=login.router)
@app.get("/")
async def root():
    return {"message":"Welcome"}