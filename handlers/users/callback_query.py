import random
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp
from states import message_states
from utils.db_api.quick_commands.commands_word import add_to_word, dictionary_words, viewing_the_dictionary
from utils.db_api.quick_commands.commands_dict import (
    all_dict_kb,
    select_all_user_dictionaries, 
    select_dictionary, 
    dictionaries_menu_kb, 
    delete_dictionary_kb,
    delete_dictionary_command,
    )
from keysboards.inline_kb_menu.callback_dates import (
    dictionaries_cb, 
    dictionaries_menu_cb, 
    delete_menu_cb, 
    dictionaries_more_cb
    )
from keysboards.inline_kb_menu.inline_kb_menu_answer import ikb_cancel_dictionary_editing, ikb_cancel_the_study

@dp.callback_query_handler(text='to_word_dictionaries')
async def select_a_dictionary_before_adding_a_word(call : types.CallbackQuery, state : FSMContext):
    """Показывает  список словарей при добавлении слова в словарь """
    await call.message.delete()
    dictionaries = await select_all_user_dictionaries(call.message.chat.id)
    await call.message.answer(
        text=f'Выберите словарь (Всего - {len(dictionaries)})📚:',
        reply_markup=all_dict_kb(
            dictionaries,
            action='list_of_dictionaries_to_add',
            action_more='more_dictionaries_to_add'
            )
        )
    await call.answer()

@dp.callback_query_handler(dictionaries_more_cb.filter(action='more_dictionaries'))
async def select_a_dictionary(call : types.CallbackQuery, state : FSMContext):
    """Показывает еще список словарей при просморе всех словорей"""
    dictionaries = await select_all_user_dictionaries(call.message.chat.id)
    current_values = await state.get_data('next_values')
    new_values = [current_values['next_values'][0] + 6, current_values['next_values'][1] + 6]
    await state.update_data(next_values=new_values)
    await call.message.answer(
        text=f'Выберите словарь (Всего - {len(dictionaries)})📚:',
        reply_markup=all_dict_kb(
            dictionaries,
            initial_value = new_values[0],
            last_value = new_values[1],
            action='list_of_dictionaries',
            action_more='more_dictionaries'
            )
        )
    await call.answer()

@dp.callback_query_handler(dictionaries_more_cb.filter(action='remove_the_list'))
async def remove_the_list(call : types.CallbackQuery, state : FSMContext):
    """Убирает списко словарей"""
    await call.message.delete()
    await state.finish()
    await call.answer()



@dp.callback_query_handler(dictionaries_more_cb.filter(action='more_dictionaries_to_add'))
async def select_a_dictionary_to_add(call : types.CallbackQuery, state : FSMContext):
    """Показывает еще список словарей при добавлении слова в словарь"""
    dictionaries = await select_all_user_dictionaries(call.message.chat.id)
    current_values = await state.get_data('next_values')
    new_values = [current_values['next_values'][0] + 6, current_values['next_values'][1] + 6]
    await state.update_data(next_values=new_values)
    await call.message.answer(
        text=f'Выберите словарь (Всего - {len(dictionaries)})📚:',
        reply_markup=all_dict_kb(
            dictionaries,
            initial_value = new_values[0],
            last_value = new_values[1],
            action='list_of_dictionaries_to_add',
            action_more='more_dictionaries_to_add'
            )
        )
    await call.answer()

@dp.callback_query_handler(dictionaries_cb.filter(action='list_of_dictionaries'))
async def words_in_the_dictionary(call : types.CallbackQuery, callback_data: dict):
    """Показывает функционал словаря"""
    
    id_dictionary=int(callback_data['id_dictionary'])
    dictionary = await select_dictionary(id_dictionary)
    list_words = await viewing_the_dictionary(call.message.chat.id, dictionary.dictname)
    if len(list_words) == 0:
        mess = "Словарь пустой"
    else:
        mess = f"Количество слов: {len(list_words)}"
    answer_message = f"📖 '{dictionary.dictname}' - {mess}\n\n" + "\n"
    await call.message.answer(answer_message, reply_markup=dictionaries_menu_kb(id_dictionary, len(list_words)))
    await call.answer()

@dp.callback_query_handler(dictionaries_menu_cb.filter(action='show_words_dictionary'))
async def show_words_dictionary(call : types.CallbackQuery, callback_data: dict):
    await call.message.delete()
    """Показывает слова словоря"""
    id_dictionary=int(callback_data['id_dictionary'])
    dictionary = await select_dictionary(id_dictionary)
    list_words = await viewing_the_dictionary(call.message.chat.id, dictionary.dictname)
    list_words_row = [
        f'{word.word_ru.capitalize()} - {word.word_en.capitalize()}  /del{word.id} ⬅️ удалить'
        for word in list_words
    ]
    if len(list_words) != 0:
        await call.message.answer('\n'.join(list_words_row))
    else:
        await call.message.answer('Словарь пустой')
    await call.answer()

"""Удаляет словарь"""
@dp.callback_query_handler(dictionaries_menu_cb.filter(action='delete_dictionary'))
async def delete_dictionary(call : types.CallbackQuery, callback_data: dict):
    await call.message.delete()
    id_dictionary=int(callback_data['id_dictionary'])
    await call.message.answer('Вы точно хотите удалить словарь⁉️', reply_markup=delete_dictionary_kb(id_dictionary))  
    await call.answer()

