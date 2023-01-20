from models.user import USER
from models.sql import DATABASE

async def delcat(user:USER, arg):
    DATABASE.delcat(arg)
    user.setstate(1)
    user.setcat(0)