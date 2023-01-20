from models.user import USER
from aiogram.fsm.context import FSMContext
async def mainmenu(user:USER, state: FSMContext):
    user.setcity('0')
    user.setcat(0)
    user.setstate(0)
    await state.clear()