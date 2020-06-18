class Location:
    file: str
    line: int

    def __init__(self, file: str, line: int):
        self.file = file
        self.line = line