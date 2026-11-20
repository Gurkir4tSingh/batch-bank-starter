"""STEP010 GENERATE: write data/trans.dat.

    python python/step010_generate.py                 200 clean records (seed 2026)
    python python/step010_generate.py --dirty         same, but every 20th record is damaged
    python python/step010_generate.py --input FILE    copy FILE to data/trans.dat instead

Clean mode never overdraws an account, so a clean run ends with JOB MAXRC=0000.
Dirty mode damages exactly 10 of 200 records (2 of each kind) so rules can be tested:
    kind 0: bad type (R1)    kind 1: non-numeric amount (R2)    kind 2: bad date (R3)
    kind 3: blank account (R4)    kind 4: wrong length (R5)
"""
import argparse
import os
import random
import sys

from common import ROOT, RC_ERROR, RC_OK, read_master, read_path, write_lines

COUNT = 200
SEED = 2026


def make_clean(rng, balances):
    accounts = sorted(balances)
    lines = []
    for i in range(COUNT):
        acct = rng.choice(accounts)
        date = f"202611{1 + (i * 20) // COUNT:02d}"          # 20261101 to 20261120
        roll = rng.random()
        kind = "D" if roll < 0.45 else ("W" if roll < 0.85 else "T")
        if kind != "D" and balances[acct] < 1000:
            kind = "D"                                       # never overdraw
        if kind == "D":
            amount = rng.randrange(1000, 50001)
            balances[acct] += amount
        else:
            amount = rng.randrange(1000, min(50000, balances[acct]) + 1)
            balances[acct] -= amount                         # T counts as money out
        lines.append(f"{acct}{kind}{amount:09d}{date}")
    return lines


def damage(line, kind):
    if kind == 0:
        return line[:8] + "X" + line[9:]                     # bad type
    if kind == 1:
        return line[:9] + "00001A550" + line[18:]            # non-numeric amount
    if kind == 2:
        return line[:18] + "20261399"                        # month 13, day 99
    if kind == 3:
        return " " * 8 + line[8:]                            # blank account
    return line[:24]                                         # wrong length


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dirty", action="store_true")
    ap.add_argument("--input")
    args = ap.parse_args()

    if args.input:
        source = args.input if os.path.isabs(args.input) else os.path.join(ROOT, args.input)
        if not os.path.exists(source):
            print(f"GENERATE  input file not found: {args.input}")
            return RC_ERROR
        lines = read_path(source)
        write_lines("trans.dat", lines)
        print(f"GENERATE  {len(lines)} records from {args.input} -> data/trans.dat")
        return RC_OK

    rng = random.Random(SEED)
    lines = make_clean(rng, read_master("master_in.dat"))
    damaged = 0
    if args.dirty:
        for i in range(7, COUNT, 20):
            lines[i] = damage(lines[i], damaged % 5)
            damaged += 1
    write_lines("trans.dat", lines)
    note = f" ({damaged} damaged)" if args.dirty else ""
    print(f"GENERATE  {len(lines)} records{note} -> data/trans.dat")
    return RC_OK


if __name__ == "__main__":
    sys.exit(main())
