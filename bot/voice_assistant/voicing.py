from loader import bot, dp, el
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

VOICE_KB_WIDTH = 4
VOICE_KB_HEIGHT = 3
VOICE_KB_BUTTONS_NUM = 12


def voice_keyboard(offset_start=0, offset_end=None, purpose="use_voice", voices=None):
    if voices is None:
        voices = el.voices()
    if offset_end is None:
        offset_end = offset_start + VOICE_KB_BUTTONS_NUM
    keyboard = []
    if offset_start != 0:
        keyboard.append([InlineKeyboardButton(text=f"Попередні голоси", callback_data=f'back:{offset_start}')])
    for row in range(VOICE_KB_HEIGHT):
        temp_row = []
        for voice in voices[offset_start:offset_start + VOICE_KB_WIDTH]:
            temp_row.append(
                InlineKeyboardButton(text=f"{voice.name}", callback_data=f'{purpose}:{voice.voice_id}:{voice.name}')
            )
        keyboard.append(temp_row)
        offset_start += VOICE_KB_WIDTH

    if offset_end < len(voices):
        keyboard.append([InlineKeyboardButton(text=f"Наступні голоси", callback_data=f'next:{offset_end}')])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@dp.message_handler(commands="to_voice")
async def text_to_voice(message: Message):
    if message.reply_to_message:
        await message.answer(
            f"Оберіть голос для озвучки вашого повідомлення: \n{message.reply_to_message.text}",
            reply_markup=voice_keyboard()
        )

@dp.message_handler(commands=["hi"])
async def hello(message: Message):
    pass

@dp.message_handler(commands="delete_voice")
async def show_delete_voice_keyboard(message: Message):
    custom_voices = [voice for voice in el.voices()[::-1] if voice.category == "cloned"]
    await message.answer(
        f"Оберіть голос який хочете видалити:",
        reply_markup=voice_keyboard(purpose="delete_voice", voices=custom_voices)
    )

@dp.callback_query_handler(text_startswith="back")
async def show_previous_voices(call: CallbackQuery):
    await call.answer()
    start = int(call.data.split(":")[1])
    purpose = call.message.reply_markup["inline_keyboard"][1][0]["callback_data"].split(":")[0]
    await call.message.edit_reply_markup(
        reply_markup=voice_keyboard(offset_start=start - VOICE_KB_BUTTONS_NUM, purpose=purpose)
    )


@dp.callback_query_handler(text_startswith="next")
async def show_next_voices(call: CallbackQuery):
    await call.answer()
    start = int(call.data.split(":")[1])
    purpose = call.message.reply_markup["inline_keyboard"][1][0]["callback_data"].split(":")[0]
    await call.message.edit_reply_markup(reply_markup=voice_keyboard(offset_start=start, purpose=purpose))


@dp.callback_query_handler(text_startswith="use_voice")
async def message_to_voice(call: CallbackQuery):
    await call.answer(text="Озвучую ваше повідомлення...")
    text_for_voice = call.message.text[call.message.text.index("\n") + 1:]
    voice_id, voice_name = call.data.split(":")[1:3]
    audio = el.generate(
        text=text_for_voice,
        voice=voice_id,
        model="eleven_multilingual_v2"
    )
    await call.message.answer_audio(audio, title=voice_name, reply=True)


@dp.callback_query_handler(text_startswith="delete_voice")
async def delete_voice(call: CallbackQuery):
    await call.answer(text="Голос видалено...")
    voice_id, voice_name = call.data.split(":")[1:3]
    first_button = call.message.reply_markup["inline_keyboard"][0][0]["callback_data"]
    start = int(first_button.split(":")[1] if first_button.split(":")[0] == "back" else 0)
    el.Voice(voice_id=voice_id).delete()
    custom_voices = [voice for voice in el.voices()[::-1] if voice.category == "cloned" and voice.voice_id != voice_id]
    await call.message.edit_reply_markup(
        reply_markup=voice_keyboard(offset_start=start, purpose="delete_voice", voices=custom_voices)
    )