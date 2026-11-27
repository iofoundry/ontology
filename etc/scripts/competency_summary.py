"""Total the per-suite question counts of a CI run into one Markdown table.

Each competency job writes its suite's counts with `./competency SUITE --summary-json FILE`;
the summary job downloads those files and runs

    python etc/scripts/competency_summary.py DIR >> "$GITHUB_STEP_SUMMARY"

The counts and suite names are already in the public log, so the table reveals nothing more.
A suite whose job did not report (cancelled, or crashed before writing) is listed as missing.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from competency_runner import summary_table, tally_line


def collect(directory: Path) -> list[dict]:
    tallies = []
    for path in sorted(Path(directory).rglob('*.json')):
        tallies.extend(json.loads(path.read_text()))
    return tallies


def report(directory: Path, expected: list[str] | None = None) -> str:
    tallies = collect(directory)
    text = '## Competency questions: ' + tally_line(tallies) + '\n\n' + summary_table(tallies)
    missing = sorted(set(expected or []) - {t['suite'] for t in tallies})
    if missing:
        text += '\n**No result from:** ' + ', '.join(missing) + '\n'
    return text


if __name__ == '__main__':
    expected = json.loads(sys.argv[2]) if len(sys.argv) > 2 else None   # the suite list from --list
    sys.stdout.write(report(Path(sys.argv[1]), expected))
