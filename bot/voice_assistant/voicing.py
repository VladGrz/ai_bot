from loader import bot, dp, el
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

VOICE_KB_WIDTH = 4
VOICE_KB_HEIGHT = 3
VOICE_KB_BUTTONS_NUM = 12


def voice_keyboard(offset_start=0, offset_end=None):
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
                InlineKeyboardButton(text=f"{voice.name}", callback_data=f'use_voice:{voice.voice_id}:{voice.name}')
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


@dp.callback_query_handler(text_startswith="back")
async def show_previous_voices(call: CallbackQuery):
    start = int(call.data.split(":")[1])
    await call.message.edit_reply_markup(reply_markup=voice_keyboard(offset_start=start - VOICE_KB_BUTTONS_NUM))


@dp.callback_query_handler(text_startswith="next")
async def show_next_voices(call: CallbackQuery):
    start = int(call.data.split(":")[1])
    await call.message.edit_reply_markup(reply_markup=voice_keyboard(offset_start=start))


@dp.callback_query_handler(text_startswith="use_voice")
async def messahe_to_voice(call: CallbackQuery):
    await call.answer(text="Озвучую ваше повідомлення...")
    text_for_voice = call.message.text[call.message.text.index("\n") + 1:]
    voice_id, voice_name = call.data.split(":")[1:3]
    audio = el.generate(
        text=text_for_voice,
        voice=voice_id,
        model="eleven_multilingual_v2"
    )
    await call.message.answer_audio(audio, title=voice_name, reply=True)
