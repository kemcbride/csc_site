""" This is copy-pasta'd from...
http://www.austintaylor.io/lxml/python/pandas/xml/dataframe/2016/07/08/convert-xml-to-pandas-dataframe/
"""

import xml.etree.ElementTree as ET
import pandas as pd

class XML2DataFrame:

    def __init__(self, xml_data):
        self.root = ET.XML(xml_data)

    def parse_root(self, root):
        """Return a list of dictionaries from the text
         and attributes of the children under this XML root."""
        return [self.parse_element(child) for child in iter(root)]

    def parse_element(self, element, parsed=None):
        """ Collect {key:attribute} and {tag:text} from thie XML
         element and all its children into a single dictionary of strings."""
        if parsed is None:
            parsed = dict()

        for key in element.keys():
            if key not in parsed:
                parsed[key] = element.attrib.get(key)
            else:
                raise ValueError('duplicate attribute {0} at element {1}'.format(key, element.getroottree().getpath(element)))

        for child in list(element):
            self.parse_element(child, parsed)

        return parsed

    def process_data(self):
        """ Initiate the root XML, parse it, and return a dataframe"""
        structure_data = self.parse_root(self.root)
        return pd.DataFrame(structure_data)
