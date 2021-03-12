import random
import itertools
import json
import networkx as nx
import csv
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from collections import defaultdict
from multiprocessing import Pool

class NetworkGenerator():
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

class NetworkModel():
    """
       Track and Iterate Network
    """

    def __init__(self, filename, basePercentage=0):
        """
            :param filenam: A json file
            :param basePercentage: Percentage of edges in initial network
        """
        if '.json' not in filename: filename += '.json'
        with open(filename, 'r') as file:
            nodeList, groups, edgeList = json.load(file)
        if basePercentage > 0:
            g = nx.erdos_renyi_graph( n=len(nodeList), p=basePercentage )
            for i,d in nodeList:
                g.nodes[i].update(d)
            for e in g.edges:
                g.edges[e]['weight'] = 1
        else:
            g = nx.Graph()
            g.add_nodes_from( nodeList )
        g.add_weighted_edges_from( edgeList )
        self.graph = g
        self.groups = groups

        self.statusNames = {
            'S': 'Susceptible',
            'L': 'Latent',
            'I': 'Infected',
            'A': 'Asymptomatic',
            'D': 'Dead',
            'RI': 'Recovered from Infected',
            'RA': 'Recovered from Asymptomatic'
        }

        self.params = {
            'beta': 0.005,
            'gammaI': 0.1,
            'gammaA': 0.15,
            'gammaRI': 0.2,
            'gammaRA': 0.2,
            'gammaD': 0.01,
        }

        # self.iter = 0
        # self.Lists = defaultdict(list) # Lists of L, I, A and Vulnerable
        # self.trend = defaultdict(list)
        # self.trendByGroup = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    def initialize(self, percentageInfected=.01, numCases=0):
        self.iter = 0
        self.Lists = defaultdict(list) # Lists of L, I, A and Vulnerable                    
        N = len(self.graph.nodes)
        lst = list(range(N))
        for i in lst:
            self.graph.nodes[i]['Status'] = 'S'
            self.graph.nodes[i]['numNeighbor'] = defaultdict(int)
        if numCases==0:
            numCases = int(N * percentageInfected)
        subList = random.choices(lst, k=numCases)
        for i in subList:
            self.graph.nodes[i]['Status'] = 'L'
            self.Lists['L'].append(i)
        vulnerable = set()
        for i in subList:
            for j in self.graph.neighbors(i):
                if self.graph.nodes[j]['Status'] == 'S':
                    vulnerable.add(j)
                    self.graph.nodes[j]['numNeighbor']['L'] += 1
        self.Lists['Vulnerable'] = list(vulnerable)
        self.iter = 0
        self.trend = defaultdict(lambda:[0])
        self.trend['L'] = [ numCases ]
        self.trend['S'] = [ N - numCases ]
        self.trendByGroup = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    def iteration(self, gTypes=None):
        """
        Execute a single model iteration
        """
        self.iter += 1
        g = self.graph

        nextStatus = dict()
        nextLists = defaultdict(list) # Lists of L, I, A and Vulnerable

        for i in self.Lists['Vulnerable']:

            eventp = random.random()

            u = self.graph.nodes[i]

            e = u['numNeighbor']['I'] + .5 * u['numNeighbor']['L'] + .3 * u['numNeighbor']['A']
            if eventp < 1 - (1 - self.params['beta']) ** e:
                u['Status'] = 'L'
                nextLists['L'].append(i)

            u['numNeighbor'] = defaultdict(int)

        for i in self.Lists['L']:
            eventp = random.random()
            if eventp < self.params['gammaI']:
                nextStatus[i] = 'I'
                nextLists['I'].append(i)
            elif eventp < self.params['gammaI'] + self.params['gammaA']:
                nextStatus[i] = 'A'
                nextLists['A'].append(i)
            else:
                nextLists['L'].append(i)

        for i in self.Lists['I']:
            eventp = random.random()
            if eventp < self.params['gammaRI']:
                nextStatus[i] = 'RI'
            elif eventp < self.params['gammaRI'] + self.params['gammaD']:
                nextStatus[i] = 'D'
            else:
                nextLists['I'].append(i)

        for i in self.Lists['A']:
            eventp = random.random()
            if eventp < self.params['gammaRA']:
                nextStatus[i] = 'RA'
            else:
                nextLists['A'].append(i)

        # Update Information
        for i in nextStatus:
            g.nodes[i]['Status'] = nextStatus[i]

        vulnerable = set()
        for c in ['L','I','A']:
            for i in self.Lists[c]:
                for j in self.graph.neighbors(i):
                    if self.graph.nodes[j]['Status'] == 'S' and self.graph.edges[(i,j)]['weight'] > 0:
                        vulnerable.add(j)
                        self.graph.nodes[j]['numNeighbor'][c] += self.graph.edges[(i,j)]['weight']
        nextLists['Vulnerable'] = list(vulnerable)
        self.Lists = nextLists
        # print(self.Lists)
        self.record( gTypes=gTypes )

    def bunchIteration(self, numIter, gTypes=None):
        for _ in range(numIter):
            self.iteration( gTypes=gTypes )

    def record(self, gTypes=None):
        nodesByStatus = dict()
        for s in self.statusNames:
            nodesByStatus[s] = [x for u, x in self.graph.nodes.items() if x['Status']==s]
            self.trend[s].append( len(nodesByStatus[s]) )
            if not gTypes: continue
            for c in gTypes:
                lst = [x[c] for x in nodesByStatus[s]]
                for val in self.groups[c]:
                    n = lst.count(val)
                    self.trendByGroup[s][c][val].append(n)
    
    def addNodes(self, n=10, rate=0.1, contact=6, quarantine=0):
        nodesOld = list( self.graph.nodes.keys() )
        n0 = nodesOld[-1]
        nodesNew = list(range(n0+1,n0+n+1))
        self.graph.add_nodes_from( nodesNew )
        for i in nodesNew:
            eventp = random.random()
            nodeContact = random.choices(nodesOld, k=contact)
            if eventp > rate:
                self.graph.nodes[i]['Status'] = 'S'
                self.graph.nodes[i]['numNeighbor'] = defaultdict(int)
            else:
                self.graph.nodes[i]['Status'] = 'L'
                self.Lists['L'].append( i )
                for j in nodeContact:
                    if self.graph.nodes[j]['Status'] == 'S' and j not in self.Lists['Vulnerable']:
                        self.Lists['Vulnerable'].append(j)
            edgeList = [(i,j,1) for j in nodeContact ]
            self.graph.add_weighted_edges_from( edgeList )
    
    def addContacts(self, edgeList, weight=1):
        for e in edgeList:
            if e in self.graph.edges:
                self.graph.edges[e]['weight'] += weight
            else:
                self.graph.add_edge(*e,weight=weight)
            # if self.graph.edges[e]['weight'] == 0:
            #     self.graph.remove_edge(*e)
    
    def gathering_one(self, x):
        days, sz, num = x
        self.initialize()
        nodeList = list(self.graph.nodes.keys())
        for _ in range(days):
            draw = random.choices(nodeList, k=sz*num)
            count = 0
            edgeList = []
            for _ in range(num):
                members = draw[count: count+sz]
                edgeList += list( itertools.combinations( members, 2) )
                count += sz
            self.addContacts(edgeList, 1)
            self.iteration()
            self.addContacts(edgeList, -1)
        return self.trend['I'][:]

    def gathering_simulation(self, days=10, sizes=[50,70,90], num_events=[10,20,30], filename='gathering_simulation.csv'):
        sizes_and_nums = [(days,sz,num) for sz in sizes for num in num_events]
        with Pool() as p: # Multi-processing
            trendAll = p.map(self.gathering_one, sizes_and_nums)
        with open(filename, 'w') as csvfile:
            fwriter = csv.writer(csvfile)
            header = ['Size', 'Number_of_Events', 'Trend']
            fwriter.writerow(header)
            for (_,sz,num), trend in zip(sizes_and_nums, trendAll):
                st_trend = '[' + '|'.join(map(str,trend)) + ']'
                row = [sz, num, st_trend]
                fwriter.writerow(row)
                print(f'Completed simuation with size={sz} and num_events={num}')

    def gathering_plot(self, input='gathering_simulation.csv', output='sizes_vs_nums.jpg'):
        sz_set, num_set = set(), set()
        with open(input, 'r') as csvfile:
            freader = csv.reader(csvfile)
            next(freader)
            grid = defaultdict(lambda: defaultdict(int))
            for row in freader:
                sz = int(row[0])
                num = int(row[1])
                sz_set.add(sz)
                num_set.add(num)
                trend = eval(row[2].replace('|',','))
                grid[sz][num] = max(trend)
        sizes = sorted(sz_set)
        num_events = sorted(num_set, reverse=True)
        outbreaks = np.array([[grid[sz][num] for sz in sizes] for num in num_events])
        plt.subplots(figsize=(10,6))
        ax = sns.heatmap(outbreaks, cmap='coolwarm')
        plt.xlabel('Event Sizes')
        ax.set_xticklabels(sizes)
        plt.ylabel('Number of Events')
        ax.set_yticklabels(num_events)
        plt.savefig('sizes_vs_nums.jpg')
        plt.show()

if __name__ == '__main__':
    model = NetworkModel('output/network_data.json')
    model.gathering_simulation()
    model.gathering_plot()
    
