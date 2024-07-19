import logging
import os

import aiofiles
import aiogram.exceptions
from aiogram import types, Router, F, Bot, html
from aiogram.filters import CommandStart, Command, or_f, StateFilter
from aiogram.filters.callback_data import CallbackQueryFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.utils.markdown import hbold
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from aiogram.utils.formatting import as_list, as_marked_section, Bold

from AiogramPackage.TGFilters.BOTFilter import BOTFilterChatType
# from AiogramPackage.TGKeyboards import TGKeybReplyMarkup as my_reply_kb
from AiogramPackage.TGKeyboards.TGKeybReplyBuilder import reply_kb_lvl1, reply_kb_lvl2, del_kb
from AiogramPackage.TGKeyboards.TGKeybReplyList import make_row_keyboard
from AiogramPackage.TGKeyboards.TGKeybInline import get_callback_btns, get_url_btns, get_mixed_btns
from AiogramPackage.TGAlchemy.TGModelProd import TGModelProd
from AiogramPackage.TGAlchemy.TGModelStock import get_stock_row

_static_dir = "data_static"
_instrument_img = "instrument_img.jpg"
_spares_img = "spares_img.jpg"

user_router = Router()
user_router.message.filter(BOTFilterChatType(["private"]))


@user_router.message(CommandStart())
@user_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
@user_router.message(F.text.lower() == "start")
async def start_cmd(message: types.Message):
    # version1
    # await message.answer(f"{message.from_user.first_name}, welcome to bot!", reply_markup=my_reply_kb.my_reply_kb)
    # version2
    await message.answer(f"Здравствуйте, {hbold(message.from_user.first_name)}, добро пожаловать в наш 🥸бот",
                         reply_markup=reply_kb_lvl1.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует"
                         ))
    # version 3
    # await message.answer(f"{message.from_user.first_name}, welcome to bot!",
    #                      reply_markup=my_bld_kb.get_my_kb(
    #                          "Меню",
    #                          "О боте",
    #                          "Реквизиты Компании",
    #                          "Платежные реквизиты",
    #                          placeholder="Выберите пункт меню",
    #                          sizes=(2, 2)
    #                      )
    #                      )


@user_router.message(Command("hide_menu", ignore_case=True))
async def menu_cmd(message: types.Message):
    # ver1
    await message.answer(f"{message.from_user.first_name}, can't hide main menu!", reply_markup=del_kb)


@user_router.message(or_f(Command("menu", "men", ignore_case=True), (F.text.lower().contains("меню"))))
async def menu_cmd(message: types.Message):
    # ver1
    # await message.answer(f"{message.from_user.first_name}, welcome to main menu!", reply_markup=my_reply_kb.del_kb)
    await message.answer(f"{html.quote(message.from_user.first_name)}, welcome to main menu!", reply_markup=reply_kb_lvl1)


@user_router.message(Command("catalogue", ignore_case=True))
@user_router.message((F.text.lower().contains("каталог")) | (F.text.lower().contains("catalogue")))
async def menu_cmd(message: types.Message):
    await message.answer(f"{hbold(message.from_user.first_name)}, welcome to <b>Catalogue</b>",
                         reply_markup=reply_kb_lvl2.as_markup(
                             resize_keyboard=True,
                             input_field_placeholder="Что Вас интересует?"
                         ))


@user_router.message(F.text.lower().contains("реквизиты"))
async def company_info_cmd(message: types.Message):
    msg = str('<b>Наименование:</b> Акционерное общество «Серман»\n'
              '<b>Адрес:</b> 125504, г. Москва, Дмитровское шоссе, д. 71Б, этаж 5, комната 7)\n'
              '<b>ИНН / КПП:</b> 7743275417 / 774301001\n'
              '<b>ОГРН/ОКПО:</b> 1187746831007/33241658\n'
              '<b>БИК Банка:</b> 044525593\n'
              '<b>Наименование банка:</b> АО "АЛЬФА-БАНК"\n'
              '<b>Корреспондентский счет:</b> 30101810200000000593\n'
              '<b>Расчетный счет:</b> 40702810801300031452\n'
              '<b>Телефон:</b> +8 495 909 8033')
    await message.answer(f"Здравствуйте, {hbold(html.quote(message.from_user.first_name))}, реквизиты нашей Копании:\n{msg}")


class FindInstrument(StatesGroup):
    brand = State()
    model = State()


class FindSpare(StatesGroup):
    brand = State()
    code = State()


available_instrument_brands = []
available_instrument_models = ["812", "CN70"]
add_btn = ["Отмена"]


