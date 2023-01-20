from aiogram.types import Message
from aiogram.filters import Command
from aiogram.methods import EditMessageText, DeleteMessage
import logging
from config import TOKEN
from config import USERLEVEL
from aiogram import Bot


from aiogram.fsm.context import FSMContext
from models.sql import DATABASE
from models.messages import MESSAGES
from models.keyboards import KEYBOARDS
from models.user import USER


import handlers.command
import handlers.command.adm


import func.create
import func.short
bot = Bot(token=TOKEN)


async def text(msg: Message, state: FSMContext):

    if msg.from_user is None or msg.text is None:
        return
    newmsg = None

    user = USER(
        msg.from_user.id,
        msg.from_user.username
    )


    async def short(text, timer=0, userid=msg.from_user.id):
        return await func.short.send(userid, newmsg=text, timer=timer)


    arg = ''
    msgsplit = msg.text.split(maxsplit=1)
    cmd = msgsplit[0]
    if len(msgsplit) > 1:
        arg = msgsplit[1]
    else:
         arg = ''

    print(f'cmd: {cmd}, arg: {arg}')

    if user.level == USERLEVEL['mainadmin']:
        if '/user' == cmd:
            await handlers.command.adm.user(user, arg, short)

        if '/item' in cmd:
            await handlers.command.adm.item(user, cmd, msg)

        if '/add' == cmd:
            await handlers.command.adm.add(user, arg, short)

        if '/level' == cmd:
            await handlers.command.adm.level(user, arg, short)

    if user.level == USERLEVEL['user']:
        if '/level' == cmd:
                await handlers.command.level(user, arg, short)


    key = await KEYBOARDS.answer(user, state)
    text = await MESSAGES.answer(user, state)

    user.upload()  # Загружаем userdata

    try:
        await EditMessageText(text= text, chat_id = user.id, message_id = user.start_msgid, reply_markup=key)
    except:
        print('no edit message')
    return await msg.delete()
