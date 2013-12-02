#!/usr/bin/env python3

from struct import unpack

MBR = {
    "Bootstrap": (0x000, 446),
    "Partition 1": (0x1BE, 16),
    "Partition 2": (0x1CE, 16),
    "Partition 3": (0x1DE, 16),
    "Partition 4": (0x1EE, 16),
    "Sig 55h": (0x1FE, 1),
    "Sig AAh": (0x1FF, 1)
}

# addresses are relative
PARTITION = {
    "Status": (0x0, 1),
    "CHS address first": (0x1, 3),
    "Type": (0x4, 1),
    "CHS last": (0x4, 3),
    "LBA first": (0x8, 4),
    "Sectors": (0xC, 4)
}
PARTITION_STATUS = {
    0x00: "inactive",
    0x80: "bootable"
}


def parse(code, struct):
    """ Generic parse function.

    :param binary code: Binary code which should be parsed
    :param dict struct: Dictionary to describe which values should be fetched.
    A single entry always consists as a name as the dict index and the value is
    a slice containing starting address and lengt (e.g. (0x01, 3) ).

    :return: Dictionaries with the indexes from struct but with a mapped value
    :rtype: dict

    """

    result = {}
    for property in struct:
        (start, length) = struct[property]
        end = start + length
        result.update({
            property:
            unpack("<%iB" % length, code[start:end])
        })
    return result


def parse_mbr(mbr_code):
    return parse(mbr_code, MBR)


def parse_partition(partition_code):
    return parse(partition_code, PARTITION)

if __name__ == "__main__":
    with open('/dev/sda', 'rb') as hdd:
        mbr_bin = hdd.read(513)

    mbr = parse_mbr(mbr_bin)
    for entry in mbr:
        if not entry is "Bootstrap":
            print("%+20s %08x" % (entry, mbr[entry]))
