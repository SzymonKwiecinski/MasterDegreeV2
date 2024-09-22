import pulp

# Problem Data
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

# Extract data
num_links = data['NumLinks']
start_node = data['StartNode']
end_node = data['EndNode']
capacity = data['Capacity']
cost = data['Cost']
num_flow_reqs = data['NumFlowReqs']
source = data['Source']
destination = data['Destination']
data_rate = data['DataRate']

# Initialize the problem
problem = pulp.LpProblem("Network_Flow_Optimization", pulp.LpMinimize)

# Define the decision variables
x = {}
for i in range(num_links):
    for k in range(num_flow_reqs):
        x[i, k] = pulp.LpVariable(f"x_{i}_{k}", lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(cost[i] * x[i, k] for i in range(num_links) for k in range(num_flow_reqs))

# Link Capacity Constraints
for i in range(num_links):
    problem += pulp.lpSum(x[i, k] for k in range(num_flow_reqs)) <= capacity[i]

# Flow Conservation Constraints
nodes = set(start_node + end_node)
for k in range(num_flow_reqs):
    for n in nodes:
        if n == source[k]:
            problem += (pulp.lpSum(x[i, k] for i in range(num_links) if start_node[i] == n) -
                        pulp.lpSum(x[i, k] for i in range(num_links) if end_node[i] == n) == data_rate[k])
        elif n == destination[k]:
            problem += (pulp.lpSum(x[i, k] for i in range(num_links) if start_node[i] == n) -
                        pulp.lpSum(x[i, k] for i in range(num_links) if end_node[i] == n) == -data_rate[k])
        else:
            problem += (pulp.lpSum(x[i, k] for i in range(num_links) if start_node[i] == n) -
                        pulp.lpSum(x[i, k] for i in range(num_links) if end_node[i] == n) == 0)

# Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')