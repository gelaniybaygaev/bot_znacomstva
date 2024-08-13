from aiogram import Router, filters, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from data_base.db_communicate import get_curent_profile
from .keyboard import profile_feedback
from data_base.db_communicate import send_like_ancet, send_dislike_ancet, acket_union_acket


router_show_profiles = Router()

async def show_anket(user_info):
    photo = user_info.photo
    name = user_info.name
    age = user_info.age
    about_me = user_info.about_me
    id_telegram_p = user_info.id_telegramm
    return (photo,name, age, about_me, id_telegram_p)







@router_show_profiles.message(F.text=="Смотреть анкеты")
async def show_filtr_anketu(message:Message, user_id = None):
    user_id = user_id or message.from_user.id
    anketa_get_needed = await get_curent_profile(user_id)
    print("user_id",user_id)
    if not anketa_get_needed:
        await message.answer("Новых анкет нет")
    else:
        photo,name, age, about_me, id_telegram_p = await show_anket(user_info=anketa_get_needed)
        await message.answer_photo(photo,caption=f"имя{name}, возраст{age}, инфомавция{about_me}",
                                   reply_markup=await profile_feedback(id_telegram_p))




@router_show_profiles.callback_query(F.data.startswith("like"))
async def like_ancet_and_next(callback:CallbackQuery, state:FSMContext):
    to_telegram_id = callback.data.split(":")[1]
    from_telegram_id = callback.from_user.id
    await send_like_ancet(from_telegram_id, to_telegram_id)
    await show_filtr_anketu(callback.message, from_telegram_id)


@router_show_profiles.callback_query(F.data.startswith("dislike"))
async def dislike_ancet_and_next(callback:CallbackQuery, state:FSMContext):
    to_telegram_id = callback.data.split(":")[1]
    from_telegram_id = callback.from_user.id
    await send_dislike_ancet(from_telegram_id, to_telegram_id)
    await show_filtr_anketu(callback.message, from_telegram_id)


@router_show_profiles.message(F.text=="Совпадения")
async def show_union_ancet(message:Message):
    from_telegram_id = message.from_user.id
    show_ancet = await acket_union_acket(from_telegram_id)
    photo, name, age, about_me, id_telegram_p = await show_anket(user_info=show_ancet)
    user_name = await message.bot.get_chat(id_telegram_p)
    await message.answer_photo(photo, caption=f"имя{name}, возраст{age}, инфомавция{about_me}, ссылка https://t.me/{user_name.username}")








































