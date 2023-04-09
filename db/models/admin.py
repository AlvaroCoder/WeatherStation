from pydantic import BaseModel,NonNegativeInt

class Admin(BaseModel):
    id:str|None=None
    username:str
    fullname:str
    age:NonNegativeInt
    disable:bool
    email:str


class Admin_db(Admin):
    password:str