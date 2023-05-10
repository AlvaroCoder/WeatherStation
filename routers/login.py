from fastapi import APIRouter,status,Request,Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from datetime import datetime, timedelta


from db.client import db_client
from db.schemes.admin import admin_db_schema,admin_schema
from db.models.admin import Admin,Admin_db
from db.models.token_jwt import Token
#para tratar con el password con hash
from passlib.context import CryptContext

#jwt tokens
from jose import JWTError,jwt


#instancias

#jwt

ALGORITHM='HS256'
SECRET_KEY='86e03f05493b492caae0702193686d848e0a6fd2f883b48810b866222627d490' #openssl rand -hex 32
ACCESS_TOKEN_EXPIRES_MINUTES=30 #luego lo cambiamos

#para el hash a las contrasenas
crypt=CryptContext(schemes=["bcrypt"])

#ruta donde se va a verificar al usuario
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")

router=APIRouter(prefix="/login",
                 tags=["Login page"],
                 responses={status.HTTP_404_NOT_FOUND:{"message":"Page not found"}})


def search_admin(field:str,key) -> Admin:
    try:
        admin=db_client.local.admin.find_one({field:key})
        return Admin(**admin_schema(admin))
    except:
        return {"message":"Admin not found"}

def search_admin_db(field:str,key) ->Admin_db:
    try:
        adminDB=db_client.local.admin_db.find_one({field:key})
        return Admin_db(**admin_db_schema(adminDB))
    except:
        return {"message":"Admin not found"}

def password_hashing(password):
    return crypt.hash(password)

def password_verify(password,password_db):
    return crypt.verify(password,password_db)

def create_access_token(data:dict,expires_delta:timedelta|None=None):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.utcnow()+expires_delta
    else:
        expire=datetime.utcnow()+timedelta(15) #luego se modifica
    to_encode.update({'exp':expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt 


@router.get("/")
async def root():
    return {"message":"Login page"}

@router.post("/login")
async def login_for_access_token(form:OAuth2PasswordRequestForm=Depends()):
    Admin=search_admin_db("username",form.username)
    if (type(Admin)!=Admin_db):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Admin not found",headers={'WWW-Authenticate':'Bearer'})
    #verificar contra
    if not (password_verify(password=form.password,password_db=Admin.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Wrong password',headers={'WWW-Authenticate':'Bearer'})
    access_token_expires=timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    data={
        'sub':Admin.username
    }
    access_token=create_access_token(data,access_token_expires)
    return {'access_token':access_token,'token_type':'bearer'}
    #return template, a=10


#a la ruta se le debe enviar el token
@router.post("/futuro")
async def futuro(token=Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                        detail='Could not validate credentials',
                                        headers={'WWW-Authenticate':'Bearer'})
    print("Prueba")
    try:
        payload=jwt.decode(token=token,key=SECRET_KEY,algorithms=[ALGORITHM])
        username=payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {'message':'Acceso concedido'}


#JWT -info-codificacion-firma

# credenciales de usuario: Autentificar y autorizar

#token