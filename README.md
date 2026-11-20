# Batch Bank in a Box

A tiny mainframe-style **batch job** written in Java and Python. It reads fixed-width bank
transactions, validates them, posts them to account balances, writes a report, and converts the
result to **EBCDIC**, the character encoding mainframes use. Built at a StackFrame workshop.

You do not need mainframe experience, Linux, or any extra tools: just VS Code, Python 3.8 or newer, a JDK (17 or newer) and Git.

## How to run

Open this folder in VS Code, open a terminal (Terminal menu, New Terminal), and run:

```
python run_pipeline.py
```

On a **Mac**, type `python3` instead of `python`. On **Windows**, `python` or `py` both work.

You should see something like this, and the last line must say `JOB MAXRC=0000`:

```
STEP010 RC=0000  GENERATE  200 records -> data/trans.dat
STEP020 RC=0000  VALIDATE  200 valid, 0 rejected
STEP030 RC=0000  POST      177 posted, 0 skipped
STEP040 RC=0000  REPORT    data/report.txt written (1 section)
STEP050 RC=0000  ENCODE    10 records, 190 bytes -> data/master.ebcdic
JOB MAXRC=0000
```

What matters: five steps, all `RC=0000`. (Transfers are not posted yet, which is why 23 of the 200 records
are not counted as posted. That is ticket JAV-2.)

Other ways to run it:

| Command | What it does |
| --- | --- |
| `python run_pipeline.py --dirty` | The generator damages 10 of 200 records, so your rules have something to catch |
| `python run_pipeline.py --sample` | Uses `data/sample_trans.dat` (the small hand-written file) instead of generating |
| `python run_pipeline.py --input FILE` | Uses any transaction file you point it at |
| `python run_tests.py` | Runs the Python tests (pytest) and the Java tests. Needs `pip install pytest` once |
| `python python/step050_encode.py --show` | Shows records as text next to their EBCDIC bytes |
| `python python/check_record.py "<record>"` | Tries every validation rule on one record. Shows the full error if a rule crashes |

## What it does

```
STEP010 GENERATE  ->  data/trans.dat
STEP020 VALIDATE  ->  data/valid.dat + data/reject.dat
STEP030 POST      ->  data/master.dat        (Java)
STEP040 REPORT    ->  data/report.txt
STEP050 ENCODE    ->  data/master.ebcdic
```

Every step reads a file and writes a file. Python and Java only talk through files, so
different people can work on different steps at the same time.

## Return codes

Every step ends with a number, like a mainframe job.

| RC | Meaning | What the job does |
| --- | --- | --- |
| 0 | OK | Continue |
| 4 | Warning (some records rejected or skipped) | Continue |
| 8 | Error (for example, a missing file) | Stop the job |
| 12 | Severe (a step crashed) | Stop the job |

The job ends with `JOB MAXRC=` and the highest code any step returned.

## Record layouts

Fixed width: no commas, no JSON. Every field is at an exact position.

| File | Layout | Example |
| --- | --- | --- |
| Transaction (26 characters) | `ACCT`(8) `TYPE`(1) `AMOUNT`(9) `DATE`(8) | `ACCT0001D00001255020261120` |
| Master (19 characters) | `ACCT`(8) `BALANCE`(11) | `ACCT000100000050000` |
| Reject | the original line + reason code(2) | `ACCT0001X00001255020261120R1` |

- `TYPE`: `D` deposit, `W` withdrawal, `T` transfer out.
- `AMOUNT` and `BALANCE` are in **cents**: `000012550` is $125.50. A balance can start with `-` if it is overdrawn.
- `DATE`: `YYYYMMDD`.
- Reason codes: `R1` bad type, `R2` non-numeric amount, `R3` bad date, `R4` blank account, `R5` wrong length.

## Where things live

| Folder or file | What is in it |
| --- | --- |
| `run_pipeline.py` | The job runner |
| `python/rules/` | **One file per validation rule.** Add a rule by adding a file |
| `python/report_sections/` | **One file per report section.** Add a section by adding a file |
| `python/step0*.py` | The Python steps |
| `java/Step030Post.java`, `java/Transaction.java` | The Java step and the record class |
| `python/tests/`, `java/tests/` | Tests |
| `data/` | Input data, and the files the pipeline generates (these are not committed) |
| `docs/`, `GLOSSARY.md`, `TESTING.md` | Documentation tickets |

## Your first contribution

1. Pick **one** ticket (an issue) with a label for your level: `L1` no code, `L2` some code, `L3` challenge.
   Comment "me" on it and assign yourself.
2. Get the latest code and make a branch:
   ```
   git checkout main
   git pull
   git checkout -b VAL-1-yourname
   ```
3. Make your change. Test it:
   ```
   python run_pipeline.py --dirty
   python run_tests.py
   ```
4. Save it:
   ```
   git add -A
   git commit -m "VAL-1: reject non-numeric amounts (R2)"
   git push -u origin VAL-1-yourname
   ```
5. On GitHub click **Compare & pull request**. Start the title with your ticket ID, write `Closes #<issue number>`
   in the description, and ask your team's **merge captain** to review it.

You can also use VS Code's **Source Control** panel instead of typing the commit and push commands.

**No write access?** Fork the repository on GitHub, clone your fork, follow the same steps, and open the pull
request from your fork.

**Merge conflict?** Run `git checkout main`, `git pull`, `git checkout <your branch>`, then `git merge main`. Open the
conflicted file in VS Code and click Accept Incoming, Accept Current or Accept Both. Save, run the pipeline again,
commit and push. Ask an organizer if it takes more than 5 minutes.

## Rules that keep merges easy

- Validation rules and report sections are **one file each**. Do not edit someone else's file.
- Only ticket **DOC-5** edits the "How to run" section of this README.
- Do not commit generated files from `data/`. The `.gitignore` already stops most of them.

## What is missing on purpose

This is a starter, so some things are tickets, not bugs:

- Validation rules R2, R3 and R4 let everything through. (VAL-1, VAL-2, VAL-3)
- Transfers (`T`) are read but not posted. (JAV-2)
- A withdrawal can push a balance below zero. (JAV-3)
- The report only has a summary. (RPT-1, RPT-2, RPT-3)
- There is no Java EBCDIC encoder. (JAV-4)
- Most tests, the glossary and the diagram are empty. (QA, DOC tickets)

With the starter alone, `--dirty` ends with `JOB MAXRC=0004`, because some damaged records get through to the Java step and are skipped there with a warning.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `python` is not found | Windows: try `py run_pipeline.py`. Mac: use `python3` |
| `javac` is not found | Install JDK 17 or newer, then close and reopen the terminal |
| `RC=0008` at STEP030 | Read the message after it. Usually a typo in a Java file, or you ran it from the wrong folder (run from the repo root) |
| `git push` says permission denied | Use the fork route above |
| Records look the wrong length | Line endings. VS Code, bottom right: switch **CRLF** to **LF** and save |
