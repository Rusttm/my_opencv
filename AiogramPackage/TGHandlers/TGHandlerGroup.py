""" модерация группы в которой бот является админом"""

import logging

from aiogram import types, Router, F, Bot
from aiogram.filters import CommandStart, Command, or_f
from string import punctuation
from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType


user_group_router = Router()
user_group_router.message.filter(BOTFilterChatType(["group", "supergroup"]))

# restricted_words = {"идиот", "дурак", "хрень", "idiot"}


def clean_text(text: str):
    """ вырезает из текста знаки"""
    return text.translate(str.maketrans("", "", punctuation))


@user_group_router.message(Command("admin", ignore_case=True))
async def admin_cmd(message: types.Message, bot: Bot):
    """ this handler reloads group admins list"""
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id=chat_id)
    # print(f"{chat_id=}")
    bot.chat_group_admins_list = [member.user.id for member in admins_list if member.status in ["creator", "administrator"] ]
    logging.info(f"reloaded {bot.chat_group_admins_list=}")
    # if message.from_user.id in admins_list:
    await message.delete()

@user_group_router.edited_message()
@user_group_router.message()
async def cleaner(message: types.Message, bot: Bot):
    message_words_set = set(clean_text(message.text.lower()).split())
    restricted_set = set(bot.restricted_words)
    if restricted_set.intersection(message_words_set):
        await message.answer(f"{message.from_user.username}, соблюдайте порядок в чате!")
        await message.delete()
        # можно даже забанить
        # await message.chat.ban(message.from_user.id)
        # и потом восстановить
        # await message.chat.unban(message.from_user.id)

