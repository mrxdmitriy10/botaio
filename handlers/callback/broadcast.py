from aiogram.fsm.context import FSMContext
from models import states

async def broadcast(state:FSMContext):
        await state.set_state(states.InputState.broadcaster.state)