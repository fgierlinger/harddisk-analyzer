#!/usr/bin/env python3

from partitions import MBR

if __name__ == "__main__":
    from sys import argv
    with open(argv[1], 'rb') as hdd:
        hdd.seek(0)
        mbr_bin = hdd.read(512)

    mbr = MBR(mbr_bin)

    print(mbr)
