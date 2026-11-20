import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from rules import check  # noqa: E402


def test_valid_record_passes_every_rule():
    # A good record: ACCT0001, deposit, $125.50, 2026-11-20
    assert check("ACCT0001D00001255020261120") is None
