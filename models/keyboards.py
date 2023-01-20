from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup ,InlineKeyboardMarkup, InlineKeyboardButton, MenuButtonWebApp, WebAppInfo

from aiogram import types
from config import USERLEVEL
import models.states
from aiogram.fsm.context import FSMContext
from models.user import USER
from models import states
from models.sql import DATABASE





class KB:
    def __init__(self):
        self.main = InlineKeyboardMarkup(inline_keyboard=[])

        

        self.select = 0
        print('Клавиатуры загружены')

        
    def selectcat(self, catid, level):
        order, preorder = DATABASE.getItemRow(catid)
        if order > 0:
            if level == USERLEVEL['mainadmin']:
                a = '🅰️'
            else: a = ''
            row = [
                self.btn('Да', f'buy {catid}'),
                self.btn(f'{a}Остаток: {order} шт', f'items {catid}')
            ]
            self.main.inline_keyboard.append(row)
        else:
            self.main.inline_keyboard.append([self.btn('Предзаказ', f'preorder {catid}')])

        if level == USERLEVEL['mainadmin']:
            row = []
            row.append(self.btn(f'🅰️Удалить категорию {catid}', f'delcat {catid}'))
            if preorder >0:
                row.append(self.btn(f'🅰️ПЗ: {preorder} шт', f'preorder {catid}'))
            self.main.inline_keyboard.append(row)
        self.back()


    def profile(self, balance):
        self.main.inline_keyboard.append([self.btn('💳 Qiwi / Card', 'qiwi'), self.btn(f'₽ {balance}♻️', 'profile'), self.btn('BTC 💰', 'btc')])
        self.back()

    async def adminpanel(self):
        self.main.inline_keyboard.append([self.btn('предзаказы', 'preorders')])
        MenuButtonWebApp(text='Пользователи', web_app=WebAppInfo(url='localhost'), type='web_app')
        self.main.inline_keyboard.append([self.btn('пользователи', 'allusers')])
        self.main.inline_keyboard.append([self.btn('рассылка', 'broadcast')])
        self.main.inline_keyboard.append([self.btn('киви', 'qiwisetting')])
        self.back()

    async def broadcaster(self):
        self.back()

    async def selectuser(self, u):
        u = u['selectuser']
        for u in u:
            self.main.inline_keyboard.append([self.btn(f'{u}', f'selectuseratr {u}')])

        self.back()

    async def userlist(self):
        allusers = DATABASE.getAllUsers()
        for user in allusers:
            self.main.inline_keyboard.append([self.btn(f'{user["id"]} | {user["username"]}', f'selectuser {user["id"]}')])
        self.back()


    def btn(self, text, clb=''):
        if clb == '':
            clb = text
        return InlineKeyboardButton(text=text, callback_data=clb)
    def btnurl(self, text, url=''):
        if url == '':
            return
        return InlineKeyboardButton(text=text, url=url)

    def btnwa(self, text, url=''):
        if url == '':
            return
        return InlineKeyboardButton(text=text, url=url)

    async def close(self):
        self.main.inline_keyboard.append([self.btn('X', f'delete')])


    def citylist(self):
        list = DATABASE.getCityList()
        newlist = []
        for item in list:
            newlist.append(self.btn(item, f'city {item}'))
        self.main.inline_keyboard.append(newlist)


    def productlist(self, city, level, catid):
        list = DATABASE.getProductsList(city)

        for item in list:
            self.main.inline_keyboard.append([self.btn(f"{item['catname']}", f'cat {item["id"]} {item["catname"]}')])
        if level == USERLEVEL['mainadmin']:
            self.main.inline_keyboard.append([self.btn('🅰️Удалить город', f'delcity {city}')])
        self.back()

    def menulist(self, balance):
        list = []
        list.append(self.btn('Отзывы'))
        list.append(self.btn(f'₽ {balance}♻️', 'profile'))
        list.append(self.btn('Помощь'))


        self.main.inline_keyboard.append(list)
        return

    def adminmenubtn(self):
        name = '🅰️-панель'
        self.main.inline_keyboard.append([self.btn(name, 'adminpanel')])
        return

    def checkqiwi(self):
        name = 'Проверить оплату'
        self.main.inline_keyboard.append([self.btn(name, 'checkqiwi')])
        return
    async def clear(self):
        self.main = InlineKeyboardMarkup(inline_keyboard=[])

    def back(self):
        name = 'Назад'
        self.main.inline_keyboard.append([self.btn(name, name)])
        return

    def next(self):
        name = 'Вперед'
        self.main.inline_keyboard.append([self.btn(name, name)])
        return

    async def answer(self, user:USER, FSM: FSMContext ):
        await self.clear()



        if await FSM.get_state() == states.AdminState.userlist.state:
            u = await FSM.get_data()
            if 'selectuser' in u.keys():
                await self.selectuser(u)
            else:
                await self.userlist()
            return self.main

        if await FSM.get_state() == states.AdminState.adminpanel.state:
            await self.adminpanel()
            return self.main

        if await FSM.get_state() == states.InputState.broadcaster.state:
            await self.broadcaster()
            return self.main

        if await FSM.get_state() == states.InputState.btc_countpay.state:
            self.back()
            return self.main


        if await FSM.get_state() == models.states.InputState.qiwi_countpay.state:

            self.checkqiwi()
            self.back()
            return self.main

        
        if user.state == 0:
            self.citylist()
            self.menulist(user.balance)
            if user.level == USERLEVEL['mainadmin']:
                self.adminmenubtn()

        if user.state == 1:
            self.productlist(user.city, user.level, user.cat)
            

        if user.state == 2:
            self.selectcat(user.cat, user.level)
        
        if user.state == 3:
            self.profile(user.balance)

        
        return self.main

KEYBOARDS = KB()