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

class OsmMap:
	def __init__(self):
		self.nodes = dict()
		self.ways = dict()
		self.relations= dict()

	def addNode(self, node):
		if not isinstance(OsmNode, node):
			raise Exception("Must add OsmNode as Node")
		self.nodes[node.id]=node

	def addWay(self, way):
		if not isinstance(OsmWay, way):
			raise Exception("Must add OsmWay as way")
		self.way[way.id]=way

	def addRelation(self, relation):
		if not isinstance(OsmRelation, relation):
			raise Exception("Must add OsmRelation as Relation")
		self.relations[relation.id]=relation



class OsmNode:
	def __init__(self, id, lat, lon):
		self.id = int(id)
		self.lat = float(lat)
		self.long = float(lon)
		self.tags = dict()

	def getCoord(self):
		return self.lat, self.lon

	def __hash__(self):
		return hash(self.id)

	def __eq__(self, other):
		return self.id ==  other.id

class OsmWay:
	def __init__(self, id):
		self.id = int(id)
		self.nodes = list()
		self.tags = dict()

	def __hash__(self):
		return hash(self.id)

	def __eq__(self, other):
		return self.id ==  other.id

class OsmRelation:
	def __init__(self, id):
		self.id= int(id)
		self.members=dict()
		self.tags=dict()

	def __hash__(self):
		return hash(self.id)

	def __eq__(self, other):
		return self.id ==  other.id
