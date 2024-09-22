import pulp
import json

# Data provided in JSON format
data = json.loads("{'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}")

# Extracting sets and parameters from the data
NumLinks = data['NumLinks']
start_nodes = data['StartNode']
end_nodes = data['EndNode']
capacities = data['Capacity']
costs = data['Cost']
NumFlowReqs = data['NumFlowReqs']
sources = data['Source']
destinations = data['Destination']
data_rates = data['DataRate']

# Sets
A = [(start_nodes[i], end_nodes[i]) for i in range(NumLinks)]
D = [(sources[i], destinations[i]) for i in range(NumFlowReqs)]

# Create the linear programming problem
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("flow", A, lowBound=0)

# Objective Function
problem += pulp.lpSum(costs[i] * x[(start_nodes[i], end_nodes[i])] for i in range(NumLinks)), "Total_Cost"

# Capacity Constraints
for i in range(NumLinks):
    problem += x[(start_nodes[i], end_nodes[i])] <= capacities[i], f"Capacity_Constraint_{i+1}"

# Flow Conservation Constraints
for request in D:
    k, l = request
    problem += pulp.lpSum(x[(i, l)] for i in start_nodes if (i, l) in A) - pulp.lpSum(x[(l, j)] for j in end_nodes if (l, j) in A) == 0, f"Incoming_Flow_{k}_{l}"

    for m in set(start_nodes + end_nodes):
        if m != k and m != l:
            problem += pulp.lpSum(x[(i, m)] for i in start_nodes if (i, m) in A) - pulp.lpSum(x[(m, j)] for j in end_nodes if (m, j) in A) == 0, f"Flow_Conservation_{m}"

    problem += pulp.lpSum(x[(k, j)] for j in end_nodes if (k, j) in A) == data_rates[D.index(request)], f"Outgoing_Flow_{k}_{l}"

# Solve the problem
problem.solve()

# Output
optimized_paths = {f"Path_{i+1}": (sources[i], destinations[i], pulp.value(x[(sources[i], destinations[i])])) for i in range(NumFlowReqs)}
total_cost = pulp.value(problem.objective)

print(f'Optimized Paths: {optimized_paths}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')