from aiogram.fsm.context import FSMContext
from models import states
from models.sql import DATABASE

async def selectuser(arg, state:FSMContext):

    await state.update_data({'selectuser': DATABASE.getDataUser(arg)})