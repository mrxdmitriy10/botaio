from models.sql import DATABASE
from models.user import USER

async def delcity(user:USER,  arg):
    DATABASE.delcity(arg)
    user.setstate(0)
    user.setcity(0)
    user.setcat(0)