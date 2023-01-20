import requests
#from config import WEBHOOK_URL
def pay():
        URL='https://edge.qiwi.com/payment-notifier/v1/hooks'
        PARAMS={

            'hookType': 1,
            'param': f'https://ac0e-2a00-1fa2-4280-297e-49e4-2195-39d9-42ab.eu.ngrok.io/api/qiwi',
            'txnType': 0}
        r = requests.put(url = URL, params = PARAMS)
        return r.json()

print(pay())