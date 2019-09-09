import sys

from bs4 import BeautifulSoup
import field

def to_field(tag):
    return field.Field(
        tag.find("name").string, 
        int(tag.field_location.string),
        int(tag.field_length.string),
        tag.data_type.string
    )

class Extractor:
    def __init__(self, labelfile):
        with open(labelfile) as infile:
            soup = BeautifulSoup(infile, "lxml-xml")

        self.fields = [to_field(tag) for tag in soup.find_all("Field_Binary") if tag.data_type.string in field.FORMATS.keys()]
        self.record_length = int(soup.find("record_length").string)

        print(",".join([f.name for f in self.fields]))

    def keys(self):
        return [x[:-2] for x in self.fields if x.endswith("_x")]

    def extract_record(self, record):
        if (len(record) < self.record_length):
          raise Exception("undersized record")

        result = {}
        for f in self.fields:
            result[f.name] = f.extract(record)
        return result

def main():
    e = Extractor("l0label.xml")
    print(e.record_length)
    print([f.name for f in e.fields])

if __name__ == "__main__":
    sys.exit(main())