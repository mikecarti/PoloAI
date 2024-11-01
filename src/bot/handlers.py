from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums.chat_type import ChatType
from random import randint
from services.gemini_client import GeminiClient
from services.conversation_manager import ConversationManager
from typing import Optional
from legacy.prompt import DIMA_POLO_PROMPT

router = Router()
gemini_client = GeminiClient()
conversation_manager = ConversationManager()
ERROR_MSG = "Статус розыгрыша.........загрузка......89%............ катастрофически высокий шанс розыгрыша от Дима более чем на 50к"

@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(f"Здарова я Пурпурный AI, {message.from_user.full_name}!")

@router.message()
async def handle_message(message: Message) -> None:
    if not should_process_message(message):
        return

    answer = await generate_response(message.text)
    if answer:
        await message.answer(text=answer)

def should_process_message(message: Message) -> bool:
    if message.chat.type == ChatType.PRIVATE:
        return True
    return message.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP] and randint(0, 10) > 5

async def generate_response(text: str) -> Optional[str]:
    conversation = conversation_manager.format_conversation(DIMA_POLO_PROMPT, text)
    response = await gemini_client.generate_response(conversation)
    
    if response:
        last_answer = response.split("AI:")[-1].split("Дмитрий:")[-1]
        conversation_manager.save_interaction(text, last_answer)
        return last_answer
    return ERROR_MSG