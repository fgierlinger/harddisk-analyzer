#!/usr/bin/env python3

from struct import unpack
from partitions import Partition

class MBR(Partition):
    codes = {
            "bootstrap": (0x000, 0x1BE, (None, None),),
            "signature": (0x1FE, 0x200, (0x55AA, 0x55AA)),
    }
    _partitions = []

    def __init__(self, mbr_bin):
        super().__init__(self.codes, mbr_bin)

        for i in range(0, 4):
            start = 0x1BE + 0x10 * i
            end = start + 0x10
            self._partitions.append(Subpartition(mbr_bin[start:end]))

    @property
    def partitions(self):
        return self._partitions

    @partitions.setter
    def partitions(self, value):
        self._partitions.append(value)

    @property
    def signature(self):
        return self.__getattr__("signature") == 0x55AA

    def __str__(self):
        output = super().__str__()
        for i in range(0, len(self._partitions)):
            partition = self._partitions[i]
            output += 30*"="+" Partition %i\n" % i
            output += partition.__str__()
        return output



class Subpartition(Partition):
    code = {
            "status": (0x0, 0x1, (0x00, 0xFF)),
            "CHS_address_first": (0x4, 0x7, (None, None)),
            "type": (0x4, 0x5, (0x00, 0xFF)),
            "CHS_address_last": (0x5, 0x8, (None, None)),
            "LBA_address_first": (0x8, 0xC, (None, None)),
            "sectors_count": (0xC, 0x10, (None, None))
    }

    TYPE = {0x07: "NTFS", 0x0B: "FAT32", 0x83: "Linux"}

    def __init__(self, vba_bin):
        super().__init__(self.code, vba_bin)
        

    @property
    def type(self):
        type_ = self.__getattr__("type")
        try:
            return self.TYPE[type_]
        except KeyError:
            return "Unknown (0x%X)" % type_

    @property
    def CHS_address_first(self):
        return self._print_hex(self.__getattr__("CHS_address_first"))

    @property
    def CHS_address_last(self):
        return self._print_hex(self.__getattr__("CHS_address_last"))

    @property
    def LBA_address_first(self):
        return self._print_hex(self.__getattr__("LBA_address_first"))
                    


if __name__ == "__main__":
    from sys import argv
    with open(argv[1], 'rb') as hdd:
        hdd.seek(0)
        mbr_bin = hdd.read(512)

    mbr = MBR(mbr_bin)

    print(mbr)
