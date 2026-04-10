from typing import Any, Dict

from src.evaluation.rule_validators import RuleValidator


class NoopValidator:
    def validate(self, content: str) -> Dict[str, Any]:
        return {
            "pass": True,
            "issues": [],
            "checks": {"noop": True},
        }


class WebHtmlValidator:
    def __init__(self) -> None:
        self._validator = RuleValidator()

    def validate(self, content: str) -> Dict[str, Any]:
        return self._validator.validate_html(content)


def get_validator(name: str):
    if name == "web_html":
        return WebHtmlValidator()
    if name == "noop":
        return NoopValidator()
    raise ValueError(f"Unknown validator: {name}")
