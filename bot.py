from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import reg_menu
from datas import start_db,add_to_db    

class Registration(StatesGroup):
    name = State()
    phone_num = State()

api_bot = '7402556361:AAE0MGcmCGuJdSGzjtcpiZidBBM5NBN1nLQ'
bot = Bot(token=api_bot)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def on_startup(_):
    await start_db()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer('Добро пожаловать! Это бот, интегрированный с сайтом kazcc.ru\nОставьте заявку', reply_markup=reg_menu)

@dp.callback_query_handler()
async def send_reg(call:types.CallbackQuery):
    data = call.data
    if data=='reg':
        await bot.send_message(
            chat_id=call.from_user.id,
            text='Новый пользователь\nНапишите нам свое имя!'
        )
        await Registration.name.set()
@dp.message_handler(state=Registration.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Спасибо! Теперь напишите нам ваш номер телефона.')
    await Registration.next()
@dp.message_handler(state=Registration.phone_num)
async def process_phone_num(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_num'] = message.text
    await message.answer(f'''Вы прошли регистрацию!
имя: {data['name']}
номер: {data['phone_num']}
    ''')
    await  add_to_db(
        name=data['name'],
        phone_num=data['phone_num'],
        )
    await state.finish()

if __name__=='__main__':
    executor.start_polling(dp,skip_updates=True,on_startup=on_startup)