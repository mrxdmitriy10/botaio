
from aiogram.fsm.state import StatesGroup, State




class AdminState(StatesGroup):
    selectuser = State()
    adminpanel = State()
    userlist = State()


class InputState(StatesGroup):
    btc_countpay = State()
    qiwi_countpay = State()
    broadcaster = State()
