from fastapi import FastAPI 
""" , Request, templates """

app=FastAPI()

@app.get("/")
async def root():
    return {"message":"Welcome"}

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) 

