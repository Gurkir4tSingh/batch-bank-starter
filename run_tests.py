#!/usr/bin/env python3
"""Run every test: the Python tests (pytest) and the Java tests (TestRunner).

    python run_tests.py        (on a Mac: python3 run_tests.py)

Needs pytest once:  pip install pytest   (Mac: pip3 install pytest)
"""
import glob
import importlib.util
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT, "java", "out")


def python_tests():
    print("== Python tests ==")
    if importlib.util.find_spec("pytest") is None:
        print("pytest is not installed. Run:  pip install pytest")
        return False
    rc = subprocess.run([sys.executable, "-m", "pytest", "-q", "python/tests"], cwd=ROOT).returncode
    return rc == 0


def java_tests():
    print("== Java tests ==")
    javac, java = shutil.which("javac"), shutil.which("java")
    if not javac or not java:
        print("javac or java not found. Install JDK 17 or newer, then reopen the terminal.")
        return False
    os.makedirs(OUT_DIR, exist_ok=True)
    sources = sorted(glob.glob(os.path.join(ROOT, "java", "*.java")))
    sources += sorted(glob.glob(os.path.join(ROOT, "java", "tests", "*.java")))
    if subprocess.run([javac, "-d", OUT_DIR] + sources, cwd=ROOT).returncode != 0:
        print("Java did not compile.")
        return False
    return subprocess.run([java, "-cp", OUT_DIR, "TestRunner"], cwd=ROOT).returncode == 0


def main():
    results = [python_tests(), java_tests()]
    print("ALL TESTS PASSED" if all(results) else "SOME TESTS FAILED")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()
