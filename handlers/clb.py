from aiogram.types import CallbackQuery
from aiogram.methods import AnswerCallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram import Bot
import asyncio
from models import states
import logging
from config import QIWINUMBER





from config import TOKEN
from config import USERLEVEL

from models.sql import DATABASE
from models.keyboards import KEYBOARDS
from models.messages import MESSAGES
from models.user import USER




from func.broadcaster import broadcaster
import func.short
import func.create

import handlers.callback




bot = Bot(token=TOKEN)


async def clb(clb: CallbackQuery, state: FSMContext):
    if clb.data is None or clb.message is None: return AnswerCallbackQuery(callback_query_id=clb.id)

    user = USER(clb.from_user.id, clb.from_user.username)



    

    cmd = None
    arg = None

    clbsplit = clb.data.split(maxsplit=1)
    cmd = clbsplit[0]
    if len(clbsplit) > 1:
        arg = clbsplit[1]

    print(f'clb | cmd = {cmd} arg = {arg}')
    
    if 'Назад' in cmd:
        await handlers.callback.back(user, state)


    if cmd == 'selectuser':
        await handlers.callback.selectuser(arg, state)
    if cmd == 'allusers':
        await handlers.callback.alluser(state)
    if cmd == 'profile':
        await handlers.callback.profile(user)
    if cmd == 'broadcast':
        await handlers.callback.broadcast(state)
    if cmd == 'adminpanel':
        await handlers.callback.adminpanel(state)
    if cmd == 'qiwi':
        await handlers.callback.qiwi(state, clb)
    if cmd == 'btc':
        await handlers.callback.btc(state, clb)
    if cmd == 'mainmenu':
        await handlers.callback.mainmenu(user, state)
    if cmd == 'items':
        await handlers.callback.items(user, clb, arg)
    if cmd == 'city':
        await handlers.callback.city(user, arg)
    if cmd == 'delete':
        await handlers.callback.delete(clb)
    if cmd == 'delcity':
        await handlers.callback.delcity(user, arg)
    if cmd == 'delcat':
        await handlers.callback.delcat(user, arg)
    if cmd == 'cat':
        await handlers.callback.cat(user, arg)
    if cmd == 'buy':
        await handlers.callback.buy(user, clb)
    user.upload()

#    if await state.get_state() == states.AdminState.adminpanel.state:
#        return AnswerCallbackQuery(callback_query_id=clb.id)

    key = await KEYBOARDS.answer(user, state)
    text = await MESSAGES.answer(user, state)

    try:
        await clb.message.edit_text(str(text), reply_markup = key)
    except:
        print('no edit message')

    return AnswerCallbackQuery(callback_query_id=clb.id)
    