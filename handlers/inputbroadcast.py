from aiogram.types import Message
from aiogram.methods import EditMessageText, DeleteMessage
from aiogram import Bot
from aiogram.fsm.context import FSMContext

import asyncio
import logging
from config import TOKEN, MINBTC, MAXBTC
from config import USERLEVEL
from func.broadcaster import broadcaster
from models import states
from models.messages import MESSAGES
from models.keyboards import KEYBOARDS
from models.sql import DATABASE
from models.user import USER



from models.sql import SQL

import func.create
import func.short
import func.request
import handlers



bot = Bot(token=TOKEN)





async def inputbroadcast(msg: Message, state: FSMContext):
    if msg.from_user is None:
        return


    user = USER(msg.from_user.id, msg.from_user.username)


    



    id = msg.from_user.id
    text = msg.text

    asyncio.create_task(broadcaster(msg), name = 'broadcaster', )
    await state.set_state(states.AdminState.adminpanel)


    key  = await KEYBOARDS.answer(user, state)
    text = await MESSAGES.answer(user, state)

    try:
        await EditMessageText(text = str(text), chat_id=user.id, message_id=user.start_msgid, reply_markup = key)
    except:
        print('no edit message')

    await msg.delete()

    return