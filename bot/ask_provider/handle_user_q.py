import asyncio

from aiogram.types import Message, CallbackQuery
from loader import dp, bot

from .provider import _providers, ask_provider


def remove_command(text):
    separated = text.split()
    separated.pop(0) if separated[0].startswith("/") else separated
    return " ".join(separated)


@dp.message_handler(commands=["bing"])
async def answer_bing(message: Message):
    await message.answer(await ask_provider(_providers["Bing"], remove_command(message.text)))


@dp.message_handler(commands=["gptgo"])
async def answer_gptgo(message: Message):
    await message.answer(await ask_provider(_providers["GptGo"], remove_command(message.text)))


@dp.message_handler(commands=["you"])
async def answer_you(message: Message):
    await message.answer(await ask_provider(_providers["You"], remove_command(message.text)))


@dp.message_handler(commands=["chatbase"])
async def answer_chatbase(message: Message):
    await message.answer(await ask_provider(_providers["ChatBase"], remove_command(message.text)))


@dp.message_handler(commands=["phind"])
async def answer_phind(message: Message):
    await message.answer(await ask_provider(_providers["Phind"], remove_command(message.text)))


@dp.message_handler(commands=["all"])
async def answer_all(message: Message):
    for provider_id in _providers.values():
        await message.answer(await ask_provider(provider_id, remove_command(message.text)))
