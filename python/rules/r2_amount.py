"""R2: AMOUNT (line[9:18]) must be nine digits.            << ticket VAL-1

STARTER STATUS: not implemented, so every record passes this rule.
Done when: ACCT0001D0000A255020261120 is rejected with R2 and good records still pass.
Hint: a string method that tells you whether every character is a digit.
Try it:  python python/check_record.py ACCT0001D0000A255020261120
"""
CODE = "R2"
ORDER = 20


def ok(line):
    # TODO (VAL-1): return False when line[9:18] is not all digits
    return True
