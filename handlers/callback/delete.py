from aiogram import types

async def delete(clb: types.CallbackQuery):
    if clb.message is None: return

    await clb.message.delete()