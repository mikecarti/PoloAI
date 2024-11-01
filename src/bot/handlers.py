from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums.chat_type import ChatType
from random import randrange
from services.gemini_client import GeminiClient
from services.conversation_manager import ConversationManager
from typing import Optional
from legacy.prompt import DIMA_POLO_PROMPT

router = Router()
gemini_client = GeminiClient()
conversation_manager = ConversationManager()
ERROR_MSG = "Статус розыгрыша.........загрузка......89%............ катастрофически высокий шанс розыгрыша от Дима более чем на 50к"
RESPONSE_PROBABILITY = 0.3


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(f"Здарова я Пурпурный AI, {message.from_user.full_name}!")


@router.message()
async def handle_message(message: Message) -> None:
    print(f"\n[{message.from_user.username}] Message received: {message.text}")
    if not should_process_message(message):
        conversation_manager.save_interaction(message.text, "")
        return

    answer = await generate_response(message.text)
    if answer:
        await message.answer(text=answer)

    print(f"\n[{message.from_user.username}] Answer generated: {answer}")


def should_process_message(message: Message) -> bool:
    if message.chat.type == ChatType.PRIVATE:
        return True
    return (
        message.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]
        and randrange(0, 1, 0.1) <= RESPONSE_PROBABILITY
    )


async def generate_response(text: str) -> Optional[str]:
    conversation = conversation_manager.format_conversation(DIMA_POLO_PROMPT, text)

    print(f"\nSending conversation to Gemini: \n{conversation}")
    response = await gemini_client.generate_response(conversation)

    if response:
        last_answer = response.split("AI:")[-1].split("Дмитрий:")[-1]
        conversation_manager.save_interaction(text, last_answer)
        return last_answer
    return ERROR_MSG
