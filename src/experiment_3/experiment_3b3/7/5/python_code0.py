import pulp

# Data from JSON
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
links = [(data['StartNode'][i], data['EndNode'][i]) for i in range(data['NumLinks'])]
capacity = {links[i]: data['Capacity'][i] for i in range(data['NumLinks'])}
cost = {links[i]: data['Cost'][i] for i in range(data['NumLinks'])}
flow_reqs = data['NumFlowReqs']
source_nodes = data['Source']
destination_nodes = data['Destination']
data_rates = data['DataRate']

# Nodes set
nodes = set(data['StartNode'] + data['EndNode'])

# Problem initialization
problem = pulp.LpProblem("Communication_Network", pulp.LpMinimize)

# Decision Variables
flow = pulp.LpVariable.dicts("Flow", links, lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(cost[i, j] * flow[i, j] for i, j in links), "Total Cost"

# Constraints
# Capacity constraints
for i, j in links:
    problem += flow[i, j] <= capacity[i, j], f"Capacity_Constraint_{i}_{j}"
    
# Flow conservation constraints
for node in nodes:
    for k in range(flow_reqs):
        if node == source_nodes[k]:
            net_flow = data_rates[k]
        elif node == destination_nodes[k]:
            net_flow = -data_rates[k]
        else:
            net_flow = 0
           
        problem += (
            pulp.lpSum(flow[i, j] for i, j in links if i == node) -
            pulp.lpSum(flow[j, i] for j, i in links if i == node) == net_flow,
            f"Flow_Conservation_Node_{node}_Req_{k}"
        )

# Solve the problem
problem.solve()

# Print the outputs
print("Optimized path flows and costs:")
for i, j in links:
    print(f"Flow on link ({i} -> {j}): {flow[i, j].varValue} bits/second with cost: {cost[i, j] * flow[i, j].varValue}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')