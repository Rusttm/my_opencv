from aiogram.filters.callback_data import CallbackData


class TGMWCallbackData(CallbackData, prefix="rep"):
    """ tries to send data in class"""
    text: str
    url: str = str()
    description: str = "description not added"
    type: str = "test"
    data: dict = dict()
