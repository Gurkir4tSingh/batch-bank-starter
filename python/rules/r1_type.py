"""R1: TYPE (character 9, index 8) must be D, W or T. (Working in the starter.)"""
CODE = "R1"
ORDER = 10


def ok(line):
    return line[8] in ("D", "W", "T")
