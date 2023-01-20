
from models.user import USER



async def city(user:USER, arg):
        city = str(arg)
        user.setstate(1)
        user.setcity(city)