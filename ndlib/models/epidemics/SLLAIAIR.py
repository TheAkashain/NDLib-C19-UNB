#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 14:36:07 2020

@author: theakashain
"""

import future.utils
import numpy as np
from ndlib.models.DiffusionModel import DiffusionModel

class SLLAIAIR(DiffusionModel):
    def __init__(self, graph, seed=None):
        super(self.__class__, self).__init__(graph, seed)
        
        self.available_statuses = {
            "Susceptible": 0,
            "Exposed": 1,
            "Exposed 2": 2,
            "Infected": 3,
            "Infected 2": 4,
            "Quarantined": 5,
            "Quarantined 2": 6,
            "Recovered A": 7,
            "Recovered I": 8
        }

        self.name = "SLLAIAIRR"

        self.parameters = {
            "model": {
                "alpha": {
                    "descr": "Incubation period",
                    "range": [0, 1],
                    "optional": False},
                "beta": {
                    "descr": "Infection rate",
                    "range": [0, 1],
                    "optional": False},
                "phi": {
                    "descr": "Recovery rate",
                    "range": [0, 1],
                    "optional": False}
            },
            "nodes": {},
            "edges": {}
        }

        self.progress = 0

    def iteration(self, node_status=True):
        self.clean_initial_status(list(self.available_statuses.values()))

        actual_status = {node: nstatus for node, nstatus in future.utils.iteritems(self.status)}

        #If this is the first iteration, return initial note status
        if self.actual_iteration == 0:
            self.actual_iteration += 1
            delta, node_count, status_delta = self.status_delta(actual_status)
            if node_status:
                return {"iteration": 0, "status": actual_status.copy(),
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}
            else:
                return {"iteration": 0, "status": {},
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}
        
        #Iteration inner loop
        for u in self.graph.nodes:

            u_status = self.status[u]
            eventp = np.random.random_sample()
            neighbors = self.graph.neighbors(u)
            if self.graph.directed:
                neighbors = self.graph.predecessors(u)

            if u_status == 0:  # Susceptible

                infected_neighbors = [v for v in neighbors if (self.status[v] == 3 or self.status[v] == 4)]

                if eventp < 1 - (1 - self.params['model']['beta']) ** len(infected_neighbors):
                        actual_status[u] = 1  # Exposed

            elif u_status == 1:
                if eventp < self.params['model']['alpha']:
                    actual_status[u] = 2  # Latent 2
            
            elif u_status == 2:
                if eventp < self.params['model']['alpha']:
                    actual_status[u] = 3  # Asymp
                    
            elif u_status == 3:
                if eventp < self.params['model']['alpha']:
                    actual_status[u] = 4  # Asymp 2

            elif u_status == 3:
                if eventp < self.params['model']['phi']:
                    actual_status[u] = 5  # Infected
                    
            elif u_status == 4:
                if eventp < self.params['model']['alpha']:
                    actual_status[u] = 7  # Removed A
                    
            elif u_status == 4:
                if eventp < self.params['model']['phi']:
                    actual_status[u] = 6  # Infected 2
                    
            elif u_status == 5:
                if eventp < self.params['model']['alpha']:
                    actual_status[u] = 6  # Infected 2
                    
            elif u_status == 6:
                if eventp < self.params['model']['alpha']:
                    actual_status[u] = 8  # Removed I

        delta, node_count, status_delta = self.status_delta(actual_status)
        self.status = actual_status
        self.actual_iteration += 1

        if node_status:
            return {"iteration": self.actual_iteration - 1, "status": delta.copy(),
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}
        else:
            return {"iteration": self.actual_iteration - 1, "status": {},
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}