from aiogram.types import Message
from aiogram.methods import EditMessageText, DeleteMessage
from aiogram import Bot
from aiogram.fsm.context import FSMContext


import logging
from config import TOKEN, MINBTC, MAXBTC
from config import USERLEVEL


from models.sql import SQL
from models.messages import MESSAGES
from models.keyboards import KEYBOARDS
from models.keyboards import USER



import func.create
import func.short
import func.request


bot = Bot(token=TOKEN)





async def inputpaycount(msg: Message, state: FSMContext):
    if msg.from_user is None:
        return
    user = USER(msg.from_user.id, msg.from_user.username)




    data = await state.get_data()
    print(f'data =  {data}')
    id = msg.from_user.id
    count = str(msg.text)
    if count.isnumeric():
        count = int(count)
        if count > MINBTC-1 and count < MAXBTC+1:
            await func.short.send(id, KEYBOARDS, newmsg = f'Перейдите по ссылке и получите BTC адрес для оплаты\n {func.request.pay(count, id)}\n\nЗачисление происходит от 30 минут до 3 часов в зависимости от загруженности сети Bitcoin')
            await state.clear()

    await DeleteMessage(chat_id = id, message_id = msg.message_id)


    key = await KEYBOARDS.answer(user, state)
    text = await MESSAGES.answer(user, state)
    user.upload()

    try:
        await EditMessageText(text = text, chat_id = id, message_id = user.start_msgid,reply_markup = key)
    except:
        print('no edit message')

    return