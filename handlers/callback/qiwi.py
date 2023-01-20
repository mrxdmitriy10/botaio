from aiogram.fsm.context import FSMContext
from aiogram import types
from models import states
async def qiwi(state:FSMContext, clb: types.CallbackQuery):
        
        await state.set_state(states.InputState.qiwi_countpay)
        await state.update_data()
        await state.update_data(delmessage=clb.message.message_id+1) #type: ignore
        await state.update_data(comment=str(clb.from_user.id))