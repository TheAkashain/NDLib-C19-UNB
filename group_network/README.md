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
- Breadth First Search (BFS). Instead of visiting all nodes in each iteration,
only infected and vulnerable nodes are visited.

## Requirement

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install NetWorkX.

```bash
pip install networkx
```

## Usage

See 
[GroupNetwork_Run.ipynb](./GroupNetwork_Run.ipynb)
for more demonstrations.

The demo file
was written in Jupyter Notebook,
which can be run in
[Anaconda](https://www.anaconda.com/products/individual)
on your local machine.
Alternatively,
it can be run on the cloud in
[Google Colab](https://colab.research.google.com/github/TheAkashain/NDLib-C19-UNB/blob/master/group_network/GroupNetwork_Run.ipynb).

## Sample Codes and Outputs

### Build network
Set percentage of age levels
and sizes of social groups.
```python
import myGroupNetwork

N = 20000 # Total Population

youngPercent = 0.15 # Percentage of each age group
adultPercent = 0.65
oldPercent = 1 - youngPercent - adultPercent # = 0.20

nYoung = int(youngPercent * N)
nMiddle = int(adultPercent * N)
nSenior = N - nYoung - nMiddle
data = myGroupNetwork.buildGroups(size={'Young': nYoung, 'Middle': nMiddle, 'Senior': nSenior})

# Add groups
data.addGroup(groupType='CareHome', numUnits=N//300, size={'Middle':20, 'Senior': 30}, contactPercentage=.7)

data.addGroup(groupType='School', numUnits=10//300, size={'Young':50, 'Middle': 20}, contactPercentage=.7)

data.addGroup(groupType='Work', numUnits=N//20, size={'Middle': 12}, exclude=['CareHome','School'], contactPercentage=.4)

## Save data and then pass to the builder
filename = 'output/network_data.json'
data.save( filename='output/network_data.json' )
model = myGroupNetwork.buildNetwork( filename )
```

Inspect some nodes in the network

```python
N = len(model.graph.nodes)
for i in range(0, N, N//20): # List 20 nodes
    print(i ,model.graph.nodes[i])
```

```
0 {'AgeLevel': 'Young', 'Home': 3694}
1000 {'AgeLevel': 'Young', 'Home': 292}
2000 {'AgeLevel': 'Young'}
3000 {'AgeLevel': 'Middle'}
4000 {'AgeLevel': 'Middle', 'Work': 68}
5000 {'AgeLevel': 'Middle', 'Work': 957, 'Home': 1513}
6000 {'AgeLevel': 'Middle'}
7000 {'AgeLevel': 'Middle', 'Work': 618}
8000 {'AgeLevel': 'Middle', 'Home': 3910}
9000 {'AgeLevel': 'Middle', 'Work': 890, 'Home': 3860}
10000 {'AgeLevel': 'Middle', 'Work': 435, 'Home': 2298}
11000 {'AgeLevel': 'Middle', 'Work': 763}
12000 {'AgeLevel': 'Middle', 'Work': 449, 'Home': 2258}
13000 {'AgeLevel': 'Middle'}
14000 {'AgeLevel': 'Middle', 'Work': 974}
15000 {'AgeLevel': 'Middle', 'Work': 134}
16000 {'AgeLevel': 'Senior'}
17000 {'AgeLevel': 'Senior', 'CareHome': 45}
18000 {'AgeLevel': 'Senior'}
19000 {'AgeLevel': 'Senior', 'Home': 1278}
```

### Trend of Infected Population
```python
import myGroupNetwork

numRun = 5
multiTrend =  []
for iRun in tqdm(range(numRun)):
    model.initialize( numCases=10 )
    numIter = 40
    model.bunchIteration( numIter )
    multiTrend.append( model.trend )
```

```python
import matplotlib.pyplot

ave, upper, lower = (defaultdict(lambda: [0]*numIter) for _ in range(3))
percentile = 10
for j in range(numIter):
    for c in model.statusNames:
        if c in ['RI','RA']: continue
        data = [multiTrend[i][c][j] for i in range(numRun)]
        ave[c][j] = np.average(data)
        upper[c][j] = np.percentile(data,percentile)
        lower[c][j] = np.percentile(data,100-percentile)
fig, ax = plt.subplots( figsize=(10,6) )
days = list(range(numIter))
for c in model.statusNames:
    if c in ['S','RI','RA']: continue
    ax.plot(days, ave[c], label=model.statusNames[c])
    ax.fill_between(days, lower[c], upper[c], alpha=.2)
ax.legend( fontsize='large' )
ax.set_xlabel('Days', fontsize='x-large')
ax.set_ylabel('Population', fontsize='x-large')
ax.set_title(f'The {percentile}-{100-percentile} Percentiles wit {numRun} Runs')
```

![Trend by Age](output/fig_trend_multi_run.jpg)

Representing infected population by age groups
```python
fig, ax = plt.subplots( figsize=(10,6) )
status = 'I'
gType = 'AgeLevel'
gVals = list( model.groups[gType].keys() )
data = dict()
for val in gVals:
    data[val] = trendByGroup[status][gType][val]
days = list(range(num_iter))
ax.stackplot(days, data.values(), labels=data.keys(), alpha=.6)
ax.legend(fontsize='large', loc='upper left')
ax.set_xlabel('Days', fontsize='large')
ax.set_ylabel(f'{model.statusNames[status]} Population ({status})', fontsize='large')
```

![Trend by Age](output/fig_trend_by_age.jpg)

### Simulatiing the Effects of Large Events
```python
import myGroupNetwork

dayOfEvent = [5,6] # Big event days
numIter = 40
numRun = 7

numPeople = 400
contactPercentage = .6

nodesList = list(model.graph.nodes.keys())
multiTrend = []
for iRun in tqdm(range(numRun)):
    model.initialize( numCases=10 )
    for j in range(numIter):
        if j in dayOfEvent:
            participantsList = random.choices(nodesList, k=numPeople)
            edgeAll = list( itertools.combinations(participantsList,2) )
            edgeList = random.choices( edgeAll, k=int(len(edgeAll)*contactPercentage) )
            model.addContacts(edgeList, weight=1)
            model.iteration()
            model.addContacts(edgeList, weight=-1)
        else:
            model.iteration()
    multiTrend.append( model.trend )
```

```python
import matplotlib.pyplot

percentile = 5
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
    ax.fill_between(days, lower[s], upper[s], alpha=.2)
ax.legend( fontsize='large' )
ax.set_xlabel('Days', fontsize='x-large')
ax.set_ylabel('Population', fontsize='x-large')
ax.set_title(f'Big event on days {dayOfEvent}')
```

![Large Gathering](output/fig_large_gathering.jpg)

### Simulatiing the Effects of Family Gathering
```python
import myGroupNetwork

start = 5 # start day of family gathering
end = 10 # end day of family gathering
numIter = 50
numRun = 7
numFamily = 60
numPeopleEach = 20
nodeList = list(model.graph.nodes.keys())

model.params['beta'] = .005

draw = random.choices( nodeList, k = numFamily * numPeopleEach )
count = 0
edgeList = []
for i in range(numFamily):
    members = draw[count:count+numPeopleEach]
    edgeList += list( itertools.combinations( members, 2) )
    count += numPeopleEach

multiTrend =  []
for iRun in tqdm(range(numRun)):
    model.initialize( numCases=10 )
    for j in range(numIter):
        if j == start:
            model.addContacts(edgeList, weight=1)
        model.iteration()
        if j == end:
            model.addContacts(edgeList, weight=-1)
    multiTrend.append( model.trend )
```

```python
import matplotlib.pyplot

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
    ax.fill_between(days, lower[s], upper[s], alpha=.2)
ax.legend( fontsize='large' )
ax.set_xlabel('Days', fontsize='x-large')
ax.set_ylabel('Population', fontsize='x-large')
ax.set_title(f'{numFamily} families gathered, each of size {numPeopleEach}, from day {start} to {end}')
```

![Large Gathering](output/fig_family_gathering.jpg)

### Simulatiing the Effects of Importation
```python
import myGroupNetwork

modelOld = model
numVisitorsPerDay = [10, 20, 30, 40]
N = len(numVisitorsPerDay)
newInfectiousRate = .005
contact = 6
quarantine = 0
numIter = 40
numRun = 7
endSizes = [[0] * numRun for _ in range(N)]
for j in tqdm(range(N)):
    numV = numVisitorsPerDay[j]
    model = deepcopy(modelOld)
    for iRun in range(numRun):
        model.initialize( numCases=10 )
        for _ in range(numIter):
            model.addNodes(numV, newInfectiousRate, contact, quarantine)
            model.iteration()
        for c in ['L','I','A']:
            endSizes[j][iRun] += model.trend[c][-1]
model = modelOld
```

```python
import matplotlib.pyplot

fig, ax = plt.subplots( figsize=(10,5) )
sns.boxplot(data=endSizes, ax=ax)
sns.swarmplot(data=endSizes, ax=ax, size=4, color='k', linewidth=.9)
plt.xticks(plt.xticks()[0], numVisitorsPerDay)
ax.set_xlabel('Importation Per Day', fontsize='x-large')
ax.set_ylabel(f'Infected population (I+L+A) on day {numIter}', fontsize='x-large')
```

![Large Gathering](output/fig_importation.jpg)

## Contributing
UNB and GNB
