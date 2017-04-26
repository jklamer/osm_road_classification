#Utility objects and wrappers for the project
#Jack Klamer 
import xml.sax as xml



class ElementHandler(xml.ContentHandler):
	def __init__(self):
		self.elementsProcessed=0
	def startElement(self, tag, attr):
		self.elementsProcessed+=1
		if tag == 'node':
			print('id' in attr)
		if self.elementsProcessed>100:
			exit()
	def endElement(self, tag):
		pass
	def characters(self, content):
		pass


class OsmNode:
	def __init__(self, id, lat, lon):
		self.id = id
		self.lat = lat 
		self.long = lon
		self.tags = dict()

	def getCoord(self):
		return self.lat, self.lon
	def __hash__(self):
		return hash(self.id)
	def __eq__(self, other):
		return self.id ==  other.id

class OsmWay:
	def __init__(self, id):
		self.id = id
		self.nodes = list()
		self.tags = dict()


		

