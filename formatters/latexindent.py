import subprocess
import os
from .common import FormatException


class LatexindentFormatter:
    def __init__(self, syntax, filename):
        self.syntax = syntax
        self.filename = filename

    def format(self, text):
        p = subprocess.Popen(
            ["latexindent"],
            cwd=os.path.dirname(self.filename),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        output, error = p.communicate(text.encode())
        if p.returncode != 0:
            raise FormatException(error.decode())
        return output.decode()
