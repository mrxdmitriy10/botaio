from models.user import USER


async def cat(user:USER, arg):
    catid = str(arg).split()[0]
    user.setstate(2)
    user.setcat(catid)