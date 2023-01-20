import sqlite3
import logging
from config import DATABASENAME
logging.basicConfig(level=logging.INFO)


class SQL:
    def __init__(self):
        self.name = DATABASENAME
        self.con = sqlite3.connect(self.name)
        try:
            self.createalltable()
            print('Таблицы созданы')
        except:
            print('Таблицы найдены')


    def ex(self, func, value=None):
        cur = self.con.cursor()
        if value != None:
            res = cur.execute(func, value)
        else:
            res = cur.execute(func)
        self.con.commit()
        #cur.close()
        return res

    def createalltable(self):
        self.createtableusers()
        self.createtablecity()
        self.createtableproducts()
        self.createtableitems()


    def setbalance(self, id, amount):

        return self.ex(f'''UPDATE users SET balance = ? WHERE id = ?''', (amount, id))
    def delcity(self, city):
        return self.ex(f'''DELETE FROM city WHERE city = ?''', (city,))

    def delcat(self, catid):
        return self.ex(f'''DELETE FROM products WHERE id = ?''', (catid,))


    def updateStartMsg(self, id, start_msgid):
        return self.ex(f'''UPDATE users SET start_msgid = ? WHERE id = ?''', (start_msgid, id))

    def adduser(self, id, username):
        return self.ex(f'''INSERT OR IGNORE INTO users (id, username, state, balance, start_msgid, level, city, cat) VALUES (?,?,?,?,?,?,?,?)''', (id, username, 0, 0, 0, 0, '0', 0))

    def addproduct(self, city, catname):
        return self.ex(f'''INSERT INTO products (city, catname) VALUES (?,?)''', (city, catname))

    def addcity(self, city):
        return self.ex(f'''INSERT OR IGNORE INTO city (city) VALUES (?)''', (city,))

    def changelevel(self, id, level):
        return self.ex(f'''INSERT OR REPLACE INTO users (level) VALUES (?) WHERE id = ?''', (level, id))

    def additem(self, item, catid, preorder=0, owner=0):
        try:
            self.ex(f'''INSERT INTO items (item, catid, preorder, owner) VALUES (?,?,?,?)''', (item, int(catid), int(preorder), int(owner)))
            res = f'cat {catid} \n + {item}'
        except:
            res = f'XXX\ncat {catid} \n XXX {item}'
        return res
        

    def createtableusers(self):
        return self.ex('''CREATE TABLE users (id INTEGER PRIMARY KEY NOT NULL UNIQUE, username TEXT, state INTEGER, balance INTEGER, start_msgid INTEGER, level INTEGER, city TEXT, cat INTEGER)''')

    def createtableitems(self):
            return self.ex('''CREATE TABLE items (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, item TEXT, catid INTEGER, preorder INTEGER, owner INTEGER)''')


    def createtablecity(self):
        return self.ex('''CREATE TABLE city (city TEXT PRIMARY KEY NOT NULL UNIQUE)''')

    def createtableproducts(self):
        return self.ex('''CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, catname TEXT)''')



    def uploadUserDataToSql(self, data):

        return self.ex(f'''UPDATE users SET username = ?, state = ?, balance = ?, start_msgid = ?, level = ?, city = ?, cat = ? WHERE id = ?''', (
            data['username'],
            data['state'],
            data['balance'],
            data['start_msgid'],
            data['level'],
            data['city'],
            data['cat'],
            data['id']))


    def getAllUsers(self):
        pos = self.ex(f'''SELECT id, username FROM users''').fetchall()
        if len(pos)>0:
            pass
        a=list()

        for i in pos:
            a.append({'id': i[0], 'username': i[1]})
        return a


    def getDataUser(self, id):
        data = None
        pos = self.ex(f'''SELECT id, username, state, balance, start_msgid, level, city, cat FROM users WHERE id = ?''',
                      (id,)).fetchall()
        if len(pos)>0:
            data = {
                'id': int(pos[0][0]),
                'username': str(pos[0][1]),
                'state': int(pos[0][2]),
                'balance': int(pos[0][3]),
                'start_msgid': int(pos[0][4]),
                'level': int(pos[0][5]),
                'city': str(pos[0][6]),
                'cat': pos[0][7]
                }
            res = True
        else:
            self.adduser(id, 'None')
            data = self.getDataUser(id)
            res = False
            print('Пользователь добавлен в бд')
        print('Пользователь загружен из бд')
        return data

    def getCityList(self):
        data = []
        citylist = self.ex('''SELECT * FROM city''')
        for item in citylist:
            data.append(item[0])
        return data

    def changeItemOwner(self, id, owner = 0):
        try:
            self.ex('''UPDATE OR IGNORE items SET owner = ? WHERE id = ?''', (owner, id))
            return f'Update item {id}  OWNER = {owner}'
        except:
            return f'NOT UPDATE ITEM'

    def getItemRow(self, catid, owner = 0):
        order = self.ex('''SELECT COUNT(id) FROM items WHERE preorder = 0 and catid = ? AND owner = ?''',(catid, owner)).fetchall()
        preorder = self.ex('''SELECT COUNT(id) FROM items WHERE preorder = 1 and catid = ? AND owner = ?''',(catid, owner)).fetchall()
        order = order[0][0]
        preorder = preorder[0][0]
        return order, preorder


    def getItemsList(self, catid, owner = 0, preorder = 0):
            pos = self.ex('''SELECT * FROM items WHERE catid = ? AND preorder = ? AND owner = ?''',(catid, preorder, owner)).fetchall()
            data = []
            text = f'Кат. {catid} '
            for item in pos:
                data.append({
                    'id': int(item[0]),
                    'item': str(item[1]),
                    'catid': int(item[2])
                })
                text = text + f'\n/item_{item[0]}\n\n'
            
            
            return text
            


    def getItemFromCat(self, catid, owner = 0, preorder = 0, id = 0):
        if id == 0:
            pos = self.ex('''SELECT * FROM items WHERE catid = ? AND preorder = ? AND owner = ?''',(catid, preorder, owner)).fetchall()
        else:
            pos = self.ex('''SELECT * FROM items WHERE id = ? AND preorder = ? AND owner = ?''',(id, preorder, owner)).fetchall()

        try:
            if len(pos) > 0:
                data = {
                    'id': int(pos[0][0]),
                    'item': str(pos[0][1]),
                    'catid': int(pos[0][2]),
                    'preorder': int(pos[0][3]),
                    'owner': int(pos[0][4])}
                res = '1'
            else:
                data = None
                res = 'Не нашлось ничего'
        except:
            data = {}
            res = '0'
        logging.info(f'GET ITEM in catid {catid} FROM DATABASE : {res}')
        return data

    def getProductsList(self, city):
        data = []
        pos = self.ex ('''SELECT * FROM products WHERE city = ?''',(city,)).fetchall()
        try:
            for item in pos:
                data.append({
                    'id': int(item[0]),
                    'city': item[1],
                    'catname': item[2]})
            res = True
        except:
            res = False
        logging.info(f'GET PRODUCTS in {city} FROM DATABASE : {res}')
        return data

DATABASE = SQL()