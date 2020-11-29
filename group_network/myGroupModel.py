# from ndlib.models.DiffusionModel import DiffusionModel
# import numpy as np
# import future.utils
import random
import json
import pandas
import networkx as nx
from collections import defaultdict

class myGroupModel():
    """
       Track and Iterate Network
    """

    def __init__(self, filename):
        """
            :param labels: A cvs file for pandas dataframe
            :param edges: 
         """
        g = nx.erdos_reny(p=.1)
        if '.json' not in filename: filename += '.json'
        with open(filename, 'r') as file:
            nodeList, groups, edgeList = json.load(file)
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

    def initialize(self, percentageInfected):
        self.iter = 0
        N = len(self.graph.nodes)
        lst = list(range(N))
        for i in lst:
            self.graph.nodes[i]['Status'] = 'S'
        n = int(N * percentageInfected)
        subList = random.choices(lst, k=n)
        for i in subList:
            self.graph.nodes[i]['Status'] = 'L'

    def iteration(self):
        """
        Execute a single model iteration
        """
        self.iter += 1

        nextStatus = dict()
        g = self.graph

        # Similar to NDLib
        for id, u in self.graph.nodes.items():

            eventp = random.random()
            neighbors = self.graph.neighbors(id)
            
            if u['Status'] == 'S':
                neighborsL = [v for v in neighbors if g.nodes[v]['Status'] == 'L']
                neighborsI = [v for v in neighbors if g.nodes[v]['Status'] == 'I']
                neighborsA = [v for v in neighbors if g.nodes[v]['Status'] == 'A']

                e = len(neighborsI) + .5 * len(neighborsL) + .3 * len(neighborsA)
                if eventp < 1 - (1 - self.params['beta']) ** e:
                    u['Status'] = 'L'
                        
            elif u['Status'] == 'L':
                if eventp < self.params['gammaI']:
                    nextStatus[id] = 'I'
                elif eventp < self.params['gammaI'] + self.params['gammaA']:
                    nextStatus[id] = 'A'

            elif u['Status'] == 'I':
                if eventp < self.params['gammaRI']:
                    nextStatus[id] = 'RI'
                elif eventp < self.params['gammaRI'] + self.params['gammaD']:
                    nextStatus[id] = 'D'

            elif u['Status'] == 'A':
                if eventp < self.params['gammaRA']:
                    nextStatus[id] = 'RA'

        # Update Information
        for id in nextStatus:
            g.nodes[id]['Status'] = nextStatus[id]
    
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
            if self.graph.edges[e]['weight'] == 0:
                self.graph.remove_edge(*e)
        return None
