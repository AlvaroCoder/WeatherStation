from fastapi import FastAPI 
""" , Request, templates """

app=FastAPI()

@app.get("/")
async def root():
    return {"message":"Welcome"}

""" @app.get("/")
async def login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request}) """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)