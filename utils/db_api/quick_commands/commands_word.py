from aiogram import types
from asyncpg import UniqueViolationError
from utils.db_api.schemas.words import Words
from utils.db_api.db_gino import db

async def add_to_word(user_id: int, dictname: str, word_en: str, word_ru:str, dict_id : int):
    try:
        words = Words(user_id=user_id, dictname=dictname, word_en=word_en, word_ru=word_ru, dict_id=dict_id)
        await words.create()
    except UniqueViolationError:
        print('Такой плользователь уже существует')


async def viewing_the_dictionary(user_id, dictname):

    words =await Words.query.where(
        Words.user_id == user_id
        ).where(
            Words.dictname == dictname
            ).gino.all()       
    return words



async def delete_a_word(word_id):
    word = await Words.query.where(
        Words.id == word_id
    ).gino.first()
    if word != None:
        await word.delete()


async def attempt_add(id):
    word = await  Words.query.where(Words.id == id).gino.first()
    new = word.attempt + 1
    await word.update(attempt=new).apply()
   

async def successful_attempt_add(id):
    word = await  Words.query.where(Words.id == id).gino.first()
    new = word.successful_attempt + 1
    await word.update(successful_attempt=new).apply()


async def dictionary_words(dict_id):
    words = await Words.query.where(Words.dict_id == dict_id).gino.all()
    return words 

