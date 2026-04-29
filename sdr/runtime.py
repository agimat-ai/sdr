"""Runtime orchestration for SDR campaign execution."""

from agents import Runner, trace

from sdr.agents.sales_agents import build_sales_agent_bundle
from sdr.config import load_settings
from sdr.providers import build_models


async def run_campaign(message: str, protected: bool = True) -> None:
    print("[runtime] Loading settings...")
    settings = load_settings()
    print("[runtime] Building model providers...")
    models = build_models(settings)
    print("[runtime] Building agent bundle...")
    bundle = build_sales_agent_bundle(settings, models)
    manager = bundle.careful_sales_manager if protected else bundle.sales_manager

    trace_name = "Protected Automated SDR" if protected else "Automated SDR"
    print(f"[runtime] Running campaign (protected={protected})")
    with trace(trace_name):
        await Runner.run(manager, message)
    print("[runtime] Campaign run completed.")
