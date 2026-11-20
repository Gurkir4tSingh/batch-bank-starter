"""Shared constants and helpers for the Python steps."""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

# Record layouts. Every record is fixed width with no delimiters.
TRANS_LEN = 26    # ACCT(8) TYPE(1) AMOUNT(9, cents) DATE(8)
MASTER_LEN = 19   # ACCT(8) BALANCE(11, cents, may start with a minus sign)

# Return codes (the mainframe convention).
RC_OK, RC_WARN, RC_ERROR, RC_SEVERE = 0, 4, 8, 12


def path(filename):
    """Full path of a file inside the data folder."""
    return os.path.join(DATA, filename)


def read_path(full_path):
    """Read a text file as a list of records. Strips \\r\\n so Windows line endings
    never change a record's length, and skips completely empty lines."""
    with open(full_path, "r", encoding="utf-8", newline="") as f:
        lines = [line.rstrip("\r\n") for line in f]
    return [line for line in lines if line != ""]


def read_lines(filename):
    return read_path(path(filename))


def write_lines(filename, lines):
    """Write records one per line with plain \\n endings, on every operating system."""
    with open(path(filename), "w", encoding="utf-8", newline="\n") as f:
        for line in lines:
            f.write(line + "\n")


def read_master(filename="master.dat"):
    """Return {account: balance in cents} from a master file."""
    master = {}
    for line in read_lines(filename):
        master[line[0:8]] = int(line[8:19])
    return master


def money(cents):
    """Format cents as dollars: 12550 -> $125.50, -50 -> -$0.50."""
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}${cents // 100:,}.{cents % 100:02d}"
