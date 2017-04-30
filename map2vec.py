import sys
import xml.sax as xml
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import datetime
from osm import *
usage="USAGE: map2vec.py INPUTS -o OUTPUTS"

if len(sys.argv)== 1 or sys.argv[1] == '-h' or sys.argv[1] == '--help':
	print(usage)
	exit()

if __name__ == "__main__":

	inputs=[]
	outputs=[]
	#parse inputs
	parsingInputs= True
	for arg in sys.argv[1:]:
		if arg == '-o':
			parsingInputs=False
		elif parsingInputs:
			inputs.append(arg)
		else:
			outputs.append(arg)

	if len(inputs) != len(outputs):
		print(usage)
		print("Number of outputs must equal number of inputs")

	#init the parsing object
	MapParser = xml.make_parser()
	MapParser.setFeature(xml.handler.feature_namespaces, 0)

	for i in range(len(inputs)):
		#create specific handler for each map
		map = OsmMap(includeRelations=False)
		myHandler = OsmDataContentHandler(map, wayRequireTags=['highway'])
		MapParser.setContentHandler(myHandler)
		MapParser.parse(open(inputs[i]))
		# #map.printMap(file = open(outputs[i],'w'))
		# classCounts={}
		# for way in map.ways.keys():
		# 	klass = way.tags['highway']
		# 	if klass not in classCounts:
		# 		classCounts[klass] = 0
		# 	classCounts[klass] += 1


		# print(inputs[i])
		# for roadType in sorted(list(classCounts.keys())):
		# 	print("{}: {}".format(roadType, classCounts[roadType]))

		del(map)
