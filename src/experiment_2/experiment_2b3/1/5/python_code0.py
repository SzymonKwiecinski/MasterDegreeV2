import pulp

# Data from JSON
data = {'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}

# Unpack the data
num_links = data['NumLinks']
start_node = data['StartNode']
end_node = data['EndNode']
capacity = data['Capacity']
cost = data['Cost']
num_flow_reqs = data['NumFlowReqs']
source = data['Source']
destination = data['Destination']
data_rate = data['DataRate']

# Possible paths for each flow request
links = [(start_node[i], end_node[i]) for i in range(num_links)]

# Problem definition
problem = pulp.LpProblem("Minimize_Total_Transmission_Cost", pulp.LpMinimize)

# Decision variables for flow on each link for each flow request
flow_vars = {}
for f in range(num_flow_reqs):
    for (i, j) in links:
        flow_vars[f, (i, j)] = pulp.LpVariable(f'flow_{f}_{i}_{j}', lowBound=0, upBound=capacity[links.index((i, j))], cat='Continuous')

# Objective function
problem += pulp.lpSum([flow_vars[f, (i, j)] * cost[links.index((i, j))] for f in range(num_flow_reqs) for (i, j) in links])

# Constraints
for f in range(num_flow_reqs):
    # Flow conservation
    for node in set(start_node + end_node):
        incoming = pulp.lpSum([flow_vars[f, (i, j)] for (i, j) in links if j == node])
        outgoing = pulp.lpSum([flow_vars[f, (i, j)] for (i, j) in links if i == node])
        
        if node == source[f]:
            problem += (outgoing - incoming == data_rate[f], f'flow_conservation_source_{f}_{node}')
        elif node == destination[f]:
            problem += (incoming - outgoing == data_rate[f], f'flow_conservation_dest_{f}_{node}')
        else:
            problem += (incoming == outgoing, f'flow_conservation_middle_{f}_{node}')

# Solve the problem
problem.solve()

# Collect results
optimized_paths = {"paths": []}
total_cost = pulp.value(problem.objective)

for f in range(num_flow_reqs):
    path_flow = {}
    for (i, j) in links:
        if pulp.value(flow_vars[f, (i, j)]) > 0:
            path_flow[(i, j)] = pulp.value(flow_vars[f, (i, j)])
    
    path_cost = sum([pulp.value(flow_vars[f, (i, j)]) * cost[links.index((i, j))] for (i, j) in path_flow])
    optimized_paths["paths"].append({
        "source": source[f],
        "destination": destination[f],
        "route": list(path_flow.keys()),
        "path_flow": list(path_flow.values()),
        "path_cost": path_cost
    })

optimized_paths["total_cost"] = total_cost

print(optimized_paths)
print(f'(Objective Value): <OBJ>{total_cost}</OBJ>')