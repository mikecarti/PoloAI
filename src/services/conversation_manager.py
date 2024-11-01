from langchain.memory import ConversationBufferMemory
from typing import Optional


class ConversationManager:
    TRUNCATE_HISTORY_LENGTH = 1000

    def __init__(self):
        self.memory = ConversationBufferMemory()

    def get_conversation_history(self) -> str:
        history = self.memory.load_memory_variables({})
        return f"History:\n{history['history']}"

    def save_interaction(self, question: str, answer: str) -> None:
        self.memory.save_context(
            inputs={"user": question}, outputs={"DimaPolo": answer}
        )

    def format_conversation(self, system_prompt: str, question: str, full_name: str) -> tuple[list[dict], str]:
        history = self.get_conversation_history()[-self.TRUNCATE_HISTORY_LENGTH :]
        # formatted_input = f"({full_name}): {question}"
        formatted_input = f"{question}"
        convo_with_question = f"{history}\n{formatted_input}"
        conversation = [
            {"role": "user", "parts": [{"text": system_prompt}]},
            {"role": "user", "parts": [{"text": convo_with_question}]},
        ]

        return conversation, formatted_input
