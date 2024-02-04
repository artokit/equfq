from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_markup(func):
    def wrapper(*args, **kwargs):
        keyboard = InlineKeyboardBuilder()
        func(keyboard, *args, **kwargs)
        return keyboard.as_markup()

    return wrapper


@create_markup
def start(keyboard: InlineKeyboardBuilder):
    keyboard.row(InlineKeyboardButton(text="TAYYORMAN🟢", callback_data="next"))


@create_markup
def get_signal(keyboard: InlineKeyboardBuilder):
    keyboard.row(InlineKeyboardButton(text="START🟢", callback_data='get_signal'))


@create_markup
def get_next_signals(keyboard: InlineKeyboardBuilder):
    keyboard.add(InlineKeyboardButton(text='Win💰', callback_data='get_signal'))
    keyboard.add(InlineKeyboardButton(text='Lose⛔️', callback_data='get_signal'))


@create_markup
def get_me(keyboard: InlineKeyboardBuilder):
    keyboard.row(InlineKeyboardButton(text='💬Help💬', url='https://t.me/farxod_x'))
