from langchain_openai import ChatOpenAI
from llm.base_provider import BaseProvider
from llm.settings import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, MODEL_NAME

from observability.logger import log_event


class DeepSeekProvider(BaseProvider):

    @staticmethod
    def get_llm():
        log_event("llm", "called")
        return ChatOpenAI(
            model=MODEL_NAME,
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
            temperature=0,
        )