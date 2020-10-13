import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as ns
from ndlib.utils import multi_runs
import time

N = 60000
connections = 6
iterations = 200
executions = 20
start_time = time.time()
print('-----Generating Barbasi-Albert graph with {} nodes-----'.format(N))
g = nx.barabasi_albert_graph(N, connections)

# Composite Model instantiation
print('-----Configuring Model-----')
model = gc.CompositeModel(g)

# Model statuses
model.add_status("Susceptible")
model.add_status("Infected")
model.add_status("Removed")

# Compartment definition
c1 = ns.NodeStochastic(0.02, triggering_status="Infected")
c2 = ns.NodeStochastic(0.01)

# Rule definition
model.add_rule("Susceptible", "Infected", c1)
model.add_rule("Infected", "Removed", c2)

# Model initial status configuration
config = mc.Configuration()
config.add_model_parameter('fraction_infected', 0.05)
model.set_initial_status(config)

# Simulation multiple execution
print('-----Doing {} simulation(s)-----'.format(executions))
trends = multi_runs(model, execution_number=executions, iteration_number=iterations, infection_sets=None)

stop_time = time.time()
total_time = stop_time - start_time
print('\n----- Total Time: {} seconds ----'.format(total_time))

print('-----Plotting Results-----')

from ndlib.viz.mpl.DiffusionTrend import DiffusionTrend

viz = DiffusionTrend(model, trends)
viz.plot()

