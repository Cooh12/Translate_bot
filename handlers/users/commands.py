from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from loader import dp
from utils.db_api.quick_commands.commands_user import add_user
from utils.db_api.quick_commands.commands_dict import  all_dict_kb, select_all_user_dictionaries
from states import message_states
from keysboards.inline_kb_menu.inline_kb_menu_answer import ikb_cancel_dictionary_creation




@dp.message_handler(Command('start'))
async def command_start(message: types.Message):
    await message.answer(await add_user(message.from_user.id, message.from_user.username))
    await message.delete()

@dp.message_handler(Command('help'))
async def command_help(message: types.Message):
    await message.delete()
    await message.answer(f"С вопросами обращайтесь @Wn_Bs ")


@dp.message_handler(Command('dictionaries'))
async def command_dict(message: types.Message, state : FSMContext):
    """Показывает все словари пользователя"""
    dictionaries = await select_all_user_dictionaries(message.from_user.id)

    await state.update_data(next_values=[0, 6])
    await message.answer(
        text=f'Выберите словарь: (Всего - {len(dictionaries)})📚',
        reply_markup=all_dict_kb(
            dictionaries, 
            action='list_of_dictionaries',
            action_more='more_dictionaries'
            )
        )
    await message.delete()


@dp.message_handler(Command('create_dictionaries'))
async def command_dict(message: types.Message):
    """Создает словарь"""
    await message_states.UserMessage.create_dict.set() 
    await message.answer(text='Придумайте название📙:', reply_markup=ikb_cancel_dictionary_creation)
    await message.delete()


    