import aiogram.types.chat
from aiogram.filters import Filter
from aiogram import types, Bot
import logging
from aiogram.methods.get_chat_administrators import GetChatAdministrators
import os


class BOTFilterChatType(Filter):

    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, message: types.Message) -> bool:
        return message.chat.type in self.chat_types


class BOTFilterAdminList(Filter):
    logger_name = f"{os.path.basename(__file__)}"
    _main_key = "bot_config"
    _fin_key = "admin_members"
    _config_dir_name = "config"
    _config_file_name = "bot_main_config.json"
    _module_config: dict = None

    def __init__(self):
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return message.from_user.id in bot.admins_list


class BOTFilterFinList(Filter):
    logger_name = f"{os.path.basename(__file__)}"
    _main_key = "bot_config"
    _fin_key = "fin_members"
    _config_dir_name = "config"
    _config_file_name = "bot_main_config.json"
    _module_config: dict = None

    def __init__(self):
        """ filter for financial group members"""
        from AiogramPackage.TGConnectors.BOTReadJsonAsync import BOTReadJsonAsync
        self.connector = BOTReadJsonAsync()

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        self._module_config = await self.connector.get_main_config_json_data_async(self._config_dir_name,
                                                                                   self._config_file_name)
        fin_members_dict = self._module_config.get(self._main_key).get(self._fin_key)
        bot.fins_list = list(fin_members_dict.values())

        return message.from_user.id in bot.fins_list


class BOTFilterIsGroupAdmin(Filter):
    def __init__(self):
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        """ filter doesn't work with private chats, only group chats"""
        return message.from_user.id in bot.chat_group_admins_list


if __name__ == "__main__":
    filter = BOTFilterFinList()
    print(filter._module_config)
