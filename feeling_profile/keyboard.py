from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder



async def batton_sex():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="М🙎‍♂️",callback_data="male"))
    keyboard.add(InlineKeyboardButton(text="Ж🙍‍♀️",callback_data="female"))
    return keyboard.adjust(2).as_markup()


async def batton_search():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="М",callback_data="search_male"))
    keyboard.add(InlineKeyboardButton(text="Ж",callback_data="search_female"))
    return keyboard.adjust(2).as_markup()



menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Совпадения")],
    [KeyboardButton(text="Смотреть анкеты")],
    [KeyboardButton(text="Удалить")]
],resize_keyboard=True,input_field_placeholder="Выберите пункт меню")