__author__ = 'shubhamid'
#!/usr/bin/python

import re

class Vertex:
    def __init__(self,key):
        self.id = key
        self.connectedTo = {}

    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self,nbr):
        return self.connectedTo[nbr]

class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self,n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertList

    def addEdge(self,f,t,cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

g = Graph()
for i in range(4):
    g.addVertex(i+1)
g.vertList

for i in range(4):
    fileName = (i+1).__str__() + '.html'
    f = open(fileName, 'r')
    fileContent = f.read()

    pattern = r"<a href=\"(.*).html\""

    regex = re.compile(pattern, re.IGNORECASE)
    for match in regex.finditer(fileContent):
        #print (i+1), match.group(1)
        g.addEdge((i+1),match.group(1))

#for v in g:
#   for w in v.getConnections():
#       print("( %s , %s )" % (v.getId(), w.getId()))

adjMat = [[0 for i in range(4)] for j in range(4)]

for v in g:
   for w in v.getConnections():
       rowNo = int(v.getId())
       colNo = int(w.getId())
       adjMat[rowNo-1][colNo-1] = 1

sumRow = [0 for i in range(4)]
sumCol = [0 for i in range(4)]
ratio = [0 for i in range(4)]
for v in g:
   for w in v.getConnections():
       rowNo = int(v.getId())
       colNo = int(w.getId())
       sumRow[rowNo-1] += adjMat[rowNo-1][colNo-1]
       sumCol[colNo-1] += adjMat[rowNo-1][colNo-1]

for r in adjMat:
    print r

for i in range(4):
    ratio[i] = (float(sumRow[i]) / float(sumCol[i])).__pow__(-1)

print "InDegree :", sumCol
print "OutDegree :", sumRow
print "Ratio :", ratio

flag = ['empty' for i in range(4)]

for i in range(4):
    if ratio[i] < 0.95 :
        flag[i] = 'Not Spam'
    elif ratio[i] > 1.20:
        flag[i] = 'Spam'
    else:
        flag[i] = 'BorderLine'
print flag

pr = [1.0 for i in range(4)]
print pr
d = 0.85

for k in range(50):
    for i in range(4):
        sigma = 0.0
        for j in range(4):
            if adjMat[j][i] == 1:
                #print j+1, pr[j], sumRow[j]
                sigma += (pr[j] / sumRow[j])
        pr[i] = (1-d) + d*(sigma)

print pr