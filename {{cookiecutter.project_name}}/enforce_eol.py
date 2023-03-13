#!/usr/bin/env python
import sys
from collections.abc import Iterator
from itertools import chain
from pathlib import Path
from traceback import print_exc


def assert_eol_characters(filename):
    size = filename.stat().st_size
    if size == 0:
        return
    if size == 1:
        raise ValueError(f"File {filename} contains only a single character")
    with filename.open("rb+") as file:
        file.seek(-2, 2)
        penultimate, last = file.read(2)
    newline = ord("\n")
    if last != newline:
        raise ValueError(f"File {filename} doesn't end with a \\n character")
    if penultimate == newline:
        raise ValueError(f"File {filename} ends with multiple \\n characters")


def gather_files() -> Iterator[Path]:
    base_dir = Path(__file__).parent
    files = [
        base_dir.iterdir(),
        base_dir.joinpath("src").rglob("*"),
        base_dir.joinpath("tests").rglob("*"),
    ]
    ignored_suffixes = {".ico", ".jpg", ".png"}
    for file in chain.from_iterable(files):
        if (
            file.is_file()
            and file.parent.name != "__pycache__"
            and file.suffix not in ignored_suffixes
        ):
            yield file


def main():
    failed = False
    for file in gather_files():
        try:
            assert_eol_characters(file)
        except ValueError:
            print_exc(limit=0)
            failed = True
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
