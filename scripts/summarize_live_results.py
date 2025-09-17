import json
from pathlib import Path

summary = json.loads(Path("live_test_results.json").read_text(encoding="utf-8"))
print(f"Total success: {summary['total_success']} of {summary['total_count']}")
for category, info in summary["categories"].items():
    failed = [(name, details) for name, details in info["details"].items() if not details[0]]
    print(f"\nCategory: {category} ({info['successful']}/{info['total']})")
    if failed:
        for name, details in failed:
            snippet = details[1].splitlines()[0]
            print(f"  - FAILED {name}: {snippet}")
    else:
        print("  All endpoints OK.")
