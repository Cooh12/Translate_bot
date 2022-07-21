from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from middlewares.throttling import ThrottlingMiddleware
from utils.db_api.db_gino import db
from data import config


bot = Bot(token=config.API_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(ThrottlingMiddleware(limit=2))
__all__ = ['db','bot','storage','dp']


