from aiohttp import web
from models.sql import SQL
import func.create
import func.short
from aiogram import Bot
from aiogram.methods import DeleteMessage
from config import TOKEN
from aiogram.fsm.context import FSMContext
from models.sql import DATABASE

bot = Bot(token=TOKEN)


async def get_btc(req:web.BaseRequest):
    if  req.headers.get('User-Agent') == 'CrystalPAY-Callback':
        a = req.query
        amount = a.get('AMOUNT')
        userid = a.get('EXTRA')
        if amount == None:
            return
        amount = int(amount)
        user =  DATABASE.getDataUser(userid)

        DATABASE.setbalance(userid, user['balance'] + amount)


        print(f'{userid} + {amount}')
        await func.short.send(userid, user['start_msgid'], f'💰💰💰 Зачислено {amount}')

    return web.Response(status=200, text='Ok')
