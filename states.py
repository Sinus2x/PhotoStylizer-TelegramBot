from aiogram.dispatcher.filters.state import State, StatesGroup


class Dialog(StatesGroup):
    content_photo = State()
    style_photo = State()
    processing = State()