@dp.callback_query_handler(delete_menu_cb.filter(action='delete'))
async def confirmation_deleting_the_dictionary(call : types.CallbackQuery, callback_data: dict):
    await call.message.delete()
    try:
        id_dictionary=int(callback_data['id_dictionary'])
        dictionary = await select_dictionary(id_dictionary)
        await delete_dictionary_command(id_dictionary)
        await call.message.answer(f'Словарь -{dictionary.dictname}- успешно удален✅')
        await call.answer()
    except AttributeError:
        await call.message.answer('Словарь уже удален❗️')
        await call.answer()

@dp.callback_query_handler(delete_menu_cb.filter(action='cancel'))
async def cancel_deleting_the_dictionary(call : types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('❗️Отменено❗️')

@dp.callback_query_handler(dictionaries_menu_cb.filter(action='change_the_dictionary_name'))
async def change_the_dictionary_name(call : types.CallbackQuery, callback_data: dict, state : FSMContext):
    """Изменяет название словоря"""
    await call.message.delete()
    try:
        id_dictionary=int(callback_data['id_dictionary'])
        dictionary = await select_dictionary(id_dictionary)
        await call.message.answer(f'Введите новое название словаря -{dictionary.dictname}-', reply_markup=ikb_cancel_dictionary_editing)
        await state.update_data(dictionary=dictionary)
        await message_states.DictionariesState.rename_dictionary.set()
        await call.answer()
    except AttributeError:
        await call.message.answer('Такого словаря уже нет❗️')
        await call.answer()
        await state.finish()

@dp.callback_query_handler(text='cancel_dictionary_editing', state=message_states.DictionariesState.rename_dictionary)
async def cancel_dictionary_editing_name(call : types.CallbackQuery, state: FSMContext):
    """Отменяет изменение словаря"""
    await call.message.delete()
    await call.message.answer('Отменено ✔️')
    await state.finish()
    await call.answer()


@dp.callback_query_handler(text='cancel_dictionary_creation', state=message_states.UserMessage.create_dict)
async def cancel_dictionary_creating_name(call : types.CallbackQuery, state: FSMContext):
    """Отменяет создание словоря"""
    await call.message.delete()
    await call.message.answer('Отменено ✔️')
    await state.finish()
    await call.answer()

@dp.callback_query_handler(text='cancel_the_study', state=message_states.DictionariesState.studied_words)
async def studied_words(call : types.CallbackQuery, state: FSMContext):
    """Отменяет изучение словоря"""
    await call.message.delete()
    await call.message.answer('Отменено ✔️')
    await state.finish()
    await call.answer()

@dp.callback_query_handler(dictionaries_menu_cb.filter(action='dictionary_statistics'))
async def dictionary_statistics(call : types.CallbackQuery, callback_data: dict, state : FSMContext):
    """Показывает статистику словаря"""
    await call.message.delete()
    id_dictionary=int(callback_data['id_dictionary'])
    dictionary = await select_dictionary(id_dictionary)
    words = await dictionary_words(id_dictionary)
    if dictionary.last_study == None:
        mess='не изучался'
    else:
        mess=dictionary.last_study.strftime("%d.%m.%Y")
    await call.message.answer(
        f'Количество слов - {len(words)}\n'
        f'Дата создания - {dictionary.created_at.strftime("%d.%m.%Y")} \n'
        f'Дата последнего изучения - {mess}\n'
        F'Количество изучений - {dictionary.quantity_try}\n'
        f'Упешных прохождений - {dictionary.successful_try}'
        )
    await call.answer()

@dp.callback_query_handler(dictionaries_menu_cb.filter(action='learn_words_dictionary'))
async def learn_words_dictionary(call : types.CallbackQuery, callback_data: dict, state : FSMContext):
    """Учить слова"""
    await call.message.delete()
    id_dictionary=int(callback_data['id_dictionary'])
    dictionary = await select_dictionary(id_dictionary)
    list_words = await viewing_the_dictionary(call.message.chat.id, dictionary.dictname)
    random_word = list_words[random.randrange(0, len(list_words))]
    list_words.remove(random_word)
    await state.update_data(list_words=list_words)
    await state.update_data(random_word=random_word)
    await state.update_data(dictionary_id=dictionary.id)
    await state.update_data(count_successful_attempt = 0)
    await message_states.DictionariesState.studied_words.set()
    await call.message.answer(f'{random_word.word_ru.capitalize()}', reply_markup=ikb_cancel_the_study)

@dp.callback_query_handler(dictionaries_cb.filter(action='list_of_dictionaries_to_add'))
async def adding_a_word_to_a_dictionary(call : types.CallbackQuery, callback_data: dict, state : FSMContext):
    """Добавляет слово в словарь"""
    id_dictionary=int(callback_data['id_dictionary'])
    dictionary = await select_dictionary(id_dictionary)
    words = await state.get_data('word_ru')
    list_words = await viewing_the_dictionary(call.message.chat.id, dictionary.dictname)
    check_words = [x.word_en for x in list_words]
    if  words['word_en'] in check_words:
        await call.answer(text='Такое слово уже существует в этом словаре.') 
    else:
        await add_to_word(
            call.message.chat.id,
            dictionary.dictname,
            words['word_en'],
            words['word_ru'],
            dictionary.id
        )
        await call.answer(text=f'Слово успешно добавленео в словарь -{dictionary.dictname}-✅')
        await call.answer()
        await call.message.delete()