@user_router.message(StateFilter('*'), Command("cancel", ignore_case=True))
@user_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_find_instrument(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(f"Ввод ❌<b>Отменен</b>", reply_markup=
    reply_kb_lvl2.as_markup(resize_keyboard=True, input_field_placeholder="Что Вас интересует?"))


@user_router.message(StateFilter(None), F.text == "Инструмент")
async def find_brand_instrument(message: types.Message, state: FSMContext, bot: Bot):
    available_instrument_brands = bot.filters_dict.get("instrument_brands_list", ["MEITE", "BLOCK"])
    kb_lines = [add_btn, available_instrument_brands]
    await message.answer(f"Введите <b>Марку</b> 🔨инструмента (или '.')", reply_markup=make_row_keyboard(kb_lines))
    await state.set_state(FindInstrument.brand)


# @user_router.message(FindInstrument.brand, F.text.in_(available_instrument_brands))
@user_router.message(FindInstrument.brand)
async def find_model_instrument(message: types.Message, state: FSMContext, bot: Bot):
    """ after press brand """
    available_instrument_models = bot.filters_dict.get("instrument_models_list", ["8016", "851", "CN"])
    kb_lines = [add_btn, available_instrument_models]
    await state.update_data(brand=message.text)
    await message.answer(f"Введите <b>Модель</b> 🔨инструмента (или '.')", reply_markup=make_row_keyboard(kb_lines))
    await state.set_state(FindInstrument.model)


@user_router.message(FindInstrument.model)
async def find_instrument(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    """ after press model"""
    await state.update_data(model=message.text)
    await message.answer(f"<b>Поиск</b> 🔨инструмента", reply_markup=reply_kb_lvl2.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Введите комманду"
    ))
    try:
        data = await state.get_data()
        brand = data.get("brand")
        model = data.get("model")
        statement = select(TGModelProd).filter(TGModelProd.pathName.contains("Инструмент"))
        if brand != ".":
            statement = statement.filter(TGModelProd.pathName.contains(brand))
        if model != ".":
            statement = statement.filter(TGModelProd.name.contains(model))
        result = await session.execute(statement)
        obj_list = result.scalars().all()
        if obj_list:
            for prod_obj in obj_list:
                url = "https://sermangroup.ru"
                photo = None
                try:
                    prod_attrs = prod_obj.attributes
                    for attr in prod_attrs:
                        attr_name = attr.get("name")
                        if attr_name == "Ссылка на товар на сайте магазина":
                            url = attr.get("value")
                        elif attr_name == "Ссылка на фото товара":
                            photo = attr.get("value")
                except Exception as e:

                    logging.warning(f"cannot get attributes from prod, error {e}")
                stock_sum = "Недоступно"
                try:
                    prod_id = prod_obj.id
                    # print(f"{prod_id=}")
                    stock = await get_stock_row(prod_id)
                    stock_sum = stock.stock
                except Exception as e:
                    logging.warning(f"cannot get stock sum from stock, error {e}")
                up_cur_file_path = os.path.dirname(os.path.dirname(__file__))
                static_file = os.path.join(up_cur_file_path, _static_dir, _instrument_img)
                async with aiofiles.open(static_file, "rb") as plot_img:
                    # print(f"{len(prod_obj.id)=} and {len(prod_obj.meta.get('href'))=}")
                    if not photo:
                        photo = BufferedInputFile(file=await plot_img.read(), filename="Инструмент")
                    # try to send photo
                    try:
                        await bot.send_photo(chat_id=message.chat.id,
                                             photo=photo,
                                             caption=f"🔨Инструмент {prod_obj.name}\n"
                                                     f"🫙На складе: {stock_sum}",
                                             reply_markup=get_mixed_btns(btns={
                                                 "Перейти": url,
                                                 "Подробнее": f"get_prod_info_{prod_obj.id}"
                                             }))
                    except aiogram.exceptions.TelegramBadRequest:
                        # sometime photo href doesnt work
                        # await message.answer(f"Не могу найти фото {url} для 🔨Инструмента {str(data)}!")
                        try:
                            photo = BufferedInputFile(file=await plot_img.read(), filename="Инструмент")
                            await bot.send_photo(chat_id=message.chat.id,
                                                 photo=photo,
                                                 caption=f"🔨Инструмент {prod_obj.name}\n"
                                                         f"🫙На складе: {stock_sum}",
                                                 reply_markup=get_mixed_btns(btns={
                                                     "Перейти": url,
                                                     "Подробнее": f"get_prod_info_{prod_obj.id}"
                                                 }))
                        except Exception as e:
                            msg = f"Cant find correct photo for spare part, error {e}"
                            print(msg)
        else:
            await message.answer(f"🔨Инструмент {str(data)} не обнаружен!")
    except Exception as e:
        logging.warning(f"cannot get attributes from prod, error {e}")
    await state.clear()


"""  Запчасти """


@user_router.message(StateFilter(None), F.text.lower() == "запчасти")
async def find_brand_spare(message: types.Message, state: FSMContext, bot: Bot):
    available_spares_brands = bot.filters_dict.get("spares_brands_list", ["Meite", "Block"])
    kb_lines = [add_btn, available_spares_brands]
    await message.answer(f"Введите <b>производителя</b> для поиска 🔩запчасти (или '.')",
                         reply_markup=make_row_keyboard(kb_lines))
    await state.set_state(FindSpare.brand)


@user_router.message(FindSpare.brand)
async def find_model_spare(message: types.Message, state: FSMContext, bot: Bot):
    available_spares_codes = bot.filters_dict.get("spare_codes_list", ["8016", "851", "CN"])
    kb_lines = [add_btn, available_spares_codes]
    await state.update_data(brand=message.text)
    await message.answer(f"Введите <b>код</b> 🔩запчасти",
                         reply_markup=make_row_keyboard(kb_lines),
                         input_field_placeholder="Enter a code")
    await state.set_state(FindSpare.code)


@user_router.message(FindSpare.code)
async def find_spare(message: types.Message, state: FSMContext, session: AsyncSession, bot: Bot):
    await state.update_data(code=message.text)
    await message.answer(f"<b>Поиск</b> 🔨инструмента", reply_markup=reply_kb_lvl2.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Введите новый запрос"
    ))
    try:
        data = await state.get_data()
        brand = data.get("brand")
        code = data.get("code")
        statement0 = select(TGModelProd).filter(TGModelProd.pathName.contains("Запасные"))
        if brand == ".":
            statement = statement0.filter(TGModelProd.name.contains(code))
        else:
            statement = statement0.filter(TGModelProd.pathName.contains(brand)).filter(TGModelProd.name.contains(code))
        result = await session.execute(statement)
        obj_list = result.scalars().all()
        if obj_list:
            for prod_obj in obj_list:
                url = "https://sermangroup.ru"
                photo = None
                try:
                    prod_attrs = prod_obj.attributes
                    for attr in prod_attrs:
                        attr_name = attr.get("name")
                        if attr_name == "Ссылка на товар на сайте магазина":
                            url = attr.get("value")
                        elif attr_name == "Ссылка на фото товара":
                            photo = attr.get("value")
                except Exception as e:
                    logging.warning(f"cannot get attributes from prod, error {e}")
                try:
                    prod_id = prod_obj.id
                    print(f"{prod_id=}")
                    stock = await get_stock_row(prod_id)
                    stock_sum = stock.stock
                except Exception as e:
                    logging.warning(f"cannot get stock sum from stock, error {e}")
                up_cur_file_path = os.path.dirname(os.path.dirname(__file__))
                static_file = os.path.join(up_cur_file_path, _static_dir, _spares_img)
                async with aiofiles.open(static_file, "rb") as plot_img:
                    # print(f"{len(prod_obj.id)=} and {len(prod_obj.meta.get('href'))=}")
                    if not photo:
                        photo = BufferedInputFile(file=await plot_img.read(), filename="Запчасть")
                    try:
                        await bot.send_photo(chat_id=message.chat.id,
                                             photo=photo,
                                             caption=f"🔩Запчасти {prod_obj.name}\n"
                                                     f"🫙На складе: {stock_sum}",
                                             reply_markup=get_mixed_btns(btns={
                                                 "Перейти": url,
                                                 "Подробнее": f"get_prod_info_{prod_obj.id}"
                                             }))
                    except aiogram.exceptions.TelegramBadRequest:
                        try:
                            photo = BufferedInputFile(file=await plot_img.read(), filename="Инструмент")
                            await bot.send_photo(chat_id=message.chat.id,
                                                 photo=photo,
                                                 caption=f"🔨Инструмент {prod_obj.name}\n"
                                                         f"🫙На складе: {stock_sum}",
                                                 reply_markup=get_mixed_btns(btns={
                                                     "Перейти": url,
                                                     "Подробнее": f"get_prod_info_{prod_obj.id}"
                                                 }))
                        except Exception as e:
                            print(e)

        else:
            await message.answer(f"🔩Запчастей: {str(data)} не обнаружено!")
    except Exception as e:
        logging.warning(f"cannot establish connection, error {e}")
        await message.answer(f"Ваш запрос 🔩запчастей: не обработан:\n Ошибка доступа к базе. Попробуйте запросить еще раз")
    await state.clear()

# @user_router.message(FindInstrument.model, F.text.lower() != "отмена")
# async def wrong_model_instrument(message: types.Message):
#     kb_lines = [add_btn, available_instrument_models]
#     await message.answer(f"Введена неверная модель! Введите <b>Модель</b> инструмента",
#                          reply_markup=make_row_keyboard(kb_lines))


# @user_router.message(StateFilter('*'), Command("back", ignore_case=True))
# @user_router.message(StateFilter('*'), F.text.casefold() == "назад")
# async def cancel_find_instrument(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state == FindInstrument.brand:
#         await message.answer(f"предыдущего шага нет, нажмите кнопку Отмена")
#         return
#     prev = None
#     for step in FindInstrument.__all_states__:
#         if step.state == current_state:
#             await state.set_state(prev)
#             await message.answer(f"<b>Возврат</b> к прошлому шагу")
#             return
#         prev = step
