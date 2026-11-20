"""Report section: summary counts and the total of all balances. (Working in the starter.)

Tickets RPT-1, RPT-2 and RPT-3 each add their OWN file next to this one, for example
s10_totals_by_type.py. Copy this file's shape: a section(ctx) function that returns lines.
"""
from common import money


def section(ctx):
    total = sum(ctx["master"].values())
    return [
        "SUMMARY",
        f"  Transactions read : {len(ctx['trans'])}",
        f"  Valid             : {len(ctx['valid'])}",
        f"  Rejected          : {len(ctx['reject'])}",
        f"  Accounts          : {len(ctx['master'])}",
        f"  Total balance     : {money(total)}",
    ]
