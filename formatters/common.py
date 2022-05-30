class FormatException(Exception):
    def __init__(self, stderr):
        self.stderr = stderr
