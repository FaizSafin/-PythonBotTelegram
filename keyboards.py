from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton


reg_menu = InlineKeyboardMarkup()
reg_menu.add(InlineKeyboardButton(text='Registration',callback_data='reg'))