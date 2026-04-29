import unittest
from types import SimpleNamespace
from unittest.mock import patch

from sdr.agents.guardrails import NameCheckOutput, build_name_guardrail


class GuardrailTests(unittest.IsolatedAsyncioTestCase):
    async def test_guardrail_triggers_when_name_found(self) -> None:
        bundle = build_name_guardrail()
        ctx = SimpleNamespace(context={})
        fake_result = SimpleNamespace(
            final_output=NameCheckOutput(is_name_in_message=True, name="Alice")
        )

        with patch("sdr.agents.guardrails.Runner.run", return_value=fake_result):
            output = await bundle.guardrail.guardrail_function(
                ctx=ctx, agent=None, message="Email Alice"
            )

        self.assertTrue(output.tripwire_triggered)
        self.assertEqual(output.output_info["found_name"].name, "Alice")
