"""R4: ACCT (line[0:8]) must not be blank.                  << ticket VAL-3

STARTER STATUS: not implemented, so every record passes this rule.
Done when: a record with spaces in the first 8 characters is rejected with R4.
Hint: .strip() removes spaces from both ends of a string.
Try it:  python python/check_record.py "        D00001255020261120"   (8 spaces, in quotes)
"""
CODE = "R4"
ORDER = 40


def ok(line):
    # TODO (VAL-3): return False when the account field is blank
    return True
