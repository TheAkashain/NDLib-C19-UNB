import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as ns
import time
from ndlib.utils import multi_runs
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# Network Definition
for initialinfect in [1]:
    for itercount in [6, 7, 8, 9, 10, 11, 12, 13, 14]:
        start_time = time.time()
        N = 20000
        connections = 6
        iterations = 30
        executions = 1000
        print('-----Generating Barabasi-Albert graph with {} nodes-----'.format(N))
        g = nx.barabasi_albert_graph(N, connections)
        
        # Model Selection
        print('-----Configuring Model-----')
        model = gc.CompositeModel(g)
        
        # Model Statuses
        model.add_status("Susceptible")
        model.add_status("Exposed")
        model.add_status("Symptomatic")
        #model.add_status("Asymptomatic")
        model.add_status("Infected")
        model.add_status("Removed")
        
        #-----------------------------------------------------
        #DISEASE DATA
        r0 = 3.1
        disease_length = 14
        people_total = 12 * disease_length 
        chance_of_infection = r0 / people_total
        infect_chance = chance_of_infection
        #print(infect_chance)
        #-----------------------------------------------------
        # Compartment Definition
        c1_1 = ns.NodeStochastic(infect_chance, triggering_status="Infected")
        c1_3 = ns.NodeStochastic(infect_chance, triggering_status="Symptomatic")
        c2_1 = ns.NodeStochastic((1 - 0.5**(1/11))) 
        c3 = ns.NodeStochastic((1 - 0.5**(1/14)))
        c4 = ns.CountDown('Testing Timer', iterations = itercount)
        
        # Rule Definition
        model.add_rule("Susceptible","Exposed",c1_1)
        model.add_rule("Susceptible","Exposed",c1_3)
        model.add_rule("Exposed","Symptomatic",c2_1)
        model.add_rule("Symptomatic","Removed",c3)
        model.add_rule("Infected","Removed",c4)
        
        # Model Configuration
        config = mc.Configuration()
        config.add_model_parameter('fraction_infected', initialinfect/N)
        model.set_initial_status(config)
        
        # Simulation
        print('-----Doing {} simulation(s) on {} day test-----'.format(executions,itercount))
        trends = multi_runs(model, execution_number = executions, iteration_number = iterations, infection_sets=None)
        
        stop_time = time.time()
        total_time = stop_time - start_time
        print('\n----- Total Time: {} seconds ----'.format(total_time))
        
        print('-----Plotting Results-----')
        #print(iterations)
        #print(trends)
        from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
        
        daydata = []
        fig = ()
        ax = ()
        for n in range(0, executions):
            if (trends[n]['trends']['node_count'][0][-1] != (N - initialinfect)):
                daydata.append(N-trends[n]['trends']['node_count'][0][-1])
        print(daydata)
        fig = plt.hist(daydata)
        stdev = np.std(daydata)
        mean = np.mean(daydata)
        
        plt.title("Infected at Day {}".format(iterations), fontsize = 24)
        plt.xlabel("Infected Population", fontsize = 24)
        plt.ylabel("Number of Simulations", fontsize = 24)
        plt.figtext(0.85, 0.80, 'Outbreaks: {:.0f}\nMean: {:.3f}\nStDev: {:.3f}'.format(len(daydata), mean, stdev), 
                fontsize = 24, bbox = dict(boxstyle = 'round', facecolor = 'white'))
        plt.tight_layout()
        plt.savefig("Histogram4/(HIST)Patient 0 Test: {} Days Test, {} Days Total, {} Initial.png".format(itercount, iterations, initialinfect))
        plt.clf()
        
        viz = DiffusionTrend(model, trends)
        name = ("Histogram4/(COUNT)Patient 0 Test: {} Days Test, {} Days Total, {} Initial.png".format(itercount, iterations, initialinfect))
        viz.plot(filename = name, percentile = 90, itercount = executions, timereq = total_time)
            
