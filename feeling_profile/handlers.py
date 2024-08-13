from aiogram import Router, filters
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from data_base.db_communicate import create_profile


from .keyboard import batton_sex, batton_search, menu

router = Router()


class Profile(StatesGroup):
    name = State()
    age = State()
    sex = State()
    search = State()
    search_age_start = State()
    search_age_finish = State()
    about_me = State()
    photo = State()



@router.message(filters.CommandStart())
async def start_work(message: Message, state: FSMContext):
    await message.answer("Привет. Давай заполним анкет")
    await state.set_state(Profile.name)
    await message.answer("Введите свое имя")


@router.message(Profile.name)
async def filling_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Profile.age)
    await message.answer("Сколько тебе лет")


@router.message(Profile.age)
async def filling_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число")
        return
    await state.update_data(age=message.text)
    await state.set_state(Profile.sex)
    await message.answer("Ваш пол",reply_markup=await batton_sex())


@router.callback_query(lambda call: call.data=="male" or call.data=="female")
async def filling_sex(callback_query: CallbackQuery , state: FSMContext):
    sex = 'М' if callback_query.data == 'male' else 'Ж'
    await state.update_data(sex=sex)
    await state.set_state(Profile.search)
    await callback_query.message.answer("Какие у вас интересы",reply_markup=await batton_search())


@router.callback_query(lambda call: call.data=="search_male" or call.data=="search_female")
async def filling_search(callback_query: CallbackQuery , state: FSMContext):
    search = 'М' if callback_query.data == 'search_male' else 'Ж'
    await state.update_data(search=search)
    await state.set_state(Profile.search_age_start)
    await callback_query.message.answer("Выбери возраст поиска от")


@router.message(Profile.search_age_start)
async def filling_search_age_start(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Введите число")
        return
    await state.update_data(search_age_start=message.text)
    await state.set_state(Profile.search_age_finish)
    await message.answer("Выбери возраст поиска до")


@router.message(Profile.search_age_finish)
async def filling_search_age_finish(message: Message, state: FSMContext):
    finish_age = message.text
    if not finish_age.isdigit():
        await message.answer("Введите число")
        return
    user_data = await state.get_data()
    start_age = user_data["search_age_start"]
    if int(start_age) > int(finish_age):
        await message.answer("начальный возраст поиска не может быть больше финального")
        return
    await state.update_data(search_age_finish=finish_age)
    await state.set_state(Profile.about_me)
    await message.answer("Раскажи о себе")


@router.message(Profile.about_me)
async def filling_about_me(message: Message, state: FSMContext):
    if len(message.text)>200:
        await message.answer("Введено больше 200 символов. Сократите текст")
        return
    await state.update_data(about_me=message.text)
    await state.set_state(Profile.photo)
    await message.answer("Добавь фото")


@router.message(Profile.photo)
async def filling_photo(message: Message, state: FSMContext):
    photo_user = message.photo[-1].file_id
    print(photo_user)
    user_id = message.from_user.id
    data_user = await state.get_data()
    print(data_user)
    await create_profile(user_id,data_user["name"],data_user["age"],data_user["sex"],
                         data_user["search"], data_user["search_age_start"], data_user["search_age_finish"],
                         data_user["about_me"],photo_user)
    await state.clear()
    await message.answer("Анкета заполнена",reply_markup=menu)


























