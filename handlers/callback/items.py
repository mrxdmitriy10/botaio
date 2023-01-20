from models.sql import SQL
from models.user import USER
from config import USERLEVEL
from func import short
from aiogram import types
from models.sql import DATABASE


async def items(user:USER, clb:types.CallbackQuery, arg):
    if clb.message is None: return

    if user.level == USERLEVEL['mainadmin']:
        data = DATABASE.getItemsList(int(arg))

        await short.send(userid=user.id, newmsg=data)