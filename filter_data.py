import sys
import xml.sax as xml
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import datetime
from utility import *



if __name__ == "__main__":

	MapParser = xml.make_parser()
	MapParser.setFeature(xml.handler.feature_namespaces, 0)

	myHandler = ElementHandler()
	MapParser.setContentHandler(myHandler)

	MapParser.parse(open("data/reykjavik_iceland.osm"))
