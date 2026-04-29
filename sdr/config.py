"""Environment-backed runtime settings."""

from dataclasses import dataclass
import os
import warnings

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    google_api_key: str
    deepseek_api_key: str
    groq_api_key: str
    sendgrid_api_key: str
    sender_email: str
    recipient_email: str


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        warnings.warn(f"Missing required environment variable: {name}", stacklevel=2)
        return ""
    print(f"{name} is present")
    return value


def load_settings(load_dotenv_file: bool = True) -> Settings:
    if load_dotenv_file:
        load_dotenv(override=False)
    return Settings(
        openai_api_key=_require_env("OPENAI_API_KEY"),
        google_api_key=_require_env("GOOGLE_API_KEY"),
        deepseek_api_key=_require_env("DEEPSEEK_API_KEY"),
        groq_api_key=_require_env("GROQ_API_KEY"),
        sendgrid_api_key=_require_env("SENDGRID_API_KEY"),
        sender_email=os.getenv("SENDER_EMAIL", "<REPLACE WITH YOUR SENDER EMAIL>"),
        recipient_email=os.getenv("RECIPIENT_EMAIL", "<REPLACE WITH YOUR RECIPIENT EMAIL>"),
    )
