import subprocess
import os
from .common import FormatException

PARSERS = {
    "JavaScript": "babel",
    "JavaScript (Babel)": "babel",
    "JSON": "json",
    "HTML": "html",
    "YAML": "yaml",
    "CSS": "css",
    "Vue Component": "vue",
}


class PrettierFormatter:
    def __init__(self, syntax, filename):
        self.syntax = syntax
        self.filename = filename

    def format(self, text):
        p = subprocess.Popen(
            [
                "prettier",
                "--parser",
                PARSERS[self.syntax],
                "--stdin-filepath",
                self.filename,
            ],
            cwd=os.path.dirname(self.filename),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        output, error = p.communicate(text.encode())
        if p.returncode != 0:
            raise FormatException(error.decode())
        return output.decode()
