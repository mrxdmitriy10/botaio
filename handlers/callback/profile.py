from models.user import USER

async def profile(user:USER):
    user.setstate(3)