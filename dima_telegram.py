import asyncio
import logging
import sys
from os import getenv
from train_polo import memory, ask_gemini

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from random import randint
from aiogram import types
from aiogram.enums.chat_type import ChatType

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "7616826614:AAGrOUsFDMJUU39pl9Lv79pclJlZ_1cV5-4"

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")


@dp.message()
async def message_handler(message: Message) -> None:
    if message.chat.type == ChatType.PRIVATE:
        print(f"Message received from {message.from_user.username}: {message.text}")
        await generate_answer(message)
    

@dp.message()
async def group_message_handler(message: Message) -> None:
    if message.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
        print(f"Message received in group from {message.from_user.id}: {message.text}")
        if randint(0, 10) > -1:
            await generate_answer(message)

async def generate_answer(message):
        polo_answer = ask_gemini(message.text)
        try:
            # Send a copy of the received message
            await message.answer(text=polo_answer)
        except TypeError as e:
            # But not all the types is supported to be copied so need to handle it
            await message.answer("Nice try!")
            print("Catched Telegram error: ", e)

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())