from aiogram import types
from aiohttp import web

from aiogram.fsm.context import FSMContext
import handlers
from models.sql import DATABASE


class BaseHandler:
    
    async def inputbroadcast(self, msg: types.Message, state: FSMContext):
        print('inputbroadcaster')
        return await handlers.inputbroadcast(msg, state)
    async def qiwihandler(self,req:web.BaseRequest):
        return web.Response(status=200, text='Ok')
    async def btchandler(self, req:web.BaseRequest):
        return await handlers.get_btc(req)
    async def callb(self, clb: types.CallbackQuery, state: FSMContext):
        return await handlers.clb(clb, state)
    async def start(self, msg: types.Message, state: FSMContext):
        print('starthandler')
        return await handlers.start(msg, state)
    async def inputpay(self, msg: types.Message, state: FSMContext) -> None:
        print('inputpayhandler')
        return await handlers.inputpaycount(msg, state)
    async def csvhandler(self, msg: types.Message, state: FSMContext) -> None:
        print('csvhandler')
        return await handlers.ct_document(msg, state)
    async def anytext(self, msg: types.Message, state: FSMContext) -> None:
        print('anymesshandler')
        await handlers.text(msg, state)
        return
