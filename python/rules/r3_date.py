"""R3: DATE (line[18:26]) must be a real calendar date in YYYYMMDD form.   << ticket VAL-2

STARTER STATUS: not implemented, so every record passes this rule.
Done when: month 13 and day 32 are rejected with R3, and 20261120 still passes.
Hint: datetime.strptime(text, "%Y%m%d") raises ValueError on a bad date.
Try it:  python python/check_record.py ACCT0001D00001255020261399
"""
from datetime import datetime
CODE = "R3"
ORDER = 30


def ok(line):
    # TODO (VAL-2): return False when line[18:26] is not a real date
    date = line[18:26]
    try:
        datetime.strptime(date, "%Y%m%d")
    except ValueError:
        return False
    return True
