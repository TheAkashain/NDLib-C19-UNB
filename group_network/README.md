# Group Network

myGroupNetwork.py is a module to construct networks.

myGroupModel.py is a module to simulate epidemic model.

These two modules were built on top of the library
[NetWorkX](https://networkx.org/).

This modules provide some features
that are not available in Network Diffusion Library
[NDLib](https://ndlib.readthedocs.io/).
The new features are:

- Age structure and group labels.
- Adding nodes and edges during between iterations, which is capable of simulating effects of importation and gathering under endemic.
- Breadth First Search (BFS). __To-Do__


## Requirement

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install NetWorkX.

```bash
pip install networkx
```

## Usage

To build network (see GroupNetwork_Build.ipynb for more details):

```python
import foobar

from myGroupNetwork import myGroupNetwork

# Set parameters
N = 2000 # Total Population
youngPercent = 0.15 # Percentage of each age group
adultPercent = 0.65
oldPercent = 1 - youngPercent - adultPercent # = 0.20

# Build base age-structured network
nYoung = int(youngPercent * N)
nMiddle = int(adultPercent * N)
nSenior = N - nYoung - nMiddle
data = myGroupNetwork(size={'Young': nYoung, 'Middle': nMiddle, 'Senior': nSenior})

# Add groups
data.addGroup(groupType='CareHome', n=60, size={'Middle':20, 'Senior': 30}, contactPercentage=.7)

data.addGroup(groupType='School', n=70, size={'Young':50, 'Middle': 20}, contactPercentage=.7)

data.addGroup(groupType='Work', n=N//20, size={'Middle': 12}, exclude=['CareHome','School'], contactPercentage=.4)

data.addGroup(groupType='Home', n=N//5, size= 3 , exclude=['CareHome'], contactPercentage=1)

# Save result
data.save( filename='network_data.json' )
```

To run simulation (see GroupNetwork_Simulation.ipynb for details):

```python
import foobar

from myGroupModel import myGroupModel

# Load network
filename = 'network_data.json'
model = myGroupModel( filename )

# Similation with large gathering
import random
import itertools
dayOfEvent = [20,21] # Big event days
numIter = 40
numRun = 5
initialRate = .05

numPeople = 400
contactPercentage = .6

nodesList = list(model.graph.nodes.keys())
multiTrend =  [defaultdict(list) for _ in range(numRun)]
for iRun in tqdm(range(numRun)):
    model.initialize( percentageInfected=initialRate )
    for j in range(numIter):
        if j in dayOfEvent:
            participantsList = random.choices(nodesList, k=numPeople)
            edgeAll = list( itertools.combinations(participantsList,2) )
            edgeList = random.choices( edgeAll, k=int(len(edgeAll)*contactPercentage) )
            model.addContacts(edgeList, weight=1)
        model.iteration()
        model.record(multiTrend[iRun])
        if j in dayOfEvent:
            model.addContacts(edgeList, weight=-1)

# Visualize the simulation
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

percentile = 10
ave, upper, lower = (defaultdict(lambda: [0]*numIter) for _ in range(3))
skipped = ['S','RI','RA']
for j in range(numIter):
    for c in model.statusNames:
        if c in skipped: continue
        data = [multiTrend[i][c][j] for i in range(numRun)]
        ave[c][j] = np.average(data)
        upper[c][j] = np.percentile(data,percentile)
        lower[c][j] = np.percentile(data,100-percentile)
fig, ax = plt.subplots( figsize=(10,5) )
days = list(range(numIter))
for s, sName in model.statusNames.items():
    if s in skipped: continue
    ax.plot(days, ave[s], label=sName)
    ax.fill_between(days, lower[c], upper[c], alpha=.2)
ax.legend( fontsize='large' )
ax.set_xlabel('Days', fontsize='x-large')
ax.set_ylabel('Population', fontsize='x-large')
ax.set_title(f'Big event on days {dayOfEvent}')
```

## Contributing
UNB and GNB
