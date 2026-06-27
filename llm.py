# pyrefly: ignore [missing-import]
from langchain_openai import ChatOpenAI
# pyrefly: ignore [missing-import]
from langchain_ollama import ChatOllama
import config

def get_llm():
    if config.USE_OLLAMA:
        return ChatOllama(
            model=config.OLLAMA_MODEL_NAME,
            base_url=config.OLLAMA_API_BASE
        )
    else:
        return ChatOpenAI(
            model=config.OPENAI_MODEL_NAME,
            openai_api_base=config.OPENAI_API_BASE
        )
