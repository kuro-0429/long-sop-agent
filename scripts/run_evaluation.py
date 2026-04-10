import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from src.evaluation.harness import (
    DEFAULT_BASELINE_REF,
    build_run_id,
    evaluate_result_against_benchmark,
    persist_run,
    run_agent_once,
    utc_timestamp,
    write_json,
)


def load_benchmark_items(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run benchmark items and persist structured evaluation outputs.")
    parser.add_argument(
        "--benchmark-file",
        default="experiments/benchmarks/web_design_v1_tasks.json",
        help="Path to benchmark task JSON file.",
    )
    parser.add_argument("--task-id", default=None, help="Optional single task id to run.")
    parser.add_argument("--output-root", default=None, help="Optional override for experiments/runs output root.")
    parser.add_argument("--baseline-ref", default=DEFAULT_BASELINE_REF, help="Baseline reference label.")
    parser.add_argument(
        "--ablation-flag",
        action="append",
        default=[],
        help="Ablation flag to record. Can be passed multiple times.",
    )
    args = parser.parse_args()

    benchmark_path = Path(args.benchmark_file)
    items = load_benchmark_items(benchmark_path)
    if args.task_id:
        items = [item for item in items if item["task_id"] == args.task_id]

    if not items:
        raise ValueError("No benchmark items selected.")

    output_root = Path(args.output_root) if args.output_root else None
    evaluation_results = []

    for item in items:
        result, duration_sec = run_agent_once(item["query"], item["profile"])
        run_id = build_run_id(item["profile"], item["query"], item["task_id"])
        run_dir = persist_run(
            query=item["query"],
            profile_name=item["profile"],
            result=result,
            duration_sec=duration_sec,
            run_id=run_id,
            output_root=output_root,
            baseline_ref=args.baseline_ref,
            dataset_item_id=item["task_id"],
            ablation_flags=args.ablation_flag,
        )
        evaluation = evaluate_result_against_benchmark(benchmark_item=item, result=result)
        evaluation["run_dir"] = str(run_dir)
        evaluation_results.append(evaluation)
        print(
            f"[run_evaluation] task_id={item['task_id']} pass={evaluation['validator_pass']} "
            f"retry_count={evaluation['retry_count']} run_dir={run_dir}"
        )

    summary_path = (output_root or (REPO_ROOT / "experiments" / "runs")) / f"evaluation_summary_{utc_timestamp()}.json"
    write_json(
        summary_path,
        {
            "benchmark_file": str(benchmark_path),
            "task_count": len(evaluation_results),
            "results": evaluation_results,
        },
    )
    print(f"[run_evaluation] summary={summary_path}")


if __name__ == "__main__":
    main()
