from aiogram.utils.callback_data import CallbackData
from requests import delete


dictionaries_cb = CallbackData('dictionaries_cb','id_dictionary', 'action')
dictionaries_more_cb =CallbackData('dictionaries_more_cb', 'action')
dictionaries_menu_cb = CallbackData('dictionaries_menu_cb','id_dictionary', 'action')
delete_menu_cb = CallbackData('delete_menu_cb', 'id_dictionary', 'action')


