from aiogram import executor

from bot import dp, bot


async def hello(x):
    await bot.send_message(559346363, "Hello!")

if __name__ == '__main__':
    # Starting bot
    executor.start_polling(dp, skip_updates=True, on_startup=hello)