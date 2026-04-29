# SDR Automation with Guardrails

Minimal SDR orchestration app using OpenAI Agents, multiple model providers, guardrails, and SendGrid delivery.

## Prerequisites

- Python 3.12+
- [`uv`](https://docs.astral.sh/uv/) installed

## Setup (with uv)

1. Create/update the virtual environment and install dependencies:

```bash
uv sync
```

2. Copy and edit environment variables:

```bash
cp .env.example .env
```

Set at least:

- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`
- `DEEPSEEK_API_KEY`
- `GROQ_API_KEY`
- `SENDGRID_API_KEY`
- Optional: `SENDER_EMAIL`, `RECIPIENT_EMAIL`

## Run

Protected mode (default):

```bash
uv run python app.py
```

Unprotected mode:

```bash
uv run python app.py --unprotected
```

Custom message:

```bash
uv run python app.py --message "Send out a cold sales email addressed to Dear CEO from Head of Business Development"
```

## Tests

```bash
uv run python -m unittest discover -s tests -p "test_*.py"
```

## Project Structure

- `app.py` - CLI entrypoint
- `sdr/config.py` - environment-backed settings
- `sdr/providers.py` - model provider factories
- `sdr/tools/email_tools.py` - email tools and SendGrid integration
- `sdr/agents/` - agent and guardrail composition
- `sdr/runtime.py` - campaign orchestration
