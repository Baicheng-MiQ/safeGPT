import os
from .main import ChatCompletion
from .rules import OpenAIModeration

api_key = os.environ.get("OPENAI_API_KEY")