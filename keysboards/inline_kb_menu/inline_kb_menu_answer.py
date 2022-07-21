from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



ikb_words_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Добавить слово📘', callback_data='to_word_dictionaries')
        ]
    ]
)

ikb_cancel_dictionary_creation = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отменить создание ❌', callback_data='cancel_dictionary_creation')
        ]
    ]
)

ikb_cancel_dictionary_editing = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Отменить удаление ❌', callback_data='cancel_dictionary_editing')
        ]
    ]
)

ikb_cancel_the_study = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Прекратить изучение ❌', callback_data='cancel_the_study')
        ]
    ]
)