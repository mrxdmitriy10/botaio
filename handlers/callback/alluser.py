from aiogram.fsm.context import FSMContext
from models import states

async def alluser(state:FSMContext):
    await state.set_state(states.AdminState.userlist.state)
    
