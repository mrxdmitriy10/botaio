from models.user import USER

from models.sql import SQL
from models.keyboards import KEYBOARDS
from models.sql import DATABASE


import func.short
from aiogram import types
import func.create

async def item(user:USER, cmd, msg:types.Message):
    cmd = str(cmd).split('_')
    if len(cmd)>0:
        if cmd[1].isnumeric():
            newmsg = f'Это объект {cmd[1]}'
            data = DATABASE.getItemFromCat(user.cat, id = int(cmd[1]))
            if data:
                newmsg = f'ID: {data["id"]}\n\n{data["item"]}\n\nПредзаказ: {data["preorder"]}\nВладелец: {data["owner"]}'
                await func.short.send(user.id, newmsg=newmsg)