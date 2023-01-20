import asyncio
from aiogram.methods import SendMessage, DeleteMessage
from config import TOKEN
from aiogram import Bot, Dispatcher
import logging as log
import func.create
from aiogram import exceptions
from models.keyboards import KEYBOARDS



bot = Bot(token=TOKEN)

async def autoDelMsg(userid, msgid, timer):
    await asyncio.sleep(timer)
    DeleteMessage(chat_id= userid, message_id=msgid)


async def send(userid, msgid=None, newmsg = '', timer=0):
    
        await KEYBOARDS.clear()
        await KEYBOARDS.close()
        try:
            await bot.send_message(userid, newmsg, reply_markup=KEYBOARDS.main)
        except exceptions.TelegramRetryAfter as e:
            log.error(f"Target [ID:{userid}]: Flood limit is exceeded. Sleep {e.retry_after} seconds.")
            await asyncio.sleep(e.retry_after)
            await bot.send_message(userid, newmsg, reply_markup=KEYBOARDS.main)
        except exceptions.TelegramForbiddenError:
            log.exception(f'Target [ID:{userid}]: stop bot')
        except exceptions.TelegramAPIError:
            log.exception(f"Target [ID:{userid}]: failed")
        else:
         #   log.info(f"Target [ID:{userid}]: success")
            
            if timer!=0 and msgid is not None:
                await autoDelMsg(userid, msgid+1, timer)
            await KEYBOARDS.clear()

            return True
        await KEYBOARDS.clear()
        return False