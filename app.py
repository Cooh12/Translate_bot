async def on_startup(dp):
    from loader import db
    from utils.db_api.db_gino import on_startup
    await on_startup(db)
    #await db.gino.drop_all()
    await db.gino.create_all()
    print('Бот запущен')
    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    

    

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    executor.start_polling(dp , on_startup=on_startup)

            