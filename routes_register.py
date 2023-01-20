from aiohttp import web
from aiogram import Dispatcher, exceptions, types
from aiogram import F, filters
from models.states import InputState
from models.BaseHandler import BaseHandler
from models.sql import SQL
from models.sql import DATABASE
import view


async def routes_register(app: web.Application, dp: Dispatcher, index=BaseHandler()):
   

    app.router.add_get('/index', view.main)
    app.router.add_get('/api/btc', index.btchandler)  # type:ignore
    app.router.add_post('/api/qiwi', index.qiwihandler)
    dp.callback_query.register(index.callb, lambda callback_query: True)
    dp.message.register(index.start, filters.CommandStart())
    dp.message.register(index.inputpay, F.text, InputState.btc_countpay)
    dp.message.register(index.inputbroadcast, F.text, InputState.broadcaster)

    dp.message.register(index.anytext, F.text)
    dp.message.register(index.csvhandler, F.document)
