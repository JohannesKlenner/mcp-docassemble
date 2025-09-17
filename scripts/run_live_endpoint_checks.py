"""Utility script to exercise all Docassemble endpoints exposed by the MCP client.

Usage::

    DOCASSEMBLE_BASE_URL=http://... \
    DOCASSEMBLE_API_KEY=... \
    PYTHONIOENCODING=utf-8 \
    python scripts/run_live_endpoint_checks.py

The script prints the raw results from the suite (including the detailed
per-endpoint output produced by the underlying test helpers) and writes a
machine-readable summary to ``live_test_results.json`` in the project root.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from tests.test_data_and_keys import DataAndKeyManagementTests
from tests.test_interview_management import InterviewManagementTests
from tests.test_playground_management import PlaygroundManagementTests
from tests.test_server_management import ServerManagementTests
from tests.test_user_management import UserManagementTests

MODULES = [
    ("user_management", UserManagementTests),
    ("data_and_keys", DataAndKeyManagementTests),
    ("interview_management", InterviewManagementTests),
    ("playground_management", PlaygroundManagementTests),
    ("server_management", ServerManagementTests),
]


def main() -> None:
    summary: dict[str, dict[str, object]] = {}
    total_success = 0
    total_count = 0

    for name, cls in MODULES:
        print(f"\n====== Starte Testkategorie: {name} ======")
        tester = cls()
        tester.delay = max(getattr(tester, "delay", 1), 1)
        results = tester.run_all_tests()

        successes = sum(1 for success, _ in results.values() if success)
        count = len(results)

        total_success += successes
        total_count += count

        summary[name] = {
            "successful": successes,
            "total": count,
            "details": results,
        }

        time.sleep(5)

    print("\n====== Gesamtübersicht ======")
    print(f"Erfolgreich: {total_success}/{total_count}")
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    Path("live_test_results.json").write_text(
        json.dumps(
            {
                "total_success": total_success,
                "total_count": total_count,
                "categories": summary,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
