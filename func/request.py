import requests
from config import WEBHOOK_URL
def pay(amount, userid):
        URL='https://api.crystalpay.ru/v1/'
        PARAMS={
            's': '8e3486bff5f3add34302725f64f1825eb9bcc00e',
            'n': 'sister15',
            'o': 'invoice-create',
            'amount': amount,
            'lifetime': 1440,
            'm': 'test',
            'extra': str(userid),
            'callback': f'{WEBHOOK_URL}api/btc'}
        r = requests.get(url = URL, params = PARAMS)
        return r.json()['url']