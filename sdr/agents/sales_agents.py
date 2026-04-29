"""Sales and manager agent composition."""

from dataclasses import dataclass

from agents import Agent

from sdr.agents.guardrails import build_name_guardrail
from sdr.prompts import (
    EMAIL_MANAGER_INSTRUCTIONS,
    SALES_AGENT_INSTRUCTIONS,
    SALES_MANAGER_INSTRUCTIONS,
    SALES_TOOL_DESCRIPTION,
)
from sdr.providers import ModelRegistry
from sdr.tools.email_tools import build_email_manager_tools
from sdr.config import Settings


@dataclass(frozen=True)
class SalesAgentBundle:
    sales_manager: Agent
    careful_sales_manager: Agent


def build_sales_agent_bundle(settings: Settings, models: ModelRegistry) -> SalesAgentBundle:
    sales_agent1 = Agent(
        name="DeepSeek Sales Agent",
        instructions=SALES_AGENT_INSTRUCTIONS["deepseek"],
        model=models.deepseek_model,
    )
    sales_agent2 = Agent(
        name="Gemini Sales Agent",
        instructions=SALES_AGENT_INSTRUCTIONS["gemini"],
        model=models.gemini_model,
    )
    sales_agent3 = Agent(
        name="Llama3.3 Sales Agent",
        instructions=SALES_AGENT_INSTRUCTIONS["llama"],
        model=models.llama_model,
    )

    sales_tools = [
        sales_agent1.as_tool(
            tool_name="sales_agent1",
            tool_description=SALES_TOOL_DESCRIPTION,
        ),
        sales_agent2.as_tool(
            tool_name="sales_agent2",
            tool_description=SALES_TOOL_DESCRIPTION,
        ),
        sales_agent3.as_tool(
            tool_name="sales_agent3",
            tool_description=SALES_TOOL_DESCRIPTION,
        ),
    ]

    email_manager = Agent(
        name="Email Manager",
        instructions=EMAIL_MANAGER_INSTRUCTIONS,
        tools=build_email_manager_tools(settings),
        model="gpt-4o-mini",
        handoff_description="Convert an email to HTML and send it",
    )

    sales_manager = Agent(
        name="Sales Manager",
        instructions=SALES_MANAGER_INSTRUCTIONS,
        tools=sales_tools,
        handoffs=[email_manager],
        model="gpt-4o-mini",
    )

    guardrail_bundle = build_name_guardrail()
    careful_sales_manager = Agent(
        name="Sales Manager",
        instructions=SALES_MANAGER_INSTRUCTIONS,
        tools=sales_tools,
        handoffs=[email_manager],
        model="gpt-4o-mini",
        input_guardrails=[guardrail_bundle.guardrail],
    )

    return SalesAgentBundle(
        sales_manager=sales_manager,
        careful_sales_manager=careful_sales_manager,
    )
