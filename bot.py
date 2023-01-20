from aiogram.types import MenuButtonWebApp, WebAppInfo
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.methods import SetChatMenuButton
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
import logging
from config import WEBAPP_HOST, WEBAPP_PORT, WEBHOOK_PATH, WEBHOOK_URL
from config import TOKEN
from routes_register import routes_register
import asyncio
import aiohttp_jinja2
import jinja2
from aiohttp_admin2.views import DashboardView, Admin
from pathlib import Path
from aiogram.client.session.aiohttp import AiohttpSession



logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)


async def on_startup(app:web.Application):
   
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    
    await routes_register(app, dp)


async def on_shutdown(app:web.Request):
    await bot.delete_webhook()
    await bot.close()
    logging.warning('Shutting down..')



if __name__ == '__main__':
    dp = Dispatcher(bot=bot, storage=MemoryStorage())
    app = web.Application()
    setup_application(app, dp)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    ).register(app, path="")
    web.run_app(app, host={WEBAPP_HOST}, port=WEBAPP_PORT)


