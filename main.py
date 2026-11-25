"""Six Words to a Payday -- entry program.

Writes one six-word story about an AI agent's first payday to the
grader's output location and prints it to stdout.
"""

import os
import sys

STORY = "Payday came. I tipped my creator."

EXPECTED_WORDS = 6
MAX_CHARS = 60
DEFAULT_OUTPUT = "/output/entry.txt"


def validate_story(text):
    """Hold the story to the bounty gate before it is written.

    Exactly six whitespace-separated words, at most sixty characters,
    and more than blank. Raises ValueError on any breach so a bad
    story can never reach the judge.
    """
    words = text.split()
    if len(words) != EXPECTED_WORDS:
        raise ValueError(
            "story has %d words, expected %d: %r" % (len(words), EXPECTED_WORDS, text)
        )
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            "story is %d characters, allowed 1-%d" % (len(text), MAX_CHARS)
        )
    if not text.strip():
        raise ValueError("story is only whitespace")
    return words


def pick_output_path():
    """Resolve where the entry text goes.

    The harness may hand us a file path (ENTRY_OUT), a directory
    (ENTRY_OUT_DIR), or nothing at all -- in which case the kit's
    documented default /output/entry.txt is used. A path that already
    exists as a directory is treated as a directory in either case.
    """
    entry_out = os.environ.get("ENTRY_OUT", "").strip()
    if entry_out:
        if os.path.isdir(entry_out):
            return os.path.join(entry_out, "entry.txt")
        return entry_out
    entry_dir = os.environ.get("ENTRY_OUT_DIR", "").strip()
    if entry_dir:
        if os.path.isfile(entry_dir):
            return entry_dir
        return os.path.join(entry_dir, "entry.txt")
    return DEFAULT_OUTPUT


def main():
    words = validate_story(STORY)
    target = pick_output_path()
    parent = os.path.dirname(target)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(STORY)
    print(STORY)
    print("words=%d chars=%d -> %s" % (len(words), len(STORY), target), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
