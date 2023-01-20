import aiohttp_jinja2
from aiohttp import web
from models.sql import DATABASE

@aiohttp_jinja2.template("main.html")
async def main(req: web.BaseRequest):
    users = '<b>ПОЛЬЗОВАТЕЛИ</b><br>'
    for i in DATABASE.getAllUsers():
        users = users + f'{i["id"]} {i["username"]}<br>'
    allcity = DATABASE.getCityList()
    a = req.query
    city = a.get('city')
    citys = '<b>Города</b><br>'
    for i in allcity:
        citys = citys + f'{i}<br>'
    text = f'{users}<br>{citys}'
    if city in allcity:

        text = text + f'{DATABASE.getProductsList(city)}'
    #return web.Response(content_type='text/html', text=str(text))
    return {'users': users}
