"""R5: the record must be exactly 26 characters. (Working in the starter.)"""
CODE = "R5"
ORDER = 0     # runs first: later rules slice the line and need the right length


def ok(line):
    return len(line) == 26
