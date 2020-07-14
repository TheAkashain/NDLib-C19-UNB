from ..DiffusionModel import DiffusionModel
import numpy as np
import future

__author__ = ["Gaia Noseworthy, UNB"]
__license__ = "BSD-2-Clause"


class ASPhaseModel(DiffusionModel):

    def __init__(self, graph, seed=None):

        super(self.__class__, self).__init__(graph, seed)

        self.name = "ASPhaseModel"

        self.available_statuses = {
            "Susceptible": 0,
            "Exposed": 1,
            "Infected": 2,
            "Asymptomatic": 3, 
            "Removed": 4,
            "Tested": 5,
            "Tested Removed": 6,
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
                    "asymp_chance": {
                            "descr": "Percent of cases that are asymptomatic",
                            "range": [0, 1],
                            "optional": False},
                    "asymp_infect": {
                            "descr": "Likelihood of infection from asymptomatic case",
                            "range": [0, 1],
                            "optional": False},
                    "symp_test": {
                            "descr": "Probability of a symptomatic case getting tested",
                            "range": [0, 1],
                            "optional": False},
                    "rand_test_count": {
                            "descr": "Number of random people tested per day",
                            "range": [0, 1],
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

    #This code runs for every iteration, or day, in the simulation
    def iteration(self, node_status=False):
        self.clean_initial_status(list(self.available_statuses.values()))

        actual_status = {node: nstatus for node, nstatus in future.utils.iteritems(self.status)}
        
        #If this is the first iteration, create the necessary environment
        if self.actual_iteration == 0:
            self.actual_iteration += 1
            delta, node_count, status_delta = self.status_delta(actual_status)
            if node_status:
                return {"iteration": 0, "status": actual_status.copy(),
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}
            else:
                return {"iteration": 0, "status": {},
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}
                
        #This code runs for every node on the graph
        for u in self.graph.nodes:
            u_status = self.status[u]
            
            neighbors = self.graph.neighbors(u)
            eventp = np.random.random_sample()
            if self.graph.directed:
                neighbors = self.graph.predecessors(u)
            
            #For susceptible individuals, they run an infection check based on the phase
            #The higher the phase (Y<O<R), the lower the chance of infection, as less edges
            #are checked (as checked in the "Phase Requirement" lines)
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

            #For exposed individuals, they have a random chance of becoming symptomatic
            #or asymptomatic, defined by the early eventp for transition, and by randtest
            #for which compartment they move to
            elif u_status == 1: #Exposed
                if eventp < self.params['model']['alpha']:
                    randtest = np.random.random_sample()
                    if (randtest < self.params['model']['asymp_chance']):
                        actual_status[u] = 3 #Asymtomatic
                    else:
                        actual_status[u] = 2 #Symptomatic (infected)
            
            #For symptomatic (infected) individuals, they have a random chance to be removed,
            #and also a random chance to be tested (which allows for contact tracing). This
            #could be easily modified to make testing more likely based on phase.
            elif (u_status == 2): #Symptomatic
                randtest = np.random.random_sample()
                if eventp < self.params['model']['gamma']:
                    actual_status[u] = 4  # Removed
                if randtest < self.params['model']['symp_test']:
                    actual_status[u] = 5 #Tested
                    self.progress[u] = 0
            
            #For asymptomatic individuals, they have a random chance to be removed.
            elif (u_status == 3): #Asymptomatic
                if eventp < self.params['model']['gamma']:
                    actual_status[u] = 4  # Removed
            
            #For tested invidiuals (specifically meaning they tested positive), their 
            #edge-neighbors are also all tested after X days.
            elif (u_status == 5): #Tested
                if self.progress[u] >= 1 and self.progress[u] < 2:
                    for v in neighbors: 
                        if (self.status[v] == 2 or self.status[v] == 3):
                            self.status[v] = 5 #Tested
                            self.progress[v] = 0
                    self.progress[u] = 2
                    
                elif self.progress[u] < 2:
                    self.progress[u] += 0.34
                    
                if eventp < self.params['model']['gamma']:
                        actual_status[u] = 6 #Tested Removed
            
            #This code allows for a tested person to heal, while still having their
            #edge-neighbors tested after X days.
            elif (u_status == 6): #Tested Removed
                if self.progress[u] >= 1 and self.progress[u] < 2:
                    for v in neighbors: 
                        if (self.status[v] == 2 or self.status[v] == 3):
                            self.status[v] = 5 #Tested
                            self.progress[v] = 0
                    self.progress[u] = 2
                    
                elif self.progress[u] < 2:
                    self.progress[u] += 0.34
        
        #This code block allows for random testing of individuals, as is done in some countries.
        #If this is not wanted, set rand_test_count to 0.
        random_tests = np.random.random_sample(self.params['model']['rand_test_count'])*len(self.graph.nodes)
        for u in random_tests:
            if (u_status == 2 or u_status == 3):
                self.status[u] = 5 #Tested
        
        #All the data is saved in these blocks, and time is moved forwards 1 day
        delta, node_count, status_delta = self.status_delta(actual_status)
        self.status = actual_status
        self.actual_iteration += 1
        
        #This block updates the phase based on the number of active, tested cases
        #ptrans1 and ptrans2 define the number of cases needed to transition phases
        if (node_count[5] > self.params['model']['ptrans2']):
            self.params['model']['phase'] = 2
        elif (node_count[5] > self.params['model']['ptrans1']):
            self.params['model']['phase'] = 1
        else:
            self.params['model']['phase'] = 0

        #This block returns the final data
        if node_status:
            return {"iteration": self.actual_iteration - 1, "status": delta.copy(),
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}
        else:
            return {"iteration": self.actual_iteration - 1, "status": {},
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}
