import os

from dotenv import load_dotenv

load_dotenv()


def _resolve_openai_base_url() -> str:
    explicit = os.getenv("OPENAI_BASE_URL") or os.getenv("CODEX_BASE_URL")
    if explicit:
        return explicit.rstrip("/")

    proxy = os.getenv("ANTHROPIC_BASE_URL", "").rstrip("/")
    if proxy:
        return f"{proxy}/v1"

    return "https://api.openai.com/v1"


CHROMA_DB_PATH = "./chroma_db"

INTENT_TYPES = ["technique_selection", "main_generation", "quality_check"]
INTENT_DEFAULT = "main_generation"

ACTIVE_DOMAIN = os.getenv("AGENT_DOMAIN", "web_design")
OPENAI_BASE_URL = _resolve_openai_base_url()
OPENAI_TIMEOUT_SECONDS = int(os.getenv("OPENAI_TIMEOUT_SECONDS", "600"))
OPENAI_PREFER_CHAT_COMPLETIONS_STREAM = (
    os.getenv(
        "OPENAI_PREFER_CHAT_COMPLETIONS_STREAM",
        "0" if "api.openai.com" in OPENAI_BASE_URL else "1",
    )
    == "1"
)

LIGHT_MODEL = os.getenv("LIGHT_MODEL") or os.getenv("OPENAI_LIGHT_MODEL") or "gpt-5.4-mini"
LIGHT_REASONING_EFFORT = os.getenv("LIGHT_REASONING_EFFORT", "low")

PROMPT_BUILD_MODEL = os.getenv("PROMPT_BUILD_MODEL") or os.getenv("OPENAI_PROMPT_BUILD_MODEL") or LIGHT_MODEL
PROMPT_BUILD_REASONING_EFFORT = os.getenv("PROMPT_BUILD_REASONING_EFFORT", "low")

GENERATION_MODEL = os.getenv("GENERATION_MODEL") or os.getenv("OPENAI_MODEL") or "gpt-5.4"
GENERATION_REASONING_EFFORT = os.getenv("GENERATION_REASONING_EFFORT", "medium")
