import subprocess
import os
from pathlib import Path
from .common import FormatException

EXT = {"C": ".c", "C++": ".cpp"}


class ClangformatFormatter:
    def __init__(self, syntax, filename):
        self.syntax = syntax
        self.filename = filename

    def format(self, text):
        filepath = Path(self.filename)
        p = subprocess.Popen(
            ["clang-format", "--assume-filename", filepath.stem + EXT[self.syntax]],
            cwd=os.path.dirname(self.filename),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        output, error = p.communicate(text.encode())
        if p.returncode != 0:
            raise FormatException(error.decode())
        return output.decode()
