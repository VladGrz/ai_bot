import asyncio

from aiogram.types import Message, CallbackQuery
from loader import dp, bot

from .provider import _providers, ask_provider


@dp.message_handler(commands=["bing"])
async def answer_bing(message: Message):
    await message.answer(await ask_provider(_providers["Bing"], message.text[6:]))


@dp.message_handler(commands=["gptgo"])
async def answer_gptgo(message: Message):
    await message.answer(await ask_provider(_providers["GptGo"], message.text[7:]))


@dp.message_handler(commands=["you"])
async def answer_you(message: Message):
    await message.answer(await ask_provider(_providers["You"], message.text[5:]))


@dp.message_handler(commands=["chatbase"])
async def answer_chatbase(message: Message):
    await message.answer(await ask_provider(_providers["ChatBase"], message.text[10:]))


@dp.message_handler(commands=["phind"])
async def answer_phind(message: Message):
    await message.answer(await ask_provider(_providers["Phind"], message.text[7:]))


@dp.message_handler(commands=["liaobots"])
async def answer_liaobots(message: Message):
    await message.answer(await ask_provider(_providers["Liaobots"], message.text[10:]))


@dp.message_handler(commands=["all"])
async def answer_all(message: Message):
    results = [
        await message.answer(
            await ask_provider(provider_id, message.text[5:])
        ) for provider_id in _providers.values()
    ]
