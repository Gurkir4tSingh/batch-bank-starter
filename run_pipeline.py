#!/usr/bin/env python3
"""Batch Bank in a Box: the job runner (a tiny stand-in for JCL).

Runs five steps in order and prints a return code (RC) for each one.
RC 0 = ok, 4 = warning, 8 = error, 12 = severe. The job halts at RC 8 or higher.

Usage:
    python run_pipeline.py                 clean run, 200 generated records
    python run_pipeline.py --dirty         the generator injects 5% bad records
    python run_pipeline.py --sample        use data/sample_trans.dat instead of generating
    python run_pipeline.py --input FILE    use any transaction file instead of generating

On a Mac, type python3 instead of python. On Windows, python or py both work.
Exit status: 0 when the job finishes (MAXRC 0 or 4), otherwise the failing RC.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
HALT_AT = 8
OUT_DIR = os.path.join(ROOT, "java", "out")


def clean(lines):
    """Drop the noise some JDK setups print before the real message."""
    return [l for l in lines if l.strip() and not l.startswith("Picked up")]


def run(cmd):
    """Run a command from the repo root. Returns (exit code, stdout lines, stderr lines)."""
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return p.returncode, clean(p.stdout.splitlines()), clean(p.stderr.splitlines())


def python_step(cmd):
    rc, out, err = run(cmd)
    if rc not in (0, 4, 8, 12):
        # A crash (traceback) is a severe error.
        rc = 12
        out = out + ["crashed: " + (err[-1] if err else "unknown error")]
    return rc, out


def java_step():
    javac, java = shutil.which("javac"), shutil.which("java")
    if not javac or not java:
        return 8, ["POST      javac or java not found. Install JDK 17 or newer, then reopen the terminal."]
    os.makedirs(OUT_DIR, exist_ok=True)
    sources = sorted(glob.glob(os.path.join(ROOT, "java", "*.java")))
    rc, out, err = run([javac, "-d", OUT_DIR] + sources)
    if rc != 0:
        first = (err or out or ["unknown compile error"])[0]
        first = first.replace(ROOT + os.sep, "")      # show java/Broken.java, not the full path
        return 8, ["POST      javac failed: " + first]
    rc, out, err = run([java, "-cp", OUT_DIR, "Step030Post"])
    if rc not in (0, 4, 8, 12):
        rc = 12
        out = out + ["POST      crashed: " + (err[0] if err else "unknown error")]
    return rc, out


def main():
    ap = argparse.ArgumentParser(description="Run the Batch Bank pipeline.")
    ap.add_argument("--dirty", action="store_true", help="inject 5%% bad records")
    group = ap.add_mutually_exclusive_group()
    group.add_argument("--sample", action="store_true", help="use data/sample_trans.dat")
    group.add_argument("--input", metavar="FILE", help="use this transaction file")
    args = ap.parse_args()

    gen = [PY, "python/step010_generate.py"]
    if args.dirty:
        gen.append("--dirty")
    if args.sample:
        gen += ["--input", "data/sample_trans.dat"]
    elif args.input:
        gen += ["--input", args.input]

    steps = [
        ("STEP010", lambda: python_step(gen)),
        ("STEP020", lambda: python_step([PY, "python/step020_validate.py"])),
        ("STEP030", java_step),
        ("STEP040", lambda: python_step([PY, "python/step040_report.py"])),
        ("STEP050", lambda: python_step([PY, "python/step050_encode.py"])),
    ]

    maxrc = 0
    for step_id, action in steps:
        rc, lines = action()
        maxrc = max(maxrc, rc)
        first = lines[0] if lines else ""
        print(f"{step_id} RC={rc:04d}  {first}")
        for extra in lines[1:]:
            print(" " * 18 + extra)
        if rc >= HALT_AT:
            print(f"JOB HALTED at {step_id}")
            break
    print(f"JOB MAXRC={maxrc:04d}")
    sys.exit(0 if maxrc < HALT_AT else maxrc)


if __name__ == "__main__":
    main()
