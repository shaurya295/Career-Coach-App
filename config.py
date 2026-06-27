import os
from dotenv import load_dotenv

# Load env variables from the root or current directory
load_dotenv()

# Ollama vs OpenAI config
USE_OLLAMA = os.getenv("USE_OLLAMA", "false").lower() in ("true", "1")

# Models configuration
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

OLLAMA_MODEL_NAME = os.getenv("OLLAMA_MODEL_NAME", "llama3.2")
OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
