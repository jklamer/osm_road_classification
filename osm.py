#Utility objects and wrappers for the project
#Jack Klamer
import xml.sax as xml

class OsmDataContentHandler(xml.ContentHandler):
	def __init__(self, map, nodeRequireTags = [], nodeProhibitTags = [], wayRequireTags= [] , wayProhibitTags=[], relationRequireTags = [], relationProhibitTags=[]):
		self.elementsProcessed = 0
		self.currentElement = None
		self.currentElementObject = None
		#a list of mandatory or required tags for nodes, ways, and relations
		self.nodeRequireTags=nodeRequireTags
		self.nodeProhibitTags=nodeProhibitTags
		self.wayRequireTags = wayRequireTags
		self.wayProhibitTags = wayProhibitTags
		self.relationRequireTags = relationRequireTags
		self.relationProhibitTags = relationProhibitTags

		if not isinstance(map, OsmMap):
			raise Exception("Cannot initialize ContentHandler with type {}, must be OsmMap".format(type(map)))
		self.map = map

	def startElement(self, tag, attr):
		##handle each new xml element, current element refers to Osm element encoded in XML elements
		if tag in ['node','way','relation']:
			self.currentElement = tag

		if tag == 'node':
			self.currentElementObject = OsmNode(id = attr['id'], lat=attr['lat'], lon=attr['lon'])

		if tag == 'way':
			self.currentElementObject = OsmWay(id = attr['id'])

		if tag == 'relation':
			self.currentElementObject = OsmRelation(id = attr['id'])

		if tag == 'tag':
			self.currentElementObject.addTag(attr['k'], attr['v'])

		if tag == 'nd' and self.currentElement=='way':
			self.currentElementObject.addNode(attr['ref'])

		if tag == 'member' and self.currentElement == 'relation':
			self.currentElementObject.addMember(attr['type'], attr['ref'], attr['role'])

	def endElement(self, tag):
		if tag not in ['node','way','relation']:
			return

		if tag =='node':
			requiredSet=set(self.nodeRequireTags)
			prohibitList=self.nodeProhibitTags
		if tag == 'way':
			requiredSet=set(self.wayRequireTags)
			prohibitList=self.wayProhibitTags
		if tag == 'relation':
			requiredSet=set(self.relationRequireTags)
			prohibitList=self.relationProhibitTags

		#choosing what gets added to map based on having tags or not
		for maptag in self.currentElementObject.tags.keys():
			if maptag in prohibitList:
				return
			elif maptag in requiredSet:
				requiredSet.remove(maptag)

		#if all the required tags are there
		if not len(requiredSet):
			self.map.add(self.currentElementObject)
			self.currentElement = None
			self.currentElementObject = None

	##this shouldnt be needed if properly formatted osm xml
	def characters(self, content):
		pass

class OsmMap:
	def __init__(self, includeNodes=True, includeWays=True, includeRelations=True):
		self.nodes = dict()
		self.ways = dict()
		self.relations= set()
		self.nodeString='node'
		self.wayString='way'
		self.relationString='relation'
		self.includeNodes=includeNodes
		self.includeWays=includeWays
		self.includeRelations=includeRelations

	def printMap(self, file=None):
		for node in self.nodes.keys():
			print(node, file=file)
		for way in self.ways.keys():
			print(way, file=file)
		for relation in self.relations:
			print(relation, file=file)

	def add(self, element):
		if isinstance(element, OsmNode):
			if self.includeNodes:
				self.addNode(element)
			return
		if isinstance(element, OsmWay):
			if self.includeWays:
				self.addWay(element)
			return
		if isinstance(element, OsmRelation):
			if self.includeRelations:
				self.addRelation(element)
			return
		raise Exception("{} is not an OSM element".format(type(element)))

	def addNode(self, node):
		if not isinstance(node, OsmNode):
			raise Exception("Must add OsmNode as node")
		if node not in self.nodes:
			self.nodes[node.id]=node

	def addWay(self, way):
		if not isinstance(way, OsmWay):
			raise Exception("Must add OsmWay as way")
		if way not in self.ways:
			self.ways[way.id] = way
			# in order to go grom way to nodes to the other connected ways
			for nd in way.nodes:
				self.nodes[nd].addSuperStruct(way.id,self.wayString)


	def addRelation(self, relation):
		if not isinstance(relation, OsmRelation ):
			raise Exception("Must add OsmRelation as relation")
		if relation not in self.relations:
			self.relations.add(relation)
			for structtype , id in relation.members.keys():
				if structtype == self.nodeString:
					self.nodes[id].addSuperStruct(relation.id, self.relationString)
				if structtype == self.wayString:
					self.ways[id].addSuperStruct(relation.id, self.relationString)




class OsmNode:
	def __init__(self, id=None, lat=None, lon=None):
		if not (id == None or lat == None or lon == None):
			self.id = int(id)
			self.lat = float(lat)
			self.lon = float(lon)
		else:
			self.id = None
			self.lat = None
			self.lon = None
		self.tags = dict()
		self.superStructs = dict()

	def __hash__(self):
		return hash(self.id)

	def __eq__(self, other):
		if isinstance(other, OsmNode):
			return self.id==other.id
		return self.id == other

	def __str__(self):
			return "Node #{}, lat={} , lon={}\n    Tags:{}".format(self.id, self.lat, self.lon, self.tags)

	def is_empty(self):
		return self.id != None and self.lat != None and self.lon != None

	def defineNode(self, id, lat, lon):
		self.id = id
		self.lat = lat
		self.lon = lon

	def getCoord(self):
		return self.lat, self.lon

	def addTag(self, k, v):
		self.tags[k] = v

	def addSuperStruct(self, id, structtype):
		if structtype not in self.superStructs:
			self.superStructs[structtype]=[]
		self.superStructs[structtype].append(id)

class OsmWay:
	def __init__(self, id=0):
		self.id = int(id)
		self.nodes = list()
		self.tags = dict()
		self.superStructs = dict()

	def __hash__(self):
		return hash(self.id)

	def __eq__(self, other):
		if isinstance(other, OsmWay):
			return self.id == other.id
		return self.id == other

	def __str__(self):
		return "Way #{}\n    Nodes:{}\n    Tags:{}".format(self.id,self.nodes,self.tags)

	def addTag(self, k, v):
		self.tags[k] = v

	def addNode(self, nodeId):
		self.nodes.append(int(nodeId))

	def addSuperStruct(self, id, structtype):
		if structtype not in self.superStructs:
			self.superStructs[structtype]=[]
		self.superStructs[structtype].append(id)

class OsmRelation:
	def __init__(self, id=0):
		self.id= int(id)
		self.members = dict()
		self.tags = dict()

	def __hash__(self):
		return hash(self.id)

	def __eq__(self, other):
		if isinstance(other, OsmRelation):
			return self.id == other.id
		return self.id == other

	def __str__(self):
		return "Relation #{}\n    Members:{}\n    Tags:{}".format(self.id,self.members,self.tags)


	def addTag(self, k, v):
		self.tags[k] = v

	def addMember(self, mtype, ref, role):
		self.members[(mtype, int(ref))] = role
