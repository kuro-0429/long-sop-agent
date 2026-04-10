# Harness Plan

## 1. Goal

This harness is the control layer for all future upgrades. Its only job is to ensure that every important change and every ablation is:

- traceable
- explainable
- reproducible

The harness must compare new runs against a frozen baseline rather than relying on subjective impressions.

## 2. Frozen Baseline

Current baseline:

- name: `web_design_profile_v1_compact_pass`
- artifact: `experiments/web_design_profile_run/20260408_163658_gpt54_retry1_compact.html`
- stats: `experiments/web_design_profile_run/20260408_163658_gpt54_retry1_compact_stats.json`
- registry entry: `experiments/baseline_registry/20260410_web_design_v1_baseline.md`

This baseline must remain untouched and always be re-runnable.

## 3. Task Suite

The harness should evaluate four task layers. These are specific enough for the current web profile, but generic enough to transfer to future profiles.

### Task A. Retrieval Fidelity

Question:

- Did the system retrieve the right evidence for the task?

Inputs:

- benchmark query
- profile
- oracle chunk ids

Metrics:

- recall@k
- precision@k
- rerank delta
- source diversity

### Task B. Compression Fidelity

Question:

- Did the system preserve the hard constraints after compression?

Inputs:

- retrieved chunks
- oracle hard constraints
- built prompt or execution spec

Metrics:

- hard-constraint coverage
- source-grounding coverage
- unresolved-item rate
- compression retention ratio

### Task C. End-to-End Artifact Quality

Question:

- Did the generated artifact satisfy the task requirements?

Inputs:

- query
- profile
- generated artifact
- validator outputs

Metrics:

- validator pass rate
- issue count by type
- retry success rate
- token cost
- latency

### Task D. Repair Loop Quality

Question:

- If the first attempt failed, did the retry loop repair the right issues without causing regressions?

Inputs:

- first-pass output
- validator issues
- retry path
- final output

Metrics:

- repair success rate
- regression count
- repair token cost
- issue recurrence rate

## 4. Initial Concrete Benchmark Set

For the current `web_design` profile, define an initial benchmark set of 12 tasks:

- 4 compact landing page tasks
- 4 interaction-heavy tasks
- 2 constraint-heavy tasks
- 2 repair tasks

Each benchmark item should contain:

- `task_id`
- `profile`
- `query`
- `artifact_type`
- `oracle_constraints`
- `oracle_chunk_ids`
- `validator_expectations`
- `notes`

## 5. Run Record Schema

Every run should create a folder under:

`experiments/runs/<run_id>/`

Minimum files:

- `run_manifest.json`
- `query.json`
- `retrieval.json`
- `compression.json`
- `generation.json`
- `validator.json`
- `artifact.html` or equivalent
- `summary.json`

Recommended manifest fields:

- `run_id`
- `timestamp`
- `profile`
- `system_version`
- `baseline_ref`
- `models`
- `provider`
- `query`
- `ablation_flags`
- `dataset_item_id`

Recommended retrieval fields:

- `expanded_queries`
- `retrieved_chunks`
- `chunk_ids`
- `chunk_scores`
- `parent_ids`
- `retrieval_latency_ms`

Recommended compression fields:

- `compression_model`
- `input_tokens`
- `output_tokens`
- `retention_ratio`
- `execution_spec`
- `source_refs`

Recommended validator fields:

- `pass`
- `issues`
- `checks`
- `retry_count`

## 6. First Ablation Matrix

Each important architectural update must be tested against the same benchmark set with ablation flags.

Initial ablations:

- `dense_only`
- `dense_plus_rerank`
- `no_parent_expansion`
- `freeform_compression`
- `structured_compression`
- `no_retry`
- `retry_enabled`

Rule:

- never compare two runs unless the benchmark set is identical
- never replace the baseline without recording the previous one

## 7. New Path

The next path is not “keep polishing web output”. The next path is:

1. generalized ingestion and layered chunking
2. parent-child plus hybrid retrieval
3. source-grounded structured compression
4. reproducible evaluation and tracing
5. lightweight experience memory after the core path is stable

## 8. Why This Path

### 8.1 Not just newer, but more appropriate

These choices are not claimed to be universally best for every agent system.

They are the best fit for this repository at the current stage because the current failure mode is:

- small hard constraints get missed
- compression is hard to inspect
- improvements are hard to prove

So the chosen path optimizes for:

- preserving small details
- making compression inspectable
- measuring improvements reproducibly

### 8.2 What is borrowed from current best practice

- `structured outputs` is the most production-ready path for schema-first compression
- `parent-child retrieval` is one of the most practical current retrieval patterns for long documents
- `contextual retrieval` is a strong recent direction for improving chunk usefulness in long documents
- `LongMemEval`, `MemBench`, `Mem2ActBench`, and `AMA-Bench` are useful recent signals for evaluation design
- `Phoenix`, `OpenAI Agent Evals`, and `trace grading` reflect current best practice for observability and evaluation

## 9. External References

- OpenAI Structured Outputs: https://platform.openai.com/docs/guides/structured-outputs
- OpenAI Agent Evals: https://platform.openai.com/docs/guides/agent-evals
- OpenAI Trace Grading: https://platform.openai.com/docs/guides/trace-grading
- Anthropic Contextual Retrieval: https://www.anthropic.com/research/contextual-retrieval
- ParentDocumentRetriever: https://api.python.langchain.com/en/latest/langchain/retrievers/langchain.retrievers.parent_document_retriever.ParentDocumentRetriever.html
- LlamaIndex Recursive Retriever: https://developers.llamaindex.ai/python/framework-api-reference/packs/recursive_retriever/
- EXIT: https://aclanthology.org/2025.findings-acl.253/
- Attribute First, then Generate: https://arxiv.org/abs/2403.17104
- Attribute or Abstain: https://aclanthology.org/2024.emnlp-main.463/
- RECOMP: https://openreview.net/forum?id=mlJLVigNHp
- LongMemEval: https://proceedings.iclr.cc/paper_files/paper/2025/file/d813d324dbf0598bbdc9c8e79740ed01-Paper-Conference.pdf
- MemBench: https://aclanthology.org/2025.findings-acl.989/
- Mem2ActBench: https://arxiv.org/abs/2601.19935
- AMA-Bench: https://arxiv.org/abs/2602.22769
- LangMem: https://langchain-ai.github.io/langmem/
- Phoenix: https://github.com/Arize-ai/phoenix
