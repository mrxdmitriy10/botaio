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
                await short(newmsg, 1)

        