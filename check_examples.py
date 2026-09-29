#!/usr/bin/env python3
"""Check every code example printed in the book.

Three kinds of check, run against every src/*.adoc file:

  * REPL transcripts (fenced blocks containing ``>>>``) are replayed
    through doctest: a printed output must still be the interpreter's
    output;
  * ``[source,python]`` blocks are just executed, to catch syntax rot;
  * a stray prompt (a bare ``>>>`` line) is reported: doctest swallows
    such a line without any error.

Usage:
    python3 check_examples.py    (or `make test`)

Exit code is non-zero when at least one example fails.
"""

import doctest
import io
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

SRC = Path(__file__).resolve().parent / "src"

# A fenced block (```), as used for the REPL transcripts.
FENCE = re.compile(r"^```[^\n]*\n(.*?)^```[ \t]*$", re.DOTALL | re.MULTILINE)
# An AsciiDoc source block tagged [source,python].
SOURCE = re.compile(
    r"^\[source,python\]\s*\n----\n(.*?)^----[ \t]*$", re.DOTALL | re.MULTILINE
)
# A REPL prompt with nothing after it: a typo, not an example.
STRAY_PROMPT = re.compile(r">>>[ \t]*")


class TranscriptChecker(doctest.OutputChecker):
    """Compare outputs the way a REPL transcript is written.

    The interpreter ends an output with a blank line (`help` does), a
    printed transcript never shows it: the closing fence of the block
    does the job. Trailing blank lines are therefore dropped on both
    sides before comparing.
    """

    def check_output(self, want, got, optionflags):
        got = got.rstrip("\n")
        want = want.rstrip("\n")
        return super().check_output(want + "\n", got + "\n", optionflags)


def line_of(text, pos):
    """1-based line number of the match at `pos`."""
    return text.count("\n", 0, pos) + 1


def mark_blank_lines(block):
    """Teach doctest the blank lines printed by the interpreter.

    doctest reads an empty line as the end of an expected output, while the
    REPL (pydoc's ``help`` for instance) happily prints one in the middle of
    its output. Every *interior* blank line becomes a ``<BLANKLINE>``
    marker; the ones separating two examples are left alone.
    """
    lines = block.split("\n")
    marked = []
    for index, line in enumerate(lines):
        following = lines[index + 1] if index + 1 < len(lines) else ""
        if line == "" and following and not following.startswith((">>>", "...")):
            marked.append("<BLANKLINE>")
        else:
            marked.append(line)
    return "\n".join(marked)


def check_repl(runner, path, text):
    """Feed every `>>>` block of `path` to the doctest runner.

    A stray prompt (a bare `>>>` line) is a typo in the book; doctest
    swallows it without an error, so it is hunted line by line here.
    """
    parser = doctest.DocTestParser()
    issues = []
    for match in FENCE.finditer(text):
        block = match.group(1)
        if ">>>" not in block:
            continue
        block = mark_blank_lines(block)
        line = line_of(text, match.start())
        for offset, source_line in enumerate(block.split("\n")):
            if STRAY_PROMPT.fullmatch(source_line):
                issues.append(
                    f"{path.name}:{line + 1 + offset}: stray `>>>` prompt"
                )
        name = f"{path.name}:{line}"
        runner.run(parser.get_doctest(block, {}, name, str(path), line))
    return issues


def check_source_blocks(path, text):
    """Execute every [source,python] block, and report any failure."""
    failures = []
    checked = 0
    for match in SOURCE.finditer(text):
        block = match.group(1)
        checked += 1
        name = f"{path.name}:{line_of(text, match.start())}"
        try:
            compiled = compile(block, name, "exec")
        except SyntaxError as error:
            failures.append(f"{name}: SyntaxError: {error.msg} (line {error.lineno})")
            continue
        try:
            # Examples may print (yeaaah), that is not what we are after here.
            with redirect_stdout(io.StringIO()):
                exec(compiled, {})
        except Exception as error:  # noqa: BLE001 - any crash is a broken example
            failures.append(f"{name}: {error.__class__.__name__}: {error}")
    return failures, checked


def main():
    paths = sorted(SRC.glob("*.adoc"))
    if not paths:
        print(f"no AsciiDoc source found in {SRC}", file=sys.stderr)
        return 2

    runner = doctest.DocTestRunner(verbose=False, checker=TranscriptChecker())
    stray_prompts = []
    source_issues = []
    source_blocks = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        stray_prompts.extend(check_repl(runner, path, text))
        failures, checked = check_source_blocks(path, text)
        source_issues.extend(failures)
        source_blocks += checked

    for line in stray_prompts + source_issues:
        print(f"FAIL {line}", file=sys.stderr)

    print(
        f"{runner.tries} transcript examples, {runner.failures} failed; "
        f"{source_blocks} source blocks, {len(source_issues)} failed; "
        f"{len(stray_prompts)} stray prompts"
    )
    broken = runner.failures or source_issues or stray_prompts
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
