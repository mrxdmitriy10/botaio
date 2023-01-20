from models.sql import SQL
import logging
from config import USERLEVEL
from models.sql import DATABASE


class USER:
    def __init__(self, id, username=None):
        self.id = id
        self.username = username
        self.state = 0
        self.balance = 0
        self.cat = 0
        self.start_msgid = 0
        self.level = USERLEVEL['user']
        self.city = '0'

        self.update(DATABASE.getDataUser(self.id))
        # self.ifcatcity()


    def incbalance(self, amount):
        self.balance= self.balance + int(amount)
        self.upload()



    def setstartmsg(self, msgid):

        self.start_msgid = int(msgid)

        logging.info(f'{self.id} STARTMSG : {msgid}')

    def setcat(self, cat):

        self.cat = int(cat)

        logging.info(f'{self.id} CAT : {cat}')

    def setstate(self, state):

        self.state = int(state)

        logging.info(f'{self.id}.state = {state}')

    def setlevel(self, level):

        self.level = int(level)

        logging.info(f'{self.id}.level : {level}')


    def setcity(self, city):

        self.city = str(city)

        logging.info(f'USER CITY : {city}')


    def adduser(self, func):
        try:
            func(self.id, self.username) ## добавили юзера
            res = True
        except:
            res = False
        logging.info(f'ADDUSER : {res}')
        

    def upload(self):
        try:
            DATABASE.uploadUserDataToSql(self.userdata())
            res = True
        except:
            res = False

        logging.info(f'UPLOAD USERDATA to DATABASE : {res}')



    def update(self, data):

        self.state = data['state']
        self.balance = data['balance']
        self.start_msgid = data['start_msgid']
        self.level = data['level']
        self.city = data['city']
        self.cat = data['cat']

   #         self.adduser(self.addUser(self.id, self.username))
        return


    def userdata(self):
        data = {
            'id': self.id,
            'username': self.username,
            'state': self.state,
            'balance': self.balance,
            'start_msgid': self.start_msgid,
            'level': self.level,
            'city': self.city,
            'cat': self.cat
        }
        return data