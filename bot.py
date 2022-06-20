from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.storage import FSMContext
from states import States
import keyboards as kb
from config import token

# Instances
storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)
group_id = -1001697420883

# Start menu
@dp.message_handler(commands=['start'], state='*')
async def starter(message: types.Message):
    await message.answer('Hello,You can add a new order for approval',reply_markup=kb.addOrder)


@dp.callback_query_handler(lambda query: query.data == 'add', state='*')
async def add(query: types.CallbackQuery,state: FSMContext):
    chat_id = query.message.chat.id
    async with state.proxy() as data:
        data['chat_id'] = chat_id
    await query.message.answer('Send me a description of order')
    await States.sendPrice.set()


@dp.message_handler(state=States.sendPrice)
async def pricer(message: types.message,state: FSMContext):
    await bot.send_message(message.chat.id, 'Send me a price of order')
    description = message.text
    async with state.proxy() as data:
        data['description'] = description
    await States.done.set()

@dp.message_handler(state=States.done)
async def pricer(message: types.message,state: FSMContext):
    price = message.text
    async with state.proxy() as data:
        data['price'] = price
        description = data['description']
    await bot.send_message(message.chat.id, 'Very well. The order is seccesfully sent to workers.Waiting pls for their answer.',reply_markup=kb.addOrder)
    await bot.send_message(group_id, f'Description:\n{description}\n\nPrice:{price}$',disable_web_page_preview=True,reply_markup=kb.answers)


@dp.callback_query_handler(lambda query: query.data == 'accept', state='*')
async def accepter(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        description = data['description']
        chat_id = data['chat_id']
    await Bot.send_message(chat_id=chat_id,text=f'Order:{description}\n Has been accepted🥳.\nYou can Apply to order',disable_web_page_preview=True,self=bot)


@dp.callback_query_handler(lambda query: query.data == 'refuse', state='*')
async def refuser(query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        description = data['description']
        chat_id = data['chat_id']
    await Bot.send_message(chat_id=chat_id,text=f'Order:{description}\n Has been refused 😔.\nLook another order', disable_web_page_preview=True,self=bot)

executor.start_polling(dp, skip_updates=True)
