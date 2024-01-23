from aiogram.dispatcher.filters.state import StatesGroup, State


class AddingCustomVoice(StatesGroup):
    voice_name = State()
    voice_file = State()
    copy_voice = State()
