from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import crud_functions1

crud_functions1.initiate_db()
products = crud_functions1.get_all_products()


api = ""

bot = Bot(token=api)

dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
button3 = KeyboardButton(text='Купить')
kb.add(button1, button2, button3)

kb1 = InlineKeyboardMarkup()
button4 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button5 = InlineKeyboardButton(text='Формулы расчета', callback_data='formulas')
kb1.add(button4, button5)

kb2 = InlineKeyboardMarkup()
button6 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button7 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button8 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button9 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb2.add(button6, button7, button8, button9)


@dp.message_handler(commands=['start'])
async def start(message: MemoryStorage, state: FSMContext):
    await state.finish()
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=kb)


@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('Информация о боте!')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb1)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора:\n BMR = 10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(лет) - 161')
    await call.answer()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    norma_calories = 10 * float(data["weight"]) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161
    await message.answer(f"Ваша норма калорий: {norma_calories} ккал в день.")
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message, state):
    await state.finish()
    await message.answer("Привет! Я бот, помогающий твоему здоровью.", reply_markup=kb)


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for pr in products:
        await message.answer(f'Название: {pr[1]} | Описание: Описание {pr[2]} | Цена: {pr[3]}')
        with open(f"images (1).jpeg", "rb") as img:
            await message.answer_photo(img)
    await message.answer("Выберите продукт для покупки:", reply_markup=kb2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


@dp.message_handler()
async def all_messages(message: types.Message):
    await message.answer("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)