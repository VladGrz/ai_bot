import asyncio

from aiogram.types import Message
from loader import dp


@dp.message_handler(commands=["start"])
async def start_message(message: Message):
    await message.answer(
        "Привіт! Я Mimicbot і я можу скопіювати твій голос😉. "
        "Крім того, я маю в наявності 44 готових голоса для озвучування ваших текстових повідомлень. "
        "Також я маю декілька провайдерів штучного інтелекту які допоможуть вам в вирішенні ваших питань."
        "\nНадішліть команду /help для детальної інформації"
    )


@dp.message_handler(commands=["help"])
async def help_message(message: Message):
    await message.answer(
        """
        Голосовий штучний інтелект:
        /to_voice - озвучити текстове повідомлення (Надішліть цю команду у відповідь на текстове повідомлення)
        /copy_voice - створити власний голос на основі аудіофайлу з голосом людини для подальшого озвучування текстових повідомлень
        /delete_voice - видалити власностворений голос
        Запитати про щось штучний інтелект: 
        /all - Запитати усіх наявних провайдерів
        /bing - Запитати пошукову систему Bing
        /gptgo - Запитати мовну модель GPT-Go
        /you - Запитати мовну модель You
        /chatbase - Запитати платформу для створення чат-ботів Chatbase про певну тему
        /phind - Запитати платформу для пошуку інформації Phind
        """
    )
