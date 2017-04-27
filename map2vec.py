import sys
import xml.sax as xml
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import datetime
from osm import *



if __name__ == "__main__":

	#init the object
	MapParser = xml.make_parser()
	MapParser.setFeature(xml.handler.feature_namespaces, 0)

	#create specific handler for each map
	map = OsmMap()
	myHandler = OsmDataContentHandler(map, wayRequireTags=['highway'])
	MapParser.setContentHandler(myHandler)
	MapParser.parse(open("data/reykjavik_iceland.osm"))
	map.printMap(file = open("reykjavik_iceland.txt",'w'))
