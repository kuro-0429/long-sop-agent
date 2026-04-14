import os
from dataclasses import dataclass
from typing import Optional

from src.config import ACTIVE_DOMAIN


@dataclass(frozen=True)
class ContextDocument:
    key: str
    path: str
    section_title: str
    always_include: bool = True
    fallback_for: Optional[str] = None


@dataclass(frozen=True)
class IndexSource:
    collection: str
    path: str
    splitter: str
    source_name: str
    label: str


@dataclass(frozen=True)
class DomainProfile:
    name: str
    description: str
    collections: tuple[str, ...]
    index_sources: tuple[IndexSource, ...]
    context_documents: tuple[ContextDocument, ...]
    query_axes: tuple[str, ...]
    builder_outline: tuple[str, ...]
    prompt_build_system: str
    generate_system: str
    output_format: str
    validator_name: str


WEB_PROMPT_BUILD_SYSTEM = """You are a context compression architect for long SOP-driven agents.

Your job is to compress long configuration documents, retrieved references, and the user brief into a high-fidelity implementation spec for a downstream specialist model.

Rules:
1. Never drop precise values, thresholds, ARIA attributes, forbidden items, breakpoints, IDs, or named technique codes.
2. Separate hard requirements from optional creative guidance.
3. Preserve domain-specific details while removing duplication.
4. If previous validation issues are provided, convert them into explicit repair requirements.
5. Be selective and query-aware; do not dump the whole corpus into the spec.
6. Prefer a compact structured execution spec over a long narrative.
7. Output an implementation spec, not the final HTML.
"""


WEB_GENERATE_SYSTEM = """You are a senior front-end engineer executing a compressed implementation spec.

Rules:
- Output only a complete single-file HTML document.
- Inline all CSS and JS.
- Satisfy acceptance criteria before adding optional flair.
- If style guidance conflicts with hard constraints, hard constraints win.
- If user intent conflicts with style guidance, user intent wins unless it violates hard constraints.
"""


GENERIC_PROMPT_BUILD_SYSTEM = """You are a context compression architect for long SOP-driven agents.

Compress long rules, retrieved references, and the user task into a compact but lossless execution spec.

Rules:
1. Preserve precise requirements, thresholds, identifiers, and prohibited actions.
2. Separate mandatory constraints from recommendations.
3. Preserve repair instructions from previous validation failures.
4. Be selective and query-aware; keep only what is needed for correct execution.
5. Output an execution spec for a downstream model, not the final deliverable.
"""


GENERIC_GENERATE_SYSTEM = """You are a specialist execution model.

Follow the provided execution spec exactly.
Honor mandatory constraints before optional improvements.
Return only the requested deliverable content.
"""


DOMAIN_PROFILES = {
    "web_design": DomainProfile(
        name="web_design",
        description="Single-file HTML generation from long web design SOPs.",
        collections=("techniques", "flow", "style"),
        index_sources=(
            IndexSource(
                collection="techniques",
                path="configs/prompt_templates/generator_techniques.md",
                splitter="techniques",
                source_name="generator_techniques",
                label="technique library",
            ),
            IndexSource(
                collection="flow",
                path="configs/prompt_templates/generator_flow.md",
                splitter="h2",
                source_name="flow",
                label="generation flow",
            ),
            IndexSource(
                collection="style",
                path="configs/prompt_templates/generator_wildcards.md",
                splitter="h2",
                source_name="style",
                label="style and wildcard library",
            ),
        ),
        context_documents=(
            ContextDocument(
                key="base_core",
                path="configs/prompt_templates/base_core.md",
                section_title="MANDATORY_CORE_RULES",
            ),
            ContextDocument(
                key="base_animation",
                path="configs/prompt_templates/base_animation.md",
                section_title="MANDATORY_ANIMATION_RULES",
            ),
            ContextDocument(
                key="visual_continuity",
                path="configs/prompt_templates/visual_continuity.md",
                section_title="VISUAL_CONTINUITY_RULES",
            ),
            ContextDocument(
                key="style_wildcards",
                path="configs/prompt_templates/generator_wildcards.md",
                section_title="STYLE_AND_WILDCARD_FALLBACK",
                always_include=False,
                fallback_for="style",
            ),
        ),
        query_axes=(
            "visual style and techniques",
            "interactive behavior and state changes",
            "hard constraints and acceptance requirements",
            "generation flow and page structure",
        ),
        builder_outline=(
            "Confirmation Card",
            "Round 1: Structure and visual direction",
            "Round 2: Functional interactions",
            "Round 3: Responsive behavior and accessibility",
            "Round 4: Polish and acceptance",
            "Acceptance Criteria",
        ),
        prompt_build_system=WEB_PROMPT_BUILD_SYSTEM,
        generate_system=WEB_GENERATE_SYSTEM,
        output_format="html",
        validator_name="web_html",
    ),
    "generic_sop": DomainProfile(
        name="generic_sop",
        description="Generic long-SOP execution profile with no domain-specific validator.",
        collections=(),
        index_sources=(),
        context_documents=(),
        query_axes=(
            "task intent",
            "mandatory constraints",
            "step sequence",
            "acceptance criteria",
        ),
        builder_outline=(
            "Task Summary",
            "Mandatory Constraints",
            "Execution Plan",
            "Failure Recovery Notes",
            "Acceptance Criteria",
        ),
        prompt_build_system=GENERIC_PROMPT_BUILD_SYSTEM,
        generate_system=GENERIC_GENERATE_SYSTEM,
        output_format="text",
        validator_name="noop",
    ),
}


def get_domain_profile(name: Optional[str] = None) -> DomainProfile:
    profile_name = name or os.getenv("AGENT_DOMAIN", ACTIVE_DOMAIN)
    try:
        return DOMAIN_PROFILES[profile_name]
    except KeyError as exc:
        available = ", ".join(sorted(DOMAIN_PROFILES))
        raise ValueError(f"Unknown domain profile '{profile_name}'. Available: {available}") from exc
