import struct

FORMATS = {"UnsignedMSB2":">H", "UnsignedMSB4":">I", "UnsignedByte":">B", "SignedMSB4":">f"}

class Field:
    def __init__(self, name, location, length, datatype):
        self.name = name
        self.location = location
        self.length = length
        self.datatype = datatype

    def extract(self, record):
        fbytes = record[self.location-1:self.location+self.length-1]
        return struct.unpack(FORMATS[self.datatype], fbytes)[0]
