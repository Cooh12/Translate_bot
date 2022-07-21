import random
from datetime import datetime
from aiogram import types
from aiogram.dispatcher import FSMContext


from utils.db_api.quick_commands.commands_dict import (
    create_dictionary, 
    dictionary_date_update, 
    select_all_user_dictionaries, 
    change_dictname, 
    quantity_try_add, 
    successful_try_add
    )
from utils.db_api.quick_commands.commands_word import (
    delete_a_word, 
    attempt_add, 
    successful_attempt_add, 
    dictionary_words
    )
from keysboards.inline_kb_menu.inline_kb_menu_answer import (
    ikb_words_menu, 
    ikb_cancel_dictionary_editing,
    ikb_cancel_dictionary_creation, 
    ikb_cancel_the_study
    )

from utils.yandex_api.yandex_api import mess_user
from loader import dp
from states import message_states




@dp.message_handler(lambda message: message.text.startswith('/del'))
async def del_expense(message: types.Message):
    """Удаляет слово по её идентификатору"""
    row_id = int(message.text[4:])
    await delete_a_word(row_id)
    answer_message = "Успешно ✅"
    await message.answer(answer_message)


@dp.message_handler()
async def translate_text(message: types.Message, state : FSMContext):
    """Обработчик всех сообщений """
    translate_text = await mess_user(message.text)
    if translate_text[1] == 'en':
        await state.update_data(word_en=message.text)
        await state.update_data(word_ru=translate_text[0])
    if translate_text[1] == 'ru':
        await state.update_data(word_ru=message.text)
        await state.update_data(word_en=translate_text[0])
    await state.update_data(next_values=[0, 6])
    await message.answer(text=translate_text[0], reply_markup=ikb_words_menu)

@dp.message_handler(state=message_states.DictionariesState.rename_dictionary)
async def rename_dictionary(message : types.Message, state : FSMContext):
    """Ожидании ввода нового названия словаря"""
    states = await state.get_data()
    mutable_dictionary = states['dictionary']
    dictionaries = await select_all_user_dictionaries(message.from_user.id)
    list_dictionaries = [x.dictname for  x in dictionaries]
    if message.text.capitalize() in list_dictionaries:
        await message.answer(text='Такое назввние уже существует⚠️.\n Придумйте новое название.', reply_markup=ikb_cancel_dictionary_editing)
    else:
        await change_dictname(mutable_dictionary.id, message.text.capitalize())
        await message.answer(text=f"Имя словоря '{mutable_dictionary.dictname}' успешно изменено на '{message.text.capitalize()}'✅")
        await state.finish()

@dp.message_handler(state=message_states.UserMessage.create_dict)
async def name_dict(message: types.Message, state: FSMContext):
    """Ожидании ввода названия словаря"""
    dictionaries = await select_all_user_dictionaries(message.from_user.id)
    list_dictname = [x.dictname for  x in dictionaries]
    if str(message.text) in list_dictname:
        await message.answer(text=f"Словарь с таким именем уже существет.\nВведите новое название", reply_markup=ikb_cancel_dictionary_creation)
    else:
        await create_dictionary(message.from_user.id, message.text.capitalize())
        await message.answer(text=f'Словарь "{message.text}" успешно создан✅')
        await state.finish()

@dp.message_handler(state=message_states.DictionariesState.studied_words)
async def rename_dictionary(message : types.Message, state : FSMContext):
    states = await state.get_data()
    count_successful = states['count_successful_attempt']
    list_words = states['list_words']
    word = states['random_word']
    dictionary_id = states['dictionary_id']
    words = await dictionary_words(dictionary_id)
    if len(list_words) == 0:
        if word.word_en.capitalize() == message.text.capitalize():
            await successful_attempt_add(word.id)
            await attempt_add(word.id)
            await message.answer(text='Верно✅')
            count_successful+=1
            await state.update_data(count_successful_attempt=count_successful)
        else:
            await message.answer(text='Не верно😬')
            await attempt_add(word.id)
        await dictionary_date_update(dictionary_id, datetime.now())
        await quantity_try_add(dictionary_id)
        if count_successful/len(words) >= 0.72:
            await successful_try_add(dictionary_id)
        await state.finish()
        await message.answer(text=f"Заверешено 💫\n{count_successful} из {len(words)} переведены верно🙃")
    else:
        random_word = list_words[random.randrange(0, len(list_words))]
        list_words.remove(random_word)
        await state.update_data(list_words=list_words)
        await state.update_data(random_word=random_word)
        await attempt_add(word.id)
        if word.word_en.capitalize() == message.text.capitalize():
            await successful_attempt_add(word.id)
            count_successful+=1
            await state.update_data(count_successful_attempt=count_successful)
            await message.answer(text='Верно ✅', reply_markup=ikb_cancel_the_study)
        else:
            await message.answer(text='Не верно😬', reply_markup=ikb_cancel_the_study)
        await message.answer(text=f'{random_word.word_ru.capitalize()}')

    