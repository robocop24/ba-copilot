from langchain_openai import ChatOpenAI
from llm.base_provider import BaseProvider
from llm.settings import (DEEPSEEK_API_KEY,DEEPSEEK_BASE_URL,MODEL_NAME)

class DeepSeekProvider(BaseProvider):
            
    @staticmethod
    def get_llm():
        return ChatOpenAI(
            model=MODEL_NAME,
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
            temperature=0,
            model_kwargs={"response_format": {"type": "json_object"}}   # ← JSON mode
        )