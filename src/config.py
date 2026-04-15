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

RETRIEVAL_ENABLE_DENSE = os.getenv("RETRIEVAL_ENABLE_DENSE", "1") == "1"
RETRIEVAL_ENABLE_LEXICAL = os.getenv("RETRIEVAL_ENABLE_LEXICAL", "1") == "1"
RETRIEVAL_ENABLE_PARENT_EXPANSION = os.getenv("RETRIEVAL_ENABLE_PARENT_EXPANSION", "1") == "1"
RETRIEVAL_DENSE_TOP_K = int(os.getenv("RETRIEVAL_DENSE_TOP_K", "4"))
RETRIEVAL_LEXICAL_TOP_K = int(os.getenv("RETRIEVAL_LEXICAL_TOP_K", "4"))
RETRIEVAL_PRE_RERANK_K = int(os.getenv("RETRIEVAL_PRE_RERANK_K", "18"))
RETRIEVAL_RERANK_TOP_K = int(os.getenv("RETRIEVAL_RERANK_TOP_K", "8"))
RETRIEVAL_FINAL_TOP_K = int(os.getenv("RETRIEVAL_FINAL_TOP_K", "10"))
RETRIEVAL_PARENT_EXPAND_MAX_FAMILIES = int(os.getenv("RETRIEVAL_PARENT_EXPAND_MAX_FAMILIES", "3"))
RETRIEVAL_PARENT_EXPAND_MAX_EXTRA = int(os.getenv("RETRIEVAL_PARENT_EXPAND_MAX_EXTRA", "4"))
RETRIEVAL_HYBRID_DENSE_WEIGHT = float(os.getenv("RETRIEVAL_HYBRID_DENSE_WEIGHT", "0.65"))
RETRIEVAL_HYBRID_LEXICAL_WEIGHT = float(os.getenv("RETRIEVAL_HYBRID_LEXICAL_WEIGHT", "0.35"))
