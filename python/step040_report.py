"""STEP040 REPORT: build data/report.txt from the files in python/report_sections/.

ONE FILE PER SECTION, so teammates never edit the same file. Each section file defines:

    def section(ctx) -> list of text lines

Files run in name order (s00_..., s10_..., s20_...). To add a section, add a file.
ctx is a dict with:
    ctx["trans"]   every line of data/trans.dat
    ctx["valid"]   every line of data/valid.dat
    ctx["reject"]  every line of data/reject.dat (original record + reason code)
    ctx["master"]  {account: balance in cents} from data/master.dat

A section that crashes is reported in the file and the step ends with RC 4.
"""
import glob
import importlib.util
import os
import sys

from common import RC_ERROR, RC_OK, RC_WARN, read_lines, read_master, write_lines

SECTIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "report_sections")


def load_sections():
    loaded = []
    for file in sorted(glob.glob(os.path.join(SECTIONS, "s*.py"))):
        name = os.path.splitext(os.path.basename(file))[0]
        spec = importlib.util.spec_from_file_location(name, file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "section"):
            loaded.append((name, module))
    return loaded


def main():
    try:
        ctx = {
            "trans": read_lines("trans.dat"),
            "valid": read_lines("valid.dat"),
            "reject": read_lines("reject.dat"),
            "master": read_master("master.dat"),
        }
    except FileNotFoundError as e:
        print(f"REPORT    missing input file: {os.path.basename(e.filename)}")
        return RC_ERROR

    out = ["BATCH BANK DAILY REPORT", "=" * 23, ""]
    rc = RC_OK
    count = 0
    for name, module in load_sections():
        try:
            out += module.section(ctx)
        except Exception as e:
            out += [f"[section {name} failed: {e}]"]
            rc = RC_WARN
        out.append("")
        count += 1

    write_lines("report.txt", out)
    print(f"REPORT    data/report.txt written ({count} section{'' if count == 1 else 's'})")
    return rc


if __name__ == "__main__":
    sys.exit(main())
