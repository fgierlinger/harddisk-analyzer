""" Definitions for reading the bootsector of different partition types. """
from struct import unpack


class Partition:
    def _unpack_2_hex(self, hex_tuple):
        """ Convert the unpack tuple to a hex value. """
        result = 0x00
        for hex in hex_tuple:
            result = result << 8 | hex
        return result

    def __init__(self, codes, bincode):
        """ Takes the given codes and creates attributes from it. 

        The codes should be a dict with the attribute name as key and a tuple 
        as value. The tuple should have the following type:
        (start-address,
         end-address,
         ( start-constraint,
           end-constraint)
        )
        The start and end-constraint help to verify if a specific value has to 
        be set. They are optional

        :param codes: Dict with attributes to create
        :param bincode: The code where the attributes should be fetched from.
    
        """
        for attr in codes:
            (start, end, constraints) = codes[attr]
            setattr(self, attr, bincode[start:end])


    def __setattr__(self, name, value):
        self.__dict__.update({name: self._unpack_2_hex(value)})

    def __getattr__(self,name):
        return self.__dict__.get(name)

    def __str__(self):
        output = ""
        for name  in sorted(self.__dict__.keys()):
            output += "%30s %s\n" % (name, getattr(self, name))
        return output

    def _print_hex(self, value):
        return "0x%08X" % value


class FAT32(Partition):

    vbr = {
            "bootloader": (0x00, 0x03,(None,None)),
            "system_name": (0x03, 0x08,(None,None)),
            "bytes_per_sector": (0x0B, 0x0D,(None,None)),
            "sector_per_cluster": (0x0D, 0x0E,(None,None)),
            "reserved_sectors": (0x0E, 0x10,(None,None)),
            "fat_amount": (0x10, 0x11, (2,2)),
            "max_entries": (0x11,0x13, (0,0)),
            "sector_count": (0x13,0x15, (0,0)),
            "type": (0x15, 0x16, (0xF8, 0xFF)),
            "sector_amount": (0x16, 0x18, (0,0)),
            "int13_sector_per_track": (0x18, 0x1A,(None,None)),
            "int13_head_count": (0x1A, 0x1C,(None,None)),
            "hidden_sectors": (0x1C, 0x20,(None,None)),
            "sector_amount_ext": (0x20, 0x24,(None,None)),
            "fat32_sector_per_fat": (0x24, 0x28,(None,None)),
            "fat32_bitswitch": (0x28, 0x2A,(None,None)),
            "fat32_partition_version": (0x2A, 0x2C,(None,None)),
            "fat32_cluster_start": (0x2C, 0x30,(None,None)),
            "fat32_sectornumber": (0x30, 0x32,(None,None)),
            "fat32_vbr_copy_begin": (0x32, 0x34,(None,None)),
            "fat32_int13_drive_number": (0x40, 0x41,(None,None)),
            "fat32_extended_boot_sig": (0x42, 0x43,(None,None)),
            "fat32_volume_id": (0x43, 0x47,(None,None)),
            "fat32_volume_name": (0x47, 0x52,(None,None)),
            "reserved_0000": (0x1FC, 0x1FE, (0x0000,0x0000)),
            "signature": (0x1FE, 0x200, (0x55AA, 0x55AA))
            }
    

    def __init__(self, code):
        super().__init__(self.vbr, code)

    @property
    def system_name(self):
        return "%s" % self.__getattr__("system_name")

    @property
    def fat32_cluster_start(self):
        return self._print_hex(self.__getattr__("fat32_cluster_start"))


if __name__ == '__main__':
    with open('./fat32.img', 'rb') as hdd:
        code = hdd.read(0x200)

    fat = FAT32(code)

    print(fat)
