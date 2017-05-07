#vectorizing only the proncipal highways
#functions take in OSM map object from before and print csv to file
import sys, csv, math
import numpy as np




def distance(node1, node2):
    lat1, lon1 = node1.getCoord()
    lat2, lon2 = node2.getCoord()

    return math.sqrt(math.pow(lat1 - lat2, 2) + math.pow(lon1 - lon2, 2))

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
        #field 1
        numNodes = len(way.nodes)

        #to calculate fields 2-7
        distances = np.zeros(shape = (numNodes-1,))
        slopes = np.zeros(shape = (numNodes-1,))

        for i in range(numNodes-1):
            distances[i] = distance(map.nodes[way.nodes[i]],map.nodes[way.nodes[i+1]])
            slopes[i] = slope(map.nodes[way.nodes[i]],map.nodes[way.nodes[i+1]])

        #Fields 2-7
        meanDist = np.mean(distances)
        stdDist = np.std(distances)
        meanSlope = np.mean(slopes)
        stdSlope =  np.std(slopes)
        firstLastDist = distance(map.nodes[way.nodes[0]],map.nodes[way.nodes[numNodes-1]])
        firstLastSlope = slope(map.nodes[way.nodes[0]],map.nodes[way.nodes[numNodes-1]])

        #Fields 10 & 11
        connectWays0Degree = connectedWays(map, way, wayTrack, 0)
        connectWays1Degree = connectedWays(map, way, wayTrack, 1)

        #calculate Fields 8 & 9
        pctUnique=np.zeros(shape = (numNodes,))
        for i in range(numNodes):
            if len(map.nodes[way.nodes[i]].superStructs[map.wayString]) == 1:
                pctUnique[i] = 1
        #Fields 8  & 9
        pctUnique = np.mean(pctUnique)
        pctNotUnique= 1.0 - pctUnique

        #input all fields
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


        #write to the csv
        csvwriter.writerow(row)


def mapVectorize2(map, csvfile):
    n_dim = 10
    fieldNames=["numNodes","firstLastDist","avgDistance","stdDistance","firstLastSlope","avgSlope","stdSlope","prctNodeConnected","prctNodeUnique","connectWaysZeroDegree","connectWaysOneDegree","scale"]

    for coordField in range(n_dim ** 2):
        fieldNames.append(str((int(coordField/n_dim), coordField % n_dim)))
    fieldNames.append("Class")
    classes={"motorway","trunk","primary","secondary","tertiary","unclassified","residential","service"}
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldNames)
    csvwriter.writeheader()

    #To keep track of how many ways connected to a single way
    wayTrack=dict()

    for id , way in map.ways.items():
        if way.tags["highway"] not in classes:
            continue

        row = dict()
        #field 1
        numNodes = len(way.nodes)

        #to calculate fields 2-9
        distances = np.zeros(shape = (numNodes-1,))
        slopes = np.zeros(shape = (numNodes-1,))
        pctUnique=np.zeros(shape = (numNodes,))

        #get slopes and distances as well the max and min lat and lons
        #calculate Fields 8 & 9
        maxLat = -90.0
        minLat = 90.0
        maxLon = -180.0
        minLon = 180.0
        for i in range(numNodes-1):
            lat1, lon1 = map.nodes[way.nodes[i]].getCoord()
            lat2, lon2 = map.nodes[way.nodes[i+1]].getCoord()
            if max(lat1, lat2) > maxLat:
                maxLat = max(lat1, lat2)
            if min(lat1, lat2) < minLat:
                minLat = min(lat1, lat2)
            if max(lon1, lon2) > maxLon:
                maxLon = max(lon1, lon2)
            if min(lon1, lon2) < minLon:
                minLon = min(lon1, lon2)

            if len(map.nodes[way.nodes[i]].superStructs[map.wayString]) == 1:
                pctUnique[i] = 1

            distances[i] = distance(map.nodes[way.nodes[i]],map.nodes[way.nodes[i+1]])
            slopes[i] = slope(map.nodes[way.nodes[i]],map.nodes[way.nodes[i+1]])

        if len(map.nodes[way.nodes[numNodes-1]].superStructs[map.wayString]) == 1:
            pctUnique[numNodes-1] = 1

        #Fields 2-9
        meanDist = np.mean(distances)
        stdDist = np.std(distances)
        meanSlope = np.mean(slopes)
        stdSlope =  np.std(slopes)
        firstLastDist = distance(map.nodes[way.nodes[0]],map.nodes[way.nodes[numNodes-1]])
        firstLastSlope = slope(map.nodes[way.nodes[0]],map.nodes[way.nodes[numNodes-1]])
        pctUnique = np.mean(pctUnique)
        pctNotUnique= 1.0 - pctUnique

        #Fields 10 & 11
        connectWays0Degree = connectedWays(map, way, wayTrack, 0)
        connectWays1Degree = connectedWays(map, way, wayTrack, 1)


        #Calculate street grid representation rest of fields
        gridCoords = set()
        latRange= (maxLat - minLat)
        lonRange= (maxLon - minLon)
        overallRange = max(latRange, lonRange)
        if overallRange == 0:
            continue #one point in a million
        def convertToGrid(latlon):
            gridLat = round((latlon[0] - minLat) * n_dim / overallRange)
            gridLon = round((latlon[1] - minLon) * n_dim / overallRange)
            return gridLat , gridLon

        for i in range(numNodes-1):
            glat1, glon1 = convertToGrid(map.nodes[way.nodes[i]].getCoord())
            glat2, glon2 = convertToGrid(map.nodes[way.nodes[i+1]].getCoord())
            glatRange = abs(glat2 - glat1)
            glonRange = abs(glon2 - glon1)
            glatSign = (glat2 - glat1) / max(glatRange, 1)
            glonSign = (glon2 - glon1) / max(glonRange, 1)
            gridCoords.add((glat1, glon1))
            ilat = glat1
            ilon = glon1
            pointsToProduce = max(glatRange, glonRange)
            for i in range(pointsToProduce):
                ilat += glatSign * glatRange / pointsToProduce
                ilon += glonSign * glonRange / pointsToProduce
                gridCoords.add((round(ilat), round(ilon)))

        #populate row once grid coordinates calculated
        for coordField in range(n_dim ** 2):
            if (int(coordField/n_dim), coordField % n_dim) in gridCoords:
                row[str((int(coordField/n_dim), coordField % n_dim))] = 1
            else:
                row[str((int(coordField/n_dim), coordField % n_dim))] = 0








        #input all fields
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
        row["scale"] = overallRange
        row["Class"] = way.tags["highway"]


        #write to the csv
        csvwriter.writerow(row)
