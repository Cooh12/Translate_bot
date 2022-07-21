from asyncpg import UniqueViolationError
from utils.db_api.schemas.user import User
from utils.db_api.db_gino import db

async def add_user(user_id: int, username: str):
    try:
        user = User(user_id=user_id, username=username)
        await user.create()
        return 'Привет👋 \nДанный бот переведет для тебя слова и тексты с русского на английский и наоборот. А также создаст словарь с сохраненными словами для дальнейшего изучения🙃'
    except UniqueViolationError:
        return 'И еще раз привет🤚 \nЕсли нужна помощь по работе с ботом воспользуйся командой  /help'


async def select_all_user():
    users = await User.query.gino.all()
    return users

async def count_users():
    count = await db.func.count(User.user_id).gino.scalar()
    return count

async def select_user(user_id):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user

async def update_user_name(user_id, new_name):
    user = await select_user(user_id)
    await user.update(update_name=new_name).apply()