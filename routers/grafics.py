from fastapi import APIRouter,status,Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


router=APIRouter(prefix="/graficas",tags=["Graphics page"],
                 responses={status.HTTP_404_NOT_FOUND:{"message":"Page not found"}})

template=Jinja2Templates("templates")
router.mount("/templates",StaticFiles(directory="static"),name="static")


@router.get("/",response_class=HTMLResponse)
async def root(request:Request):
    response={'request':request}
    return template.TemplateResponse("graficas.html",response)
