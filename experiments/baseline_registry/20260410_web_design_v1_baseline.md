# Web Design V1 Baseline Freeze

- Freeze date: `2026-04-10`
- Baseline name: `web_design_profile_v1_compact_pass`
- Status: `current best passing baseline`
- Profile: `web_design`

## Artifact

- HTML: `experiments/web_design_profile_run/20260408_163658_gpt54_retry1_compact.html`
- Stats: `experiments/web_design_profile_run/20260408_163658_gpt54_retry1_compact_stats.json`

## Query

```text
Generate a compact single-file HTML landing page for an AI automation workspace. Keep the page concise but complete. Every visible button must have enforced default, hover, active, and focus-visible states. Fully wire mobile nav, FAQ accordion, tabs, toast, modal, animated counters, and one compact interactive sandbox section. Keep all copy coherent and avoid random wildcard headings.
```

## Runtime

- Base URL: `https://kuaipao.ai/v1`
- Light model: `gpt-5.4-mini`
- Prompt-build model: `gpt-5.4-mini`
- Generation model: `gpt-5.4`
- Compression rounds: `1`
- Retry count: `0`

## Token Summary

- Total input tokens: `25077`
- Total output tokens: `27579`
- Compression input tokens: `20699`
- Compression output tokens: `4020`
- Compression token retention ratio: `0.1942`

## Retrieval Snapshot

- Retrieved chunk count: `10`
- Retrieval mode: `expanded query -> dense retrieval -> rerank -> top-10`
- Current chunking mode:
  - `generator_techniques.md` -> `split_techniques`
  - `generator_flow.md` -> `split_by_h2`
  - `generator_wildcards.md` -> `split_by_h2`
- Current fixed injected docs:
  - `base_core.md`
  - `base_animation.md`
  - `visual_continuity.md`

## Quality Check Result

- Pass: `true`
- Issues: `0`
- Checks passed:
  - `html_closure`
  - `google_fonts`
  - `css_variables`
  - `semantic_sections`
  - `inline_only`
  - `forbidden_cdn`
  - `dead_anchors`
  - `button_reset`
  - `modal`
  - `accordion`
  - `toast`
  - `tabs`
  - `counter_animation`
  - `scroll_reveal`
  - `nav_scroll_state`
  - `focus_visible`
  - `responsive_390`
  - `avoid_pure_black_bg`

## Known Limits

- Current validator is still `web_html`-centric and not sufficient to prove cross-domain generality.
- Current chunking is still simple structure-aware chunking, not generalized ingestion.
- Compression is still freeform text, not schema-first structured compression.
- Retrieval is still single-layer dense retrieval with rerank; no parent-child expansion or BM25 branch yet.

## Reproducibility Note

- This workspace does not currently expose a local `.git` directory, so a commit SHA could not be captured at freeze time.
- Once git metadata is available locally, append:
  - repository root
  - commit SHA
  - dirty file list
  - tag name for this baseline
