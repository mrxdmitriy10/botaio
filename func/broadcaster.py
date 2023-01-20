import asyncio
import logging
from aiogram.methods import SendMessage
import func.short
from aiogram import exceptions
from aiogram import types
from models.sql import SQL
import func.create
from models.sql import DATABASE
from models.user import USER
from models.keyboards import KEYBOARDS
import func.short


log = logging




async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    return await func.short.send(userid = user_id, newmsg=text)


async def broadcaster(msg:types.Message):
    await KEYBOARDS.clear()

    userlist = DATABASE.getAllUsers()
    print(userlist)
    if msg.from_user is None: 
        return 0
    userid = msg.from_user.id
    text = msg.text

    count = 0
    try:
        await func.short.send(userid = userid, newmsg=f'Запуск рассылки')

        for user in userlist:
            if await send_message(user_id=user['id'], text = str(text)):
                count += 1
            else:
                print(f"{user['id']} - не отправил")
            await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)

    finally:
        logging.info(f"{count} messages successful sent.")
        await func.short.send(userid = userid, newmsg=f'Сообщение доставлено {count} пользователям')

    return count