import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.config import ACTIVE_DOMAIN
from src.evaluation.harness import DEFAULT_BASELINE_REF, build_run_id, persist_run, run_agent_once


def load_query(args: argparse.Namespace) -> str:
    if args.query:
        return args.query.strip()
    if args.query_file:
        return Path(args.query_file).read_text(encoding="utf-8").strip()
    raise ValueError("Provide --query or --query-file")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the agent pipeline and persist a structured run bundle.")
    parser.add_argument("--query", help="User query to run.")
    parser.add_argument("--query-file", help="Path to a text file containing the query.")
    parser.add_argument("--profile", default=ACTIVE_DOMAIN, help="Domain profile name.")
    parser.add_argument("--dataset-item-id", default=None, help="Benchmark task id for tracking.")
    parser.add_argument(
        "--ablation-flag",
        action="append",
        default=[],
        help="Ablation flag to record. Can be passed multiple times.",
    )
    parser.add_argument("--baseline-ref", default=DEFAULT_BASELINE_REF, help="Baseline reference label.")
    parser.add_argument("--output-root", default=None, help="Optional override for experiments/runs output root.")
    args = parser.parse_args()

    query = load_query(args)
    run_id = build_run_id(args.profile, query, args.dataset_item_id)
    result, duration_sec = run_agent_once(query, args.profile)
    output_root = Path(args.output_root) if args.output_root else None
    run_dir = persist_run(
        query=query,
        profile_name=args.profile,
        result=result,
        duration_sec=duration_sec,
        run_id=run_id,
        output_root=output_root,
        baseline_ref=args.baseline_ref,
        dataset_item_id=args.dataset_item_id,
        ablation_flags=args.ablation_flag,
    )

    quality = result.get("quality_check") or {}
    print(f"[run_pipeline] run_dir={run_dir}")
    print(f"[run_pipeline] pass={quality.get('pass')} retry_count={result.get('retry_count', 0)} duration_sec={duration_sec}")


if __name__ == "__main__":
    main()
