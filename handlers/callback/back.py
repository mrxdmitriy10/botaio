from models import states
from aiogram.fsm.context import FSMContext
from models.user import USER


async def back(user: USER, state: FSMContext):

    if await state.get_state() == states.AdminState.adminpanel.state:
        return await state.clear()

    if await state.get_state() in [states.AdminState.userlist.state, states.InputState.broadcaster.state]:
        return await state.set_state(states.AdminState.adminpanel.state)

    if await state.get_state() == states.InputState.btc_countpay.state:
        user.setstate(3)
        await state.clear()
        return
            
    if await state.get_state() == states.InputState.qiwi_countpay.state:
        user.setstate(3)
        await state.clear()
        return


        

        

    if user.state == 1:

        user.setstate(user.state-1)
        user.setcity(0)
        return

    if user.state == 2:

        user.setstate(user.state-1)
        user.setcat(0)
        return

    if user.state == 3:
        user.setstate(0)
        user.setcat(0)
        return

    