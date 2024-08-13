from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def profile_feedback(id_telegdam):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="👎",callback_data=f"dislike:{id_telegdam}"))
    keyboard.add(InlineKeyboardButton(text="👍",callback_data=f"like:{id_telegdam}"))
    return keyboard.adjust(2).as_markup()


