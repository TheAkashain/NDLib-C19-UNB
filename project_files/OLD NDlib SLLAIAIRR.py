#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 30 16:11:22 2020

@author: theakashain
"""

import networkx as nx
import ndlib.models.ModelConfig as mc
from ndlib.utils import multi_runs
import matplotlib.pyplot as plt
import time
import ndlib.models.epidemics as ep

for phi in (0.015, 0.02, 0.025):
    start_time = time.time()
    N = 20000
    connections = 6
    iterations = 100
    executions = 1000
    initialinfect = 5
    print('-----Generating Barabasi-Albert graph with {} nodes-----'.format(N))
    g = nx.barabasi_albert_graph(N, connections)
    
    # Model Selection
    print('-----Configuring Model-----')
    model = ep.SLLAIAIR(g)
    
    #-----------------------------------------------------
    #DISEASE DATA
    r0 = 3.1
    disease_length = 14
    people_total = 12 * disease_length 
    chance_of_infection = r0 / people_total
    infect_chance = chance_of_infection
    #print(infect_chance)
    #-----------------------------------------------------
    # Model Configuration
    cfg = mc.Configuration()
    cfg.add_model_parameter('beta', 0.01)
    cfg.add_model_parameter('phi', phi)
    cfg.add_model_parameter('alpha', 0.01)
    cfg.add_model_parameter('fraction_infected', initialinfect/N)
    model.set_initial_status(cfg)
    
    # Simulation
    print('-----Doing {} simulation(s)-----'.format(executions))
    trends = multi_runs(model, execution_number = executions, iteration_number = iterations, infection_sets=None)
    
    stop_time = time.time()
    total_time = stop_time - start_time
    print('\n----- Total Time: {} seconds ----'.format(total_time))
    
    print('-----Plotting Results-----')
    #print(iterations)
    #print(trends)
    from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend
    
    daydata = []
    for n in range(0, executions):
        daydata.append(trends[n]['trends']['node_count'][0][-1])
    fig = plt.hist(daydata)
    plt.title("Susceptible Remaining at Day 100")
    plt.xlabel("Susceptible Population")
    plt.ylabel("Number of Simulations")
    plt.savefig("SLLAIAIR Results/(HIST)Patient 0 Test: {} People, {} Connections,{} Days Total, {} Initial, {} Phi.png".format(N, connections, iterations, initialinfect, phi))
    
    viz = DiffusionTrend(model, trends)
    name = ("SLLAIAIR Results/(COUNT)Patient 0 Test: {} People, {} Connections, {} Days Total, {} Initial, {} Phi.png".format(N, connections, iterations, initialinfect, phi))
    viz.plot(filename = name, percentile = 90, itercount = executions, timereq = total_time)