from ..DiffusionModel import DiffusionModel
import numpy as np
import future

__author__ = ["Gaia Noseworthy, UNB"]
__license__ = "BSD-2-Clause"


class Patient0Model(DiffusionModel):

    def __init__(self, graph, seed=None):

        super(self.__class__, self).__init__(graph, seed)

        self.name = "Patient 0"

        self.available_statuses = {
            "Susceptible": 0,
            "Exposed": 1,
            "Infected": 2,
            "Infectious": 3, 
            "Removed": 4
        }
        self.parameters = {
            "model": {
                    "alpha": {
                            "descr": "E -> I Probability",
                            "range": [0, 1],
                            "optional": False},
                    "beta": {
                            "descr": "Infection Probability",
                            "range": [0, 1],
                            "optional": False},
                    "gamma": {
                            "descr": "Recovery Probability",
                            "range": [0, 1],
                            "optional": False},
                    "days": {
                            "descr": "Days Until Caught",
                            "range": [0, 14],
                            "optional": False},
                    "phase": {
                            "descr": "Starting State",
                            "range": [0, 2],
                            "optional": False},
                    "ptrans1": {
                            "descr": "State Transition: Y -> O",
                            "range": [0, float("inf")],
                            "optional": False},
                    "ptrans2": {
                            "descr": "State Transition: O -> R",
                            "range": [0, float("inf")],
                            "optional": False},
            },
            "nodes": {},
            "edges": {
                    "Phase Requirement": {
                            "descr": "Y Phase: 0 - O Phase: 0.5 - R Phase: 1",
                            "range": [0, 1],
                            "optional": False,
                            "default": 0
                },          
            },
        }

        self.progress = {}

    def iteration(self, node_status=True):
        #print("Test")
        self.clean_initial_status(list(self.available_statuses.values()))

        actual_status = {node: nstatus for node, nstatus in future.utils.iteritems(self.status)}

        if self.actual_iteration == 0:
            self.actual_iteration += 1
            delta, node_count, status_delta = self.status_delta(actual_status)
            if node_status:
                return {"iteration": 0, "status": actual_status.copy(),
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}
            else:
                return {"iteration": 0, "status": {},
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}
                
        for u in self.graph.nodes:
            u_status = self.status[u]
            neighbors = self.graph.neighbors(u)
            days = self.params['model']['days']
            eventp = np.random.random_sample()
            if self.graph.directed:
                neighbors = self.graph.predecessors(u)

            if u_status == 0:  # Susceptible
                if (self.params['model']['phase'] == 0):
                    infected_neighbors = 0
                    for v in neighbors:
                        if (self.status[v] == 2 or self.status[v] ==3):
                            infected_neighbors += 1
                    if eventp < 1 - (1 - self.params['model']['beta']) ** infected_neighbors:
                        actual_status[u] = 1  # Exposed

                elif (self.params['model']['phase'] == 1):
                    infected_neighbors = 0
                    for v in neighbors: 
                        if (self.status[v] == 2 or self.status[v] == 3):
                            if (u,v) in self.params['edges']['Phase Requirement']:
                                if self.params['edges']['Phase Requirement'][(u,v)] >= 0.5:
                                    infected_neighbors += 1
                            elif (v, u) in self.params['edges']['Phase Requirement']:
                                if self.params['edges']['Phase Requirement'][(v,u)] >= 0.5:
                                    infected_neighbors += 1

                    if eventp < 1 - (1 - self.params['model']['beta']) ** infected_neighbors:
                        actual_status[u] = 1  # Exposed
                    
                else:
                    infected_neighbors = 0
                    for v in neighbors: 
                        if (self.status[v] == 2 or self.status[v] == 3):
                            if (u,v) in self.params['edges']['Phase Requirement']:
                                if self.params['edges']['Phase Requirement'][(u,v)] == 1:
                                    infected_neighbors += 1
                            elif (v, u) in self.params['edges']['Phase Requirement']:
                                if self.params['edges']['Phase Requirement'][(v,u)] == 1:
                                    infected_neighbors += 1
                    if eventp < 1 - (1 - self.params['model']['beta']) ** infected_neighbors:
                        actual_status[u] = 1  # Exposed

            elif u_status == 1:
                if eventp < self.params['model']['alpha']:
                    actual_status[u] = 3  # Infectious
            
            elif u_status == 2:
                try:
                    self.progress[u]
                except KeyError:
                    self.progress[u] = 0
                if self.progress[u] < days:
                    self.progress[u] += 1
                else:
                    actual_status[u] = 4  # Removed
                    del self.progress[u]
            
            elif u_status == 3:
                if eventp < self.params['model']['gamma']:
                    actual_status[u] = 4  # Removed

        delta, node_count, status_delta = self.status_delta(actual_status)
        self.status = actual_status
        self.actual_iteration += 1
        if (node_count[3] > self.params['model']['ptrans2']):
            self.params['model']['phase'] = 2
        elif (node_count[3] > self.params['model']['ptrans1']):
            self.params['model']['phase'] = 1
        else:
            self.params['model']['phase'] = 0

        if node_status:
            return {"iteration": self.actual_iteration - 1, "status": delta.copy(),
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}
        else:
            return {"iteration": self.actual_iteration - 1, "status": {},
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}
