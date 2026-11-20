"""STEP050 ENCODE: convert data/master.dat to EBCDIC (code page cp037).

The output, data/master.ebcdic, has NO line breaks: every record is exactly 19 bytes,
the way fixed-length records are stored on a mainframe.

    python python/step050_encode.py --show     also print the first 3 records as text and hex
"""
import sys

from common import RC_ERROR, RC_OK, path, read_lines


def main():
    try:
        lines = read_lines("master.dat")
    except FileNotFoundError:
        print("ENCODE    data/master.dat not found")
        return RC_ERROR

    data = b"".join(line.encode("cp037") for line in lines)
    with open(path("master.ebcdic"), "wb") as f:
        f.write(data)
    print(f"ENCODE    {len(lines)} records, {len(data)} bytes -> data/master.ebcdic")

    if "--show" in sys.argv:
        for line in lines[:3]:
            print(f"  text: {line}")
            print(f"  hex : {line.encode('cp037').hex(' ')}")
    return RC_OK


if __name__ == "__main__":
    sys.exit(main())
