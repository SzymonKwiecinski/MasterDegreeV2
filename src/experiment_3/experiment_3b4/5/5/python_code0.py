import pulp

# Data from the provided JSON
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

# Unpack data
num_links = data['NumLinks']
start_node = data['StartNode']
end_node = data['EndNode']
capacity = data['Capacity']
cost = data['Cost']
num_flow_reqs = data['NumFlowReqs']
source = data['Source']
destination = data['Destination']
data_rate = data['DataRate']

# Create the problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision variables
flow = {}
for i in range(num_links):
    for k in range(num_flow_reqs):
        flow[i, k] = pulp.LpVariable(f"f_{start_node[i]}_{end_node[i]}_{source[k]}_{destination[k]}", lowBound=0, cat=pulp.LpContinuous)

# Objective function
problem += pulp.lpSum(flow[i, k] * cost[i] for i in range(num_links) for k in range(num_flow_reqs))

# Constraints
# Flow Conservation Constraints
nodes = set(start_node + end_node)
for v in nodes:
    for k in range(num_flow_reqs):
        if v == source[k]:
            net_flow = data_rate[k]
        elif v == destination[k]:
            net_flow = -data_rate[k]
        else:
            net_flow = 0

        outflow = pulp.lpSum(flow[i, k] for i in range(num_links) if start_node[i] == v)
        inflow = pulp.lpSum(flow[i, k] for i in range(num_links) if end_node[i] == v)
        
        problem += (outflow - inflow == net_flow), f"Flow_Conservation_{v}_{source[k]}_{destination[k]}"

# Capacity Constraints
for i in range(num_links):
    problem += (pulp.lpSum(flow[i, k] for k in range(num_flow_reqs)) <= capacity[i]), f"Capacity_{start_node[i]}_{end_node[i]}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')