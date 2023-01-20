from aiogram.fsm.context import FSMContext
from aiogram import types
from models import states
async def btc(state:FSMContext, clb: types.CallbackQuery):
        
        await state.set_state(states.InputState.btc_countpay.state)
        await state.update_data(delmessage=clb.message.message_id+1) #type:ignore
