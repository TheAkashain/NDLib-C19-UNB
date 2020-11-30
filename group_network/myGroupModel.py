import random
import json
import pandas
import networkx as nx
from collections import defaultdict

class myGroupModel():
    """
       Track and Iterate Network
    """

    def __init__(self, filename, basePercentage=.05):
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

        self.iter = 0

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

        self.Lists = defaultdict(list) # Lists of L, I, A and Vulnerable

    def initialize(self, percentageInfected):
        self.iter = 0
        N = len(self.graph.nodes)
        lst = list(range(N))
        for i in lst:
            self.graph.nodes[i]['Status'] = 'S'
            self.graph.nodes[i]['numNeighbor'] = defaultdict(int)
        n = int(N * percentageInfected)
        subList = random.choices(lst, k=n)
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

    def iteration(self):
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
    
    def record(self, trend, trendByGroup=None, gTypes=None):
        nodesByStatus = dict()
        for s in self.statusNames:
            nodesByStatus[s] = [x for u, x in self.graph.nodes.items() if x['Status']==s]
            trend[s].append( len(nodesByStatus[s]) )
            if not gTypes: continue
            for c in gTypes:
                lst = [x[c] for x in nodesByStatus[s]]
                for val in self.groups[c]:
                    n = lst.count(val)
                    trendByGroup[s][c][val].append(n)
    
    def addNodes(self, n=10, rate=0.1, contact=6, quarantine=0):
        nodesOld = list( self.graph.nodes.keys() )
        n0 = nodesOld[-1]
        nodesNew = list(range(n0+1,n0+n+1))
        for u in nodesNew:
            self.graph.add_node(u)
            eventp = random.random()
            if eventp > rate:
                self.graph.nodes[u]['Status'] = 'L'
            else:
                self.graph.nodes[u]['Status'] = 'S'
                self.graph.nodes[u]['numNeighbor'] = defaultdict(int)
            nodeContact = random.choices(nodesOld, k=contact)
            for v in nodeContact:
                self.graph.add_edge(u,v)
        return None
    
    def addContacts(self, edgeList, weight=1):
        for e in edgeList:
            if e in self.graph.edges:
                self.graph.edges[e]['weight'] += weight
            else:
                self.graph.add_edge(*e,weight=weight)
            # if self.graph.edges[e]['weight'] == 0:
            #     self.graph.remove_edge(*e)
        return None
