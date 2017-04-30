#vectorizing only the proncipal highways
#functions take in OSM map object from before and print csv to file
import sys, csv, math
import numpy as np




def distance(node1, node2):
    lat1, lon1 = node1.getCoord()
    lat2, long2 = node2.getCoord()

    return math.sqrt(math.pow(lat1 - lat2, 2)+ math.pow(lon1 - lon2, 2))

def slope(node1 , node2):
    lat1, lon1 = node1.getCoord()
    lat2, long2 = node2.getCoord()
    rise = lat2 - lat1
    run = lon2 - lon1
    if run == 0:
        if rise > 0:
            return sys.float_info.max -1
        else:
            return - (sys.float_info.max - 1)
    return rise/run



def mapVectorize1(map, csvfile):
    fieldNames=["numNodes","firstLastDist","avgDistance","stdDistance","firstLastSlope","avgSlope","stdSlope","prctNodeConnected","prctNodeUnique","connectWays0Degree","connectWays1Degree"]
    # classes=[""]
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldNames)
    csvwriter.writeheader()

    for id , way in map.ways.items():
        numNodes = len(way.nodes)
        distances = np.zeros(shape = (numNodes-1,))
        slopes = np.zeros(shape = (numNodes-1,))

        for i in range(numNodes-1):
            distances[i] = distance(map.nodes[way.nodes[i]],map.nodes[way.nodes[i+1]])
            slopes[i] = slope(map.nodes[way.nodes[i]],map.nodes[way.nodes[i+1]])

        meanDist = np.mean(distances)
        stdDist = np.std(distances)
        meanSlope = np.mean(slopes)
        stdSlope =  np.std(slopes)

        firstLastDist = distance(map.nodes[way.nodes[0]],map.nodes[way.nodes[numNodes-1]])
        firstLastSlope = slope(map.nodes[way.nodes[0]],map.nodes[way.nodes[numNodes-1]])
