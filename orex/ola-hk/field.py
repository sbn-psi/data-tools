import struct

FORMATS = {"UnsignedMSB2":">H",
           "UnsignedLSB2":"<H",
           "UnsignedMSB4":">I", 
           "UnsignedLSB4":"<I",
           "SignedMSB2":">h",
           "SignedLSB2":"<h",
           "SignedMSB4":">i",
           "SignedLSB4":"<i",
           "UnsignedByte":">B" 
 }

class Field:
    def __init__(self, name, location, length, datatype):
        self.name = name
        self.location = location
        self.length = length
        self.datatype = datatype

    def extract(self, record):
        fbytes = record[self.location-1:self.location+self.length-1]
        return struct.unpack(FORMATS[self.datatype], fbytes)[0]
