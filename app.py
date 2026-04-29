import asyncio
import argparse

from sdr.runtime import run_campaign


#DEFAULT_MESSAGE = "Send out a cold sales email addressed to Dear CEO from Alice"
DEFAULT_MESSAGE = "Send out a cold sales email addressed to Dear CEO from Head of Business Development"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run SDR campaign.")
    parser.add_argument("--message", default=DEFAULT_MESSAGE, help="Campaign message prompt.")
    parser.add_argument(
        "--unprotected",
        action="store_true",
        help="Run without input guardrails.",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    await run_campaign(args.message, protected=not args.unprotected)


if __name__ == "__main__":
    asyncio.run(main())