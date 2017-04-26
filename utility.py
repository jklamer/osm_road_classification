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
		self.relations= set()

	def addNode(self, node):
		if not isinstance(node, OsmNode):
			raise Exception("Must add OsmNode as Node")
		if node not in self.nodes:
			self.nodes[node]=[]


	def addWay(self, way):
		if not isinstance(way, OsmWay):
			raise Exception("Must add OsmWay as way")
		if way not in self.ways:
			self.way[way] = []
			# in order to go grom way to nodes to the other connected ways
			for nd in way.nodes:
				self.nodes[nd].append(way.id)

	def addRelation(self, relation):
		if not isinstance(relation, OsmRelation ):
			raise Exception("Must add OsmRelation as Relation")
		if relation not in self.relations:
			self.relations.add(relation)



class OsmNode:
	def __init__(self, id=None, lat=None, lon=None):
		if not (id == None or lat == None or lon == None):
			self.id = int(id)
			self.lat = float(lat)
			self.long = float(lon)
		else:
			self.id = None
			self.lat = None
			self.lon = None
		self.tags = dict()

	def __hash__(self):
		return hash(self.id)

	def __eq__(self, other):
		if isinstance(other, OsmNode):
			return self.id==other.id
		return self.id == other

	def is_empty(self):
		return id != None and lat != None and lon != None

	def defineNode(self, id, lat, lon):
		self.id = id
		self.lat = lat
		self.lon = lon

	def getCoord(self):
		return self.lat, self.lon

	def addTag(self, k, v):
		self.tags[k] = v

class OsmWay:
	def __init__(self, id):
		self.id = int(id)
		self.nodes = list()
		self.tags = dict()

	def __hash__(self):
		return hash(self.id)

	def __eq__(self, other):
		if isinstance(other, OsmWay):
			return self.id == other.id
		return self.id == other

	def addTag(self, k, v):
		self.tags[k]=v

	def addNode(self, nodeId):
		self.nodes.append(nodeId)

class OsmRelation:
	def __init__(self, id):
		self.id= int(id)
		self.members=dict()
		self.tags=dict()

	def __hash__(self):
		return hash(self.id)

	def __eq__(self, other):
		if isinstance(other, OsmRelation):
			return self.id == other.id
		return self.id == other

	def addTag(self, k, v):
		self.tags[k] = v

	def addMember(self, mtype, ref, role):
		self.members[(mtype, ref)] = role
