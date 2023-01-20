from models.user import USER
from models.sql import DATABASE
from aiogram import types
import func.short


async def buy(user:USER, clb: types.CallbackQuery):
    if clb.message is None: return

    async def short(text, timer = 0, userid = user.id):
            await func.short.send(userid, msgid=text, timer=timer )


    Item = DATABASE.getItemFromCat(int(user.cat))
    print(f'>>>>{Item}')
    amount = 3200
    if Item:
        if user.balance < amount:
            user.setstate(3)
        else:
            print(DATABASE.changeItemOwner(Item['id'], owner = user.id))
            user.setstate(1)
            await short(f'Продукт получен {Item}', timer = 3)
    else:
        user.setstate(1)
        await short(f'Нет в наличии')


        user.setcat(0)
        user.setcity('0')
