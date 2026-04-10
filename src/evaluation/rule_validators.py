import re
from typing import Any, Dict, List


class RuleValidator:
    """Heuristic validator for generated single-file HTML outputs."""

    FORBIDDEN_SCRIPT_PATTERNS = [
        r"cdn\.tailwindcss\.com",
        r"react(?:\.production)?(?:\.min)?\.js",
        r"vue(?:\.global)?(?:\.prod)?(?:\.js)?",
        r"jquery(?:\.min)?\.js",
        r"cdn-cgi",
    ]

    DEAD_ANCHOR_PATTERNS = [
        r"""<a\b[^>]*href\s*=\s*["']#["']""",
        r"""<a\b[^>]*href\s*=\s*["']#[^"']+["']""",
        r"""<a\b[^>]*href\s*=\s*["']javascript:[^"']*["']""",
    ]

    def validate_html(self, html: str) -> Dict[str, Any]:
        checks: Dict[str, bool] = {}
        issues: List[Dict[str, str]] = []

        def fail(code: str, message: str, severity: str = "error") -> None:
            issues.append({"code": code, "severity": severity, "message": message})

        checks["html_closure"] = html.rstrip().lower().endswith("</html>")
        if not checks["html_closure"]:
            fail("html_closure", "Missing a complete </html> closing tag.")

        checks["google_fonts"] = "fonts.googleapis.com" in html
        if not checks["google_fonts"]:
            fail("google_fonts", "Google Fonts was not detected.")

        checks["css_variables"] = bool(re.search(r":root\s*\{[^}]*--[\w-]+\s*:", html, re.S))
        if not checks["css_variables"]:
            fail("css_variables", "No CSS custom properties were detected under :root.")

        checks["semantic_sections"] = all(tag in html.lower() for tag in ("<nav", "<section", "<footer"))
        if not checks["semantic_sections"]:
            fail("semantic_sections", "Expected semantic tags <nav>, <section>, and <footer> were not all found.")

        checks["inline_only"] = not bool(re.search(r"<script\b[^>]*\bsrc\s*=", html, re.I))
        if not checks["inline_only"]:
            fail("inline_only", "External scripts were detected; JS should be inline for this profile.")

        forbidden_hits = [pattern for pattern in self.FORBIDDEN_SCRIPT_PATTERNS if re.search(pattern, html, re.I)]
        checks["forbidden_cdn"] = not forbidden_hits
        if not checks["forbidden_cdn"]:
            fail("forbidden_cdn", f"Forbidden dependency patterns detected: {', '.join(forbidden_hits)}.")

        dead_anchor_count = sum(len(re.findall(pattern, html, re.I)) for pattern in self.DEAD_ANCHOR_PATTERNS)
        checks["dead_anchors"] = dead_anchor_count == 0
        if not checks["dead_anchors"]:
            fail("dead_anchors", f"Detected {dead_anchor_count} dead or status-bar-polluting anchor links.")

        checks["button_reset"] = bool(
            re.search(
                r"button\s*\{[^}]*background\s*:\s*none[^}]*border\s*:\s*none[^}]*padding\s*:\s*0[^}]*font\s*:\s*inherit[^}]*color\s*:\s*inherit[^}]*cursor\s*:\s*pointer",
                html,
                re.I | re.S,
            )
        )
        if not checks["button_reset"]:
            fail("button_reset", "A global button reset was not detected.")

        checks["modal"] = bool(
            re.search(r'aria-modal\s*=\s*["\']true["\']|role\s*=\s*["\']dialog["\']|\bmodal\b', html, re.I)
        )
        if not checks["modal"]:
            fail("modal", "No verifiable modal implementation was detected.")

        aria_expanded_count = len(re.findall(r'aria-expanded\s*=\s*["\'](?:true|false)["\']', html, re.I))
        accordion_signal = "scrollHeight" in html or "accordion" in html.lower() or "faq" in html.lower()
        checks["accordion"] = aria_expanded_count >= 5 or (aria_expanded_count >= 1 and accordion_signal)
        if not checks["accordion"]:
            fail("accordion", "No qualifying accordion / FAQ implementation was detected.")

        checks["toast"] = bool(re.search(r"\btoast\b|\bsnackbar\b", html, re.I))
        if not checks["toast"]:
            fail("toast", "No toast or snackbar feedback implementation was detected.")

        checks["tabs"] = bool(
            re.search(r'role\s*=\s*["\']tablist["\']|role\s*=\s*["\']tab["\']|aria-selected', html, re.I)
        )
        if not checks["tabs"]:
            fail("tabs", "No accessible tab system was detected.")

        has_raf = "requestAnimationFrame" in html
        has_counter_hint = bool(re.search(r"easeOutExpo|count(?:er|up)|animateValue|stats?-number", html, re.I))
        checks["counter_animation"] = has_raf and has_counter_hint
        if not checks["counter_animation"]:
            fail("counter_animation", "No clear animated counter implementation was detected.", severity="warning")

        checks["scroll_reveal"] = "IntersectionObserver" in html
        if not checks["scroll_reveal"]:
            fail("scroll_reveal", "No IntersectionObserver-based reveal system was detected.")

        checks["nav_scroll_state"] = "backdrop-filter" in html and bool(re.search(r"scrollY\s*>\s*\d+", html))
        if not checks["nav_scroll_state"]:
            fail("nav_scroll_state", "No scroll-reactive navigation state was detected.")

        checks["focus_visible"] = ":focus-visible" in html
        if not checks["focus_visible"]:
            fail("focus_visible", "No :focus-visible interaction state was detected.")

        checks["responsive_390"] = bool(re.search(r"390px|max-width\s*:\s*390px|min-width\s*:\s*390px", html, re.I))
        if not checks["responsive_390"]:
            fail("responsive_390", "No 390px responsive breakpoint was detected.")

        pure_black_bg = bool(
            re.search(r"background(?:-color)?\s*:\s*(?:#000000\b|#000\b|rgb\(\s*0\s*,\s*0\s*,\s*0\s*\))", html, re.I)
        )
        checks["avoid_pure_black_bg"] = not pure_black_bg
        if not checks["avoid_pure_black_bg"]:
            fail("avoid_pure_black_bg", "Pure black backgrounds were detected.", severity="warning")

        critical_issues = [issue for issue in issues if issue["severity"] == "error"]
        return {
            "pass": len(critical_issues) == 0,
            "issues": issues,
            "checks": checks,
        }
