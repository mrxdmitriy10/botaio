from aiogram.types import Message
from aiogram.methods import DeleteMessage, SendMessage

import logging
from config import TOKEN
from aiogram import Bot

import func.create
from aiogram.fsm.context import FSMContext


from models.sql import DATABASE
from models.messages import MESSAGES
from models.keyboards import KEYBOARDS
from models.user import USER



async def start(msg: Message, state: FSMContext):
    if msg.from_user is None:
        return
    logging.info("[[[start handler]]]")

    user = USER(msg.from_user.id, msg.from_user.username)
    



    user.setstate(0)
    await DeleteMessage(chat_id= msg.from_user.id, message_id=msg.message_id)
    # Удалили /start
    if user.start_msgid != 0:
        # Удалили сообщение из старой стартмсг
        try:
            await DeleteMessage(chat_id= msg.from_user.id, message_id=user.start_msgid)
        except:
            logging.warning('Не удалил')

    user.setstartmsg(msg.message_id+1)
    user.upload()
    key = await KEYBOARDS.answer(user, state)
    text = await MESSAGES.answer(user, state)
    return SendMessage(chat_id = msg.from_user.id, text = text, reply_markup=key)
