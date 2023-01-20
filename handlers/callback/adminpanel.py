from models.user import USER
import func.create
from aiogram.methods import SendMessage
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from models.states import AdminState
from aiogram.methods import SendMessage

async def adminpanel(state:FSMContext):
    await state.set_state(AdminState.adminpanel.state)

    