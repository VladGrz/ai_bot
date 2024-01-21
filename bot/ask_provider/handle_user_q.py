from aiogram.types import Message, CallbackQuery
from loader import dp, bot


@dp.message_handler(commands=["bing"])
async def answer_bing(message: Message):
    await message.answer("This is Bing")


@dp.message_handler(commands=["gptgo"])
async def answer_bing(message: Message):
    await message.answer("This is gptgo")


@dp.message_handler(commands=["you"])
async def answer_bing(message: Message):
    await message.answer("This is you")


@dp.message_handler(commands=["chatbase"])
async def answer_bing(message: Message):
    await message.answer("This is chatbase")


@dp.message_handler(commands=["phind"])
async def answer_bing(message: Message):
    await message.answer("This is phind")


@dp.message_handler(commands=["liaobots"])
async def answer_bing(message: Message):
    await message.answer("This is liaobots")
