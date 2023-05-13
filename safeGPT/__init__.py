import os
from .main import ChatCompletion
from .rule import OpenAIModeration

api_key = os.environ.get("OPENAI_API_KEY")