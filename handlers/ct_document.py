from aiogram.types import Message
from aiogram.methods import EditMessageText, DeleteMessage
from aiogram import Bot
from aiogram.fsm.context import FSMContext

import logging
from config import TOKEN
from config import USERLEVEL

from models.sql import DATABASE
from models.messages import MESSAGES
from models.messages import USER




import func.create, func.short

import csv

bot = Bot(token=TOKEN)



async def ct_document(message: Message, state: FSMContext):
    if message.from_user is None:
        return

    if message.document is None:
        return

    async def short(text, timer = 0, userid = message.from_user.id):
        await func.short.send(userid, newmsg=text, timer=timer)

    user = USER(message.from_user.id, message.from_user.username)

    if user.level == USERLEVEL['mainadmin']:
        print(message.document)
        if message.document.mime_type == 'text/csv':
            file = await bot.get_file(message.document.file_id)
            file_path = file.file_path
            #sdsdsd



            document = message.document
            await bot.download(document)
    

            with open('csv.csv', 'r', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
                for row in spamreader:
                    print(row)
                    try:
                        DATABASE.additem(row[0], int(row[1]), int(row[2]))
                    except:
                        await short(f'{row} ')
            await message.delete()
            await short('Добавлено', timer = 1)
    return