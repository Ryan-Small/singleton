import json
import logging
from typing import List

from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from langchain.schema import HumanMessage
from langchain.chat_models import ChatOpenAI


logger = logging.getLogger(__name__)


class AI:

    def __init__(self, openai_token):
        llm = ChatOpenAI(openai_api_key=openai_token, model_name='gpt-4')
        memory = ConversationSummaryBufferMemory(llm=llm)
        for msg in self._get_system_messages():
            memory.save_context({"input": f"It is critical to remember that {msg}."}, {"output": "acknowledged"})

        self.chat = ConversationChain(llm=llm, memory=memory, verbose=True)

    @staticmethod
    def _get_system_messages() -> List[str]:
        with open("./config.json", "r") as f:
            config = json.load(f)
            return config['SYSTEM_MESSAGES']

    def handle_message(self, message: str) -> str:
        response = self.chat.invoke([HumanMessage(content=message)])
        return response.get('response', '')
