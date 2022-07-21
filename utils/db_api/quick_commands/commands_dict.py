from aiogram import types
from asyncpg import UniqueViolationError
from utils.db_api.schemas.dictionary import Dictionary
from keysboards.inline_kb_menu.callback_dates import dictionaries_cb, dictionaries_menu_cb, delete_menu_cb, dictionaries_more_cb
from utils.db_api.schemas.words import Words


async def create_dictionary(user_id: int, dictname: str):
    try:
        dict = Dictionary(user_id=user_id, dictname=dictname)
        await dict.create()
    except UniqueViolationError:
        print('Словарь с таким именем уже существует')


async def select_all_user_dictionaries(user_id):
    dictionaries = await Dictionary.query.where(Dictionary.user_id == user_id).gino.all()
    return dictionaries


async def select_dictionary(id):
    dictionary = await Dictionary.query.where(Dictionary.id == id).gino.first()
    return dictionary

async def delete_dictionary_command(id):
    dictionary = await Dictionary.query.where(
        Dictionary.id == id, 
        ).gino.first()
    await dictionary.delete()

    
async def change_dictname(id, new_name):
    dictionary = await Dictionary.query.where(Dictionary.id == id).gino.first()
    words = await Words.query.where(Words.dict_id == dictionary.id).gino.all()
    for word in words:
        await word.update(dictname=new_name).apply()
    await dictionary.update(dictname=new_name).apply()


async def quantity_try_add(id):
    dictionary = await Dictionary.query.where(Dictionary.id == id).gino.first()
    new = dictionary.quantity_try + 1 
    await dictionary.update(quantity_try=+new).apply()

async def successful_try_add(id):
    dictionary = await Dictionary.query.where(Dictionary.id == id).gino.first()
    new = dictionary.successful_try + 1 
    await dictionary.update(successful_try=new).apply()

async def dictionary_date_update(id, date):
    dictionary = await Dictionary.query.where(Dictionary.id == id).gino.first()
    await dictionary.update(last_study=date).apply()

def all_dict_kb(dictionaries:list, action: str, action_more : str,initial_value = 0, last_value=6):
    
    keyboard = types.InlineKeyboardMarkup()
    for dictionary in dictionaries[initial_value:last_value]:
                keyboard.row(types.InlineKeyboardButton(
                text=f"{dictionary.dictname}", 
                callback_data=dictionaries_cb.new(
                    id_dictionary=dictionary.id,
                    action=action
                ))
                )
    
    keyboard.row(
            types.InlineKeyboardButton(
                text='Убрать список ❌', 
                callback_data=dictionaries_more_cb.new(
                    action='remove_the_list'
                ),)
    )
    if len(dictionaries) > last_value:
        keyboard.row(
            types.InlineKeyboardButton(
                text='Показать еще', 
                callback_data=dictionaries_more_cb.new(
                    action=action_more
                ),),
                
        )
    return keyboard


def dictionaries_menu_kb(id_dictionary, len_dictionary):
    inline_keyboard = [
        [
            types.InlineKeyboardButton(text='Удалить ❌', callback_data=dictionaries_menu_cb.new(
                id_dictionary=id_dictionary,
                action='delete_dictionary'
            )),
            types.InlineKeyboardButton(text='Изменить название', callback_data=dictionaries_menu_cb.new(
                id_dictionary=id_dictionary,
                action='change_the_dictionary_name'
            )),
        ]
    ]
    if len_dictionary != 0:
        inline_keyboard.append(
        [
           types.InlineKeyboardButton(text='Статистика 📈', callback_data=dictionaries_menu_cb.new(
                id_dictionary=id_dictionary,
                action='dictionary_statistics'
            )),
           types.InlineKeyboardButton(text='Учить 📖', callback_data=dictionaries_menu_cb.new(
                id_dictionary=id_dictionary,
                action='learn_words_dictionary'
            )) 
        ]
        )
        inline_keyboard.append(
        [
           types.InlineKeyboardButton(text='⬇️Показать слова⬇️', callback_data=dictionaries_menu_cb.new(
                id_dictionary=id_dictionary,
                action='show_words_dictionary'
            )) 
        ]
        ) 
    keyboard = types.InlineKeyboardMarkup(
      inline_keyboard=inline_keyboard
    )
    return keyboard

def delete_dictionary_kb(id_dictionary):
    keyboard = types.InlineKeyboardMarkup(
      inline_keyboard=[
      [
        types.InlineKeyboardButton(text='Да, я уверен❗️', callback_data=delete_menu_cb.new(
            id_dictionary=id_dictionary,
            action='delete'
        )),
        types.InlineKeyboardButton(text='❗️Отменить❗️', callback_data=delete_menu_cb.new(
            id_dictionary=id_dictionary,
            action='cancel'
        )),
      ]
      ]
    )
    return keyboard