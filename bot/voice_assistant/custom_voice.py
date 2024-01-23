import os

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, el

from .state_add_custom_voice import AddingCustomVoice

adding_voice_sample_stop_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Завершити додання аудіофайлів", callback_data="stop_adding_voice")]
    ]
)


@dp.message_handler(commands="copy_voice", state="*")
async def add_custom_voice(message: Message):
    await message.answer(
        text="Для копіювання вашого голосу мені необхідна його назва та аудіофайл довжиною не "
             "менше 30 cекунд з записом голосу. Ви можете зачитати мені якусь статтю чи уривок з книги, "
             "щоб я міг оцінити вашу інтонацію, темп і тд. Знайдіть тихе місце, щоб ваш голос був чітким, виразним "
             "і не спотворювався фоновим шумом."
    )
    await message.answer(
        "Задайте назву для власного голосу, за цією назвою ви зможете потім розрізнити власний голос серед інших."
    )
    await AddingCustomVoice.voice_name.set()


@dp.message_handler(content_types=['text'], state=AddingCustomVoice.voice_name)
async def set_name_for_voice(message: Message, state: FSMContext):
    await state.update_data(voice_name=message.text)
    await state.update_data(voice_file=[])
    await message.answer("Надішліть аудіофайл.")
    await AddingCustomVoice.next()


@dp.message_handler(content_types=["audio", "voice"], state=AddingCustomVoice.voice_file)
async def add_audiofile(message: Message, state: FSMContext):
    audio = message.voice if message.voice else message.audio
    print(audio.values)
    if audio.values["duration"] < 30:
        await message.answer(
            "Тривалість вашого аудіозапису менша за 30 секунд, будь ласка, "
            "надішліть файл більшої довжини для найкращого результату"
        )
        return
    files_list = (await state.get_data())["voice_file"]
    file_name = "temp/" + str(message.from_user.id) + "_" + str(len(files_list)+1 if len(files_list) else 1) + ".mp4"
    files_list.append(file_name)
    await state.update_data(voice_file=files_list)
    await audio.download(destination_file=file_name)
    if len(files_list) == 23:
        await copy_voice(message, state)
        return
    await message.answer(
        "Ви можете надіслати ще аудіофайл, для підвищення якості копійованого голосу, "
        "або ж завершити додання прикладів вашого голосу",
        reply_markup=adding_voice_sample_stop_kb
    )


@dp.callback_query_handler(text_startswith="stop_adding_voice", state=AddingCustomVoice.voice_file)
async def copy_voice(call: CallbackQuery | Message, state: FSMContext):
    await AddingCustomVoice.next()
    files_list = (await state.get_data())["voice_file"]
    voice_name = (await state.get_data())["voice_name"]
    el.clone(
        name=voice_name,
        files=files_list
    )
    if type(call) is CallbackQuery:
        await call.message.answer("Ваш голос успішно скопійовано")
    else:
        await call.answer("Ваш голос успішно скопійовано")
    await state.finish()
    for file in files_list:
        os.remove(file)
