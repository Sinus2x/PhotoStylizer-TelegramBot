from main import bot, dp
from .model import StyleTransformer
from aiogram.types import Message, ContentType


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    greeting = "Привет. Это бот для стилизации изображений.\nОтправь *два* изображения:" \
               "\n1) Изображение, *на которое хочешь перенести стиль*" \
               "\n2) Изображение, *содержащее желаемый стиль*."
    await message.answer(greeting, parse_mode='markdown')


# @dp.message_handler()
# async def transfer(msg: Message):
#     await bot.send_message(msg.from_user.id, 'не старт и не хелп')


@dp.message_handler(content_types=ContentType.PHOTO)
async def transfer(msg: Message):
    await msg.reply('photo')


