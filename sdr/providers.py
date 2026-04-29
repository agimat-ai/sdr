"""Model provider factories."""

from dataclasses import dataclass

from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

from sdr.config import Settings

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"


@dataclass(frozen=True)
class ModelRegistry:
    deepseek_model: OpenAIChatCompletionsModel
    gemini_model: OpenAIChatCompletionsModel
    llama_model: OpenAIChatCompletionsModel


def build_models(settings: Settings) -> ModelRegistry:
    deepseek_client = AsyncOpenAI(
        base_url=DEEPSEEK_BASE_URL, api_key=settings.deepseek_api_key
    )
    gemini_client = AsyncOpenAI(
        base_url=GEMINI_BASE_URL, api_key=settings.google_api_key
    )
    groq_client = AsyncOpenAI(base_url=GROQ_BASE_URL, api_key=settings.groq_api_key)

    return ModelRegistry(
        deepseek_model=OpenAIChatCompletionsModel(
            model="deepseek-chat", openai_client=deepseek_client
        ),
        gemini_model=OpenAIChatCompletionsModel(
            model="gemini-2.0-flash", openai_client=gemini_client
        ),
        llama_model=OpenAIChatCompletionsModel(
            model="llama-3.3-70b-versatile", openai_client=groq_client
        ),
    )
