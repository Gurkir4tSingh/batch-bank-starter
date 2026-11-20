"""Try every validation rule on ONE record. A rule that crashes shows its full error here.

    python python/check_record.py ACCT0001D00001255020261120
    python python/check_record.py "        D00001381120261107"      (quotes keep the spaces)

On a Mac, type python3 instead of python.
"""
import sys

from rules import load_rules


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 1
    line = sys.argv[1]
    print(f"record: [{line}]  ({len(line)} characters)")
    for rule in load_rules():
        passed = rule.ok(line)      # no try/except on purpose: a crash shows the real error
        print(f"  {rule.CODE}  {'pass' if passed else 'REJECT'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
