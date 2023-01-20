import func.create
import func.short
from aiogram import types
from models.user import USER


async def user(user: USER, arg, short):
    arg = str(arg).split()
    if len(arg)>0:
        newmsg = '=)'
        if arg[0].isnumeric():
            newuser = USER(arg[0])
            newmsg = str(newuser.userdata())
        if 'self' in arg[0]:
            newmsg = str(user.userdata())
        await short(newmsg)
