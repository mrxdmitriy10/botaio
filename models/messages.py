from typing import Optional, List


from config import MINBTC, MAXBTC, QIWINUMBER

import func.request
from models.sql import DATABASE
from aiogram.fsm.context import FSMContext
import models.states
from models.user import USER

class MSG:

    def __init__(self):
        self.main = ''
        print('Ответы загружены')


    def profile(self, balance):
        self.main = f'Ваш баланс: {balance} \n\nПополнить:'

    async def balance(self, balance, amount, userid, state: FSMContext):
        url = await state.get_data()
        if url == {}:
            await state.update_data(urlpay = func.request.pay(amount, userid))
            url = await state.get_data()

        return(f'Ваш баланс: {balance} ₽\n\nЧтобы пополнить баланс на {amount} перейдите по ссылке --> {url["urlpay"]}')

    def start(self):
        space = '                 '
        self.main =  f'Главное меню\n\nПривет, чувствуй себя как дома!{space}\nУ нас можно найти плюшки к чаю\nПросто выбери город\n'

    def city(self, city):
        self.main =  f'{city}\n\nВот что есть у нас...'

    def cat(self, catname, balance):
        self.main = f'Вы покупаете {catname}\n\nСтоиомсть продукта: 3500\nВаш баланс: {balance}'


    def broadcast(self):
        self.main = f'\nРассылка\n\n Введите сообщение для рассылки'

    def userlist(self):

        self.main = f'\nПользователи\n\n'
    def selectuser(self, u):
        self.main = f'\nПользователь\n\n{u}'


    def paybtc(self, balance):
        self.main = f'\nУ вас есть {balance} руб\nВведите сумму пополнения с помощью BTC\n\nОт {MINBTC} до {MAXBTC}'

    def payqiwi(self, balance, FSM:FSMContext):
  
        self.main = f'\nУ вас есть {balance} руб\nВДля пополнения через QIWI\nпереведите нужную сумму на\n\nномер: {QIWINUMBER}\nкомментарий:)'

    async def answer(self, user: USER, FSM:FSMContext):
        if user.state == 0:
            self.start()
        if user.state == 1:
            self.city(user.city)
        if user.state == 2:
            self.cat(user.cat, user.balance)
        if user.state == 3:
            self.profile(user.balance)

        if await FSM.get_state() == models.states.AdminState.userlist.state:

            u = await FSM.get_data()
            if 'selectuser' in u.keys():
                self.selectuser(u['selectuser'])
            else:
                self.userlist()
            

        if await FSM.get_state() == models.states.InputState.broadcaster.state:
            self.broadcast()

        if await FSM.get_state() == models.states.InputState.btc_countpay.state:
            self.paybtc(user.balance)

        if await FSM.get_state() == models.states.InputState.qiwi_countpay.state:
            self.payqiwi(user.balance, FSM)



        return self.main


MESSAGES = MSG()

        
    