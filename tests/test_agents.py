import unittest

from sdr.agents.sales_agents import build_sales_agent_bundle
from sdr.config import Settings
from sdr.providers import build_models


class AgentAssemblyTests(unittest.TestCase):
    def test_build_sales_agent_bundle_contains_graph(self) -> None:
        settings = Settings(
            openai_api_key="o-key",
            google_api_key="g-key",
            deepseek_api_key="d-key",
            groq_api_key="gr-key",
            sendgrid_api_key="sg-key",
            sender_email="sender@example.com",
            recipient_email="recipient@example.com",
        )
        models = build_models(settings)
        bundle = build_sales_agent_bundle(settings, models)

        self.assertEqual(bundle.sales_manager.name, "Sales Manager")
        self.assertEqual(bundle.careful_sales_manager.name, "Sales Manager")
        self.assertEqual(len(bundle.sales_manager.tools), 3)
        self.assertEqual(len(bundle.sales_manager.handoffs), 1)
        self.assertEqual(len(bundle.careful_sales_manager.input_guardrails), 1)
