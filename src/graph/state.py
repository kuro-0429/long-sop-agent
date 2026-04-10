from typing import Optional, TypedDict


class AgentState(TypedDict):
    user_query: str
    domain: Optional[str]

    intent: Optional[str]

    retrieved_chunks: Optional[list[str]]
    context: Optional[str]
    expanded_queries: Optional[list[str]]

    built_prompt: Optional[str]
    generation_result: Optional[str]

    quality_check: Optional[dict]
    retry_count: int
