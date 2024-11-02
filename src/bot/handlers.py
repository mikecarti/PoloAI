import asyncio
from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums.chat_type import ChatType
from aiogram.enums.chat_action import ChatAction
from aiogram.utils.chat_action import ChatActionSender
from aiogram.methods.send_chat_action import SendChatAction
from random import randint
from services.gemini_client import GeminiClient
from services.conversation_manager import ConversationManager
from typing import Optional
from legacy.prompt import DIMA_POLO_PROMPT

router = Router()
gemini_client = GeminiClient()
conversation_manager = ConversationManager()
# ERROR_MSG = "Статус розыгрыша.........загрузка......89%............ катастрофически высокий шанс розыгрыша от Дима более чем на 50к"
ERROR_MSG = "Дима сейчас срет наберите позже. Бабки в обороте. Накрутка имеет 🤏🤏🤏."
RESPONSE_PROBABILITY = 0.45


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(f"Здарова я Пурпурный AI, {message.from_user.full_name}!")


@router.message()
async def handle_message(message: Message, bot: Bot) -> None:
    print(f"\n[{message.from_user.username}] Message received: {message.text}")
    if not should_process_message(message):
        conversation_manager.save_interaction(message.text, "")
        return

    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(1)
        answer = await generate_response(message)
        if answer:
            await message.answer(text=answer)

    print(f"\n[{message.from_user.username}] Answer generated: {answer}")


def should_process_message(message: Message) -> bool:
    if message.chat.type == ChatType.PRIVATE:
        return True
    return (
        message.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]
        and randint(0, 9) <= RESPONSE_PROBABILITY * 10
    )


async def generate_response(message: Message) -> Optional[str]:
    conversation, formatted_input = conversation_manager.format_conversation(
        DIMA_POLO_PROMPT, message.text, message.from_user.full_name
    )

    print(f"\nSending conversation to Gemini: \n{conversation}")
    response = await gemini_client.generate_response(conversation)

    if response:
        last_answer = response.split("AI:")[-1].split("Дмитрий:")[-1]
        last_answer = last_answer.replace("  ", " ")
        conversation_manager.save_interaction(formatted_input, last_answer)
        return last_answer
    return ERROR_MSG
