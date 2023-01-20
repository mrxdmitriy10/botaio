from models.user import USER
from models.sql import DATABASE
import func.short
from aiogram import types

async def add(user:USER, arg, short):
    if user.state == 0:
        DATABASE.addcity(arg)
        newmsg = f'Город добавлен --> {arg}'
        await short(newmsg, 1)

    if user.state == 1:
        
        DATABASE.addproduct(user.city, arg)
        newmsg = f'{user.city} добавлена категория ->  {arg}'
        await short(newmsg, 0)
