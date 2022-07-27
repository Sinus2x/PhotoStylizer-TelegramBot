import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

kb = types.InlineKeyboardMarkup(row_width=2)
kb.row(types.InlineKeyboardButton(text='Ок', callback_data='yes'),
       types.InlineKeyboardButton(text='Поменять фото', callback_data='change'))


class Dialog(StatesGroup):
    content_photo = State()
    style_photo = State()
    processing = State()


if __name__ == '__main__':
    from handlers import dp
    executor.start_polling(dp, skip_updates=True)
