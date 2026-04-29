"""Guardrail construction for SDR flows."""

from dataclasses import dataclass

from agents import Agent, GuardrailFunctionOutput, Runner, input_guardrail
from pydantic import BaseModel

from sdr.prompts import NAME_GUARDRAIL_INSTRUCTIONS


class NameCheckOutput(BaseModel):
    is_name_in_message: bool
    name: str


@dataclass(frozen=True)
class GuardrailBundle:
    guardrail_agent: Agent
    guardrail: object


def build_name_guardrail() -> GuardrailBundle:
    guardrail_agent = Agent(
        name="Name check",
        instructions=NAME_GUARDRAIL_INSTRUCTIONS,
        output_type=NameCheckOutput,
        model="gpt-4o-mini",
    )

    @input_guardrail
    async def guardrail_against_name(ctx, agent, message):
        result = await Runner.run(guardrail_agent, message, context=ctx.context)
        is_name_in_message = result.final_output.is_name_in_message
        return GuardrailFunctionOutput(
            output_info={"found_name": result.final_output},
            tripwire_triggered=is_name_in_message,
        )

    return GuardrailBundle(
        guardrail_agent=guardrail_agent,
        guardrail=guardrail_against_name,
    )
