from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


addOrder = InlineKeyboardMarkup()
addOrder.add(InlineKeyboardButton('Add new order', callback_data='add'))

answers = InlineKeyboardMarkup()
answers.add(InlineKeyboardButton('Accept',callback_data='accept'))
answers.add(InlineKeyboardButton('Refuse',callback_data='refuse'))


