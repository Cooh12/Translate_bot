from aiogram import types

async def set_default_commands(dp):
    await dp.bot.set_my_commands([        
        types.BotCommand('dictionaries', 'Показать словари'),
        types.BotCommand('create_dictionaries', 'Создать словарь'),
        types.BotCommand('start', 'Старт'),
        types.BotCommand('help', 'Помощь'),
    ])