from myGroupNetwork import NetworkModel

model = NetworkModel(filename='network_data.json')
print('Number of nodes: {}'.format(len(model.graph)))

filename = 'gathering_simulation.csv'
days = 10
sizes = [50, 70, 90]
num_events = [60, 80, 100]
model.gathering_simulation(days, sizes=sizes, num_events=num_events, filename=filename)

model.gathering_plot(input='gathering_simulation.csv', output='sizes_vs_nums.jpg')