from typing import Any, Optional, TypedDict


class AgentState(TypedDict, total=False):
    user_query: str
    domain: Optional[str]

    intent: Optional[str]

    retrieved_chunks: Optional[list[str]]
    retrieved_chunk_details: Optional[list[dict[str, Any]]]
    context: Optional[str]
    expanded_queries: Optional[list[str]]

    built_prompt: Optional[str]
    execution_spec: Optional[dict[str, Any]]
    generation_result: Optional[str]

    quality_check: Optional[dict[str, Any]]
    retry_count: int
    call_logs: Optional[list[dict[str, Any]]]

    intent_metadata: Optional[dict[str, Any]]
    retrieval_metadata: Optional[dict[str, Any]]
    compression_metadata: Optional[dict[str, Any]]
    spec_parse_metadata: Optional[dict[str, Any]]
    generation_metadata: Optional[dict[str, Any]]
