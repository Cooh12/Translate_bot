
from venv import create
from aiogram.dispatcher.filters.state import StatesGroup, State



class UserMessage(StatesGroup):

    create_dict = State()


class DictionariesState(StatesGroup):
    first_number  = State()
    last_number = State()
    rename_dictionary = State()
    new_name = State()
    studied_words = State()
    count_successful_attempt = State()
    
class WordsState(StatesGroup):
    words = State()
