import pulp

# Data
data = {
    'NumLinks': 4, 
    'StartNode': [1, 2, 2, 3], 
    'EndNode': [2, 3, 4, 4], 
    'Capacity': [50, 40, 60, 50], 
    'Cost': [2, 3, 1, 1], 
    'NumFlowReqs': 2, 
    'Source': [1, 2], 
    'Destination': [4, 3], 
    'DataRate': [40, 30]
}

# Sets and Parameters
num_links = data['NumLinks']
start_node = data['StartNode']
end_node = data['EndNode']
capacity = data['Capacity']
cost = data['Cost']
num_flow_reqs = data['NumFlowReqs']
source = data['Source']
destination = data['Destination']
data_rate = data['DataRate']

# Define Problem
problem = pulp.LpProblem("MinCostNetworkFlow", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Flow", ((i, j, k, l) for i, j in zip(start_node, end_node) for k, l in zip(source, destination)), 
                          lowBound=0, cat=pulp.LpContinuous)

# Objective Function
problem += pulp.lpSum(cost[link] * x[i, j, k, l] 
                      for link, (i, j) in enumerate(zip(start_node, end_node)) 
                      for k, l in zip(source, destination))

# Capacity Constraints
for link, (i, j) in enumerate(zip(start_node, end_node)):
    problem += pulp.lpSum(x[i, j, k, l] for k, l in zip(source, destination)) <= capacity[link]

# Flow Conservation Constraints
nodes = list(set(start_node + end_node))
for n in nodes:
    for k, l in zip(source, destination):
        inflow = pulp.lpSum(x[i, j, k, l] for i, j in zip(start_node, end_node) if i == n)
        outflow = pulp.lpSum(x[j, i, k, l] for i, j in zip(start_node, end_node) if j == n)
        if n == k:
            problem += inflow - outflow == data_rate[source.index(k)]
        elif n == l:
            problem += inflow - outflow == -data_rate[source.index(k)]
        else:
            problem += inflow - outflow == 0

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')