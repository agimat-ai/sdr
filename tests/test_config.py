import os
import unittest
from unittest.mock import patch

from sdr.config import load_settings


class ConfigTests(unittest.TestCase):
    def test_load_settings_raises_for_missing_required_env(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                load_settings(load_dotenv_file=False)

    def test_load_settings_reads_required_values(self) -> None:
        env = {
            "OPENAI_API_KEY": "o-key",
            "GOOGLE_API_KEY": "g-key",
            "DEEPSEEK_API_KEY": "d-key",
            "GROQ_API_KEY": "gr-key",
            "SENDGRID_API_KEY": "sg-key",
            "SENDER_EMAIL": "sender@example.com",
            "RECIPIENT_EMAIL": "recipient@example.com",
        }
        with patch.dict(os.environ, env, clear=True):
            settings = load_settings(load_dotenv_file=False)
        self.assertEqual(settings.openai_api_key, "o-key")
        self.assertEqual(settings.sender_email, "sender@example.com")
