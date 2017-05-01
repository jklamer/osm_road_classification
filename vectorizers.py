#vectorizing only the proncipal highways
#functions take in OSM map object from before and print csv to file
import sys, csv, math
import numpy as np




def distance(node1, node2):
    lat1, lon1 = node1.getCoord()
    lat2, lon2 = node2.getCoord()

    return math.sqrt(math.pow(lat1 - lat2, 2)+ math.pow(lon1 - lon2, 2))

def slope(node1 , node2):
    lat1, lon1 = node1.getCoord()
    lat2, lon2 = node2.getCoord()
    rise = lat2 - lat1
    run = lon2 - lon1
    if run == 0:
        if rise > 0:
            return 100000
        else:
            return -100000
    return rise / run

def connectedWays(map, way, wayTrack, degrees):
    #only works for maps that remove other ways other than highways
    if way.id in wayTrack:
        if degrees <= 0:
            return wayTrack[way.id][0]
        else:
            runSum = wayTrack[way.id][0]
            for wayid in wayTrack[way.id][1]:
                runSum += (connectedWays(map, map.ways[wayid], wayTrack, degrees-1) - 1)
            return runSum
    else:
        connectedCurrently = 0
        searchNext = []
        for nds in way.nodes:
            for connectedWay in map.nodes[nds].superStructs[map.wayString]:
                if connectedWay != way.id:
                    connectedCurrently += 1
                    searchNext.append(connectedWay)

        wayTrack[way.id] = (connectedCurrently, searchNext)
        if degrees <= 0:
            return connectedCurrently
        else:
            runSum = connectedCurrently
            for wayid in searchNext:
                runSum += (connectedWays(map, map.ways[wayid], wayTrack, degrees-1) - 1)
            return runSum




def mapVectorize1(map, csvfile):
    fieldNames=["numNodes","firstLastDist","avgDistance","stdDistance","firstLastSlope","avgSlope","stdSlope","prctNodeConnected","prctNodeUnique","connectWaysZeroDegree","connectWaysOneDegree","Class"]
    classes={"motorway","trunk","primary","secondary","tertiary","unclassified","residential","service"}
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldNames)
    csvwriter.writeheader()
    #To keep track of how many ways connected to a single way
    wayTrack=dict()
    for id , way in map.ways.items():
        if way.tags["highway"] not in classes:
            continue

        row = dict()
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

        connectWays0Degree = connectedWays(map, way, wayTrack, 0)
        connectWays1Degree = connectedWays(map, way, wayTrack, 1)

        pctUnique=np.zeros(shape = (numNodes,))
        for i in range(numNodes):
            if len(map.nodes[way.nodes[i]].superStructs[map.wayString]) == 1:
                pctUnique[i] = 1
        pctUnique = np.mean(pctUnique)
        pctNotUnique= 1.0 - pctUnique

        row["numNodes"] = numNodes
        row["firstLastDist"] = firstLastDist
        row["avgDistance"] = meanDist
        row["stdDistance"] = stdDist
        row["firstLastSlope"] = firstLastSlope
        row["avgSlope"] = meanSlope
        row["stdSlope"] = stdSlope
        row["prctNodeConnected"] = pctNotUnique
        row["prctNodeUnique"] = pctUnique
        row["connectWaysZeroDegree"] = connectWays0Degree
        row["connectWaysOneDegree"] = connectWays1Degree
        row["Class"] = way.tags["highway"]
        csvwriter.writerow(row)
