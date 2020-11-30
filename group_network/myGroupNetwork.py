from collections import defaultdict
import random
import itertools
import pandas as pd
import json

class myGroupNetwork():
    """
       Build Network with group labels
    """

    def __init__(self, size):
        N = sum(size.values())
        self.nodes = [dict() for _ in range(N)]
        self.groups = defaultdict(lambda: defaultdict(list))
        self.edgeWeights = defaultdict(int)
        count = 0
        for c, val in size.items():
            self.groups['AgeLevel'][c] = list(range(count,count+val))
            count += val
        for c in size:
            for i in self.groups['AgeLevel'][c]:
                self.nodes[i]['AgeLevel'] = c
    
    def addGroup(self, groupType, numUnits, size, exclude=[], contactPercentage=1):
        if isinstance(size, int):
            eligible = [ u for u,d in enumerate(self.nodes) if not any(x in d for x in exclude) ]
            draw = random.choices( eligible, k=numUnits*size)
            for j in range(numUnits): # The j-th unit
                start, end = j * size, (j+1) * size
                self.groups[groupType][j] = draw[start:end]
        else: # Age is specified in size
            draw = dict() # Draw people in each age group
            for c, val in size.items():
                eligible = [ u for u in self.groups['AgeLevel'][c] if not any(x in self.nodes[u] for x in exclude) ]
                draw[c] = random.choices(eligible, k=val*numUnits)
            for j in range(numUnits): # The j-th unit
                    start, end = j * val, (j+1) * val
                    self.groups[groupType][j].extend( draw[c][start:end] )
        for j in range(numUnits): # The j-th unit
            for i in self.groups[groupType][j]:
                self.nodes[i][groupType] = j
            edgesAll = list(itertools.combinations( self.groups[groupType][j], 2))
            for e in random.choices(edgesAll, k = int(len(edgesAll)*contactPercentage) ):
                self.edgeWeights[ (min(e),max(e)) ] += 1

    def save(self, filename):
        nodeList = [(i,node) for i,node in enumerate(self.nodes)]
        edgeList = [(a,b,self.edgeWeights[(a,b)]) for a, b in self.edgeWeights]
        if '.json' not in filename: filename += '.json'
        with open( filename, 'w') as file:
            json.dump( (nodeList, self.groups, edgeList), file)
