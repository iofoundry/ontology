"""Errors and warnings on a GitHub Actions job's summary page.

The hygiene and module IRI checks report problems as workflow annotations
(``::error file=F,line=N,title=T::message``); this lists them as Markdown tables under a
headline with the counts, and appends that to ``$GITHUB_STEP_SUMMARY`` (nothing is written
outside GitHub Actions).
"""
from __future__ import annotations

import contextlib
import io
import os
import re
import sys

ANNOTATION = re.compile(r'^::(error|warning)(?: (.*?))?::(.*)$')


def parse(line: str) -> dict | None:
    """{level, title, file, line, message} of an error or warning annotation, else None."""
    m = ANNOTATION.match(line.rstrip('\n'))
    if not m:
        return None
    props = dict(p.split('=', 1) for p in (m.group(2) or '').split(',') if '=' in p)
    return {'level': m.group(1), 'title': props.get('title', ''), 'file': props.get('file', ''),
            'line': props.get('line', ''), 'message': m.group(3)}


def _cell(text: str) -> str:
    return str(text).replace('|', '\\|').replace('\n', ' ')


def section(heading: str, findings: list) -> str:
    """'## ❌ heading: 1 error, 2 warnings', then a table of the errors and one of the warnings."""
    groups = [(level, [f for f in findings if f['level'] == level]) for level in ('error', 'warning')]
    counts = ', '.join(f'{len(rows)} {level}' + ('' if len(rows) == 1 else 's') for level, rows in groups)
    icon = '❌' if groups[0][1] else ('⚠️' if groups[1][1] else '✅')
    out = [f'## {icon} {heading}: {counts}\n']
    for level, rows in groups:
        if rows:
            out.append(f'### {level.capitalize()}s\n\n| Rule | File | Message |\n|---|---|---|')
            out += [f"| {_cell(f['title'])} | {_cell(f['file'] + (':' + f['line'] if f.get('line') else ''))} "
                    f"| {_cell(f['message'])} |" for f in rows]
            out.append('')
    return '\n'.join(out) + '\n'


def append(markdown: str) -> None:
    path = os.environ.get('GITHUB_STEP_SUMMARY')
    if path:
        with open(path, 'a', encoding='utf-8') as f:
            f.write(markdown)


class _Tee(io.TextIOBase):
    def __init__(self, stream, findings):
        self.stream, self.findings, self.pending = stream, findings, ''

    def write(self, text):
        self.stream.write(text)
        self.pending += text
        *lines, self.pending = self.pending.split('\n')
        self.findings += [f for f in map(parse, lines) if f]
        return len(text)

    def flush(self):
        self.stream.flush()


@contextlib.contextmanager
def recording():
    """Yield a list that collects every error and warning annotation printed meanwhile."""
    findings = []
    tee = _Tee(sys.stdout, findings)
    with contextlib.redirect_stdout(tee):
        yield findings
    if tee.pending:
        findings += [f for f in [parse(tee.pending)] if f]
