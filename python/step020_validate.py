"""STEP020 VALIDATE: split data/trans.dat into data/valid.dat and data/reject.dat.

A rejected record is written as the original line followed by its reason code,
for example ACCT0001X00001255020261120R1. RC 4 (warning) if anything was rejected.
"""
import sys

from common import RC_ERROR, RC_OK, RC_WARN, read_lines, write_lines
from rules import check


def main():
    try:
        lines = read_lines("trans.dat")
    except FileNotFoundError:
        print("VALIDATE  data/trans.dat not found")
        return RC_ERROR

    valid, rejected = [], []
    for line in lines:
        code = check(line)
        if code is None:
            valid.append(line)
        else:
            rejected.append(line + code)

    write_lines("valid.dat", valid)
    write_lines("reject.dat", rejected)
    print(f"VALIDATE  {len(valid)} valid, {len(rejected)} rejected")
    return RC_WARN if rejected else RC_OK


if __name__ == "__main__":
    sys.exit(main())
