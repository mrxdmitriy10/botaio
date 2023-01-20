from models.user import USER
from models.sql import SQL
import func.short
import func.create
from config import USERLEVEL
from aiogram import types
import logging


async def level(user: USER, arg, short):
    arg = str(arg).split()
    if len(arg) == 2 and arg[1] in USERLEVEL.keys():
        level = USERLEVEL[f'{arg[1]}']
        if 'self' in arg[0]:
                userid = user.id
                user.setlevel(level)
                newmsg = f'Уровень себе -> {level}'
                await short(newmsg, timer = 1)

        elif arg[0].isnumeric():
            userid = int(arg[0])
            try:
                anyuser = func.create.newuser(userid, database)
                anyuser.setlevel(level)
                anyuser.upload()
                newmsg = f'Уровень {userid} -> {level}'
                await short(newmsg, timer = 1)
                del anyuser
            except:
                logging.warning('setlevel not work')
