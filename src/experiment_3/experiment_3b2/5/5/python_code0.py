import pulp
import json

# Data in JSON format
data = json.loads('{"NumLinks": 4, "StartNode": [1, 2, 2, 3], "EndNode": [2, 3, 4, 4], "Capacity": [50, 40, 60, 50], "Cost": [2, 3, 1, 1], "NumFlowReqs": 2, "Source": [1, 2], "Destination": [4, 3], "DataRate": [40, 30]}')

# Extract data
num_links = data['NumLinks']
start_nodes = data['StartNode']
end_nodes = data['EndNode']
capacities = data['Capacity']
costs = data['Cost']
num_flow_reqs = data['NumFlowReqs']
sources = data['Source']
destinations = data['Destination']
data_rates = data['DataRate']

# Sets and indices
nodes = list(set(sources + destinations))
links = [(start_nodes[i], end_nodes[i]) for i in range(num_links)]

# Create the problem
problem = pulp.LpProblem("Network_Flow_Optimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("flow", ((i, j, k, l) for (i, j) in links for k in sources for l in destinations), lowBound=0)

# Objective Function
problem += pulp.lpSum(costs[start_nodes.index(i)] * x[i, j, k, l] for (i, j) in links for k in sources for l in destinations), "Total_Transmission_Cost"

# Flow Conservation Constraints
for m in nodes:
    for k in sources:
        for l in destinations:
            if m == k:
                problem += pulp.lpSum(x[i, j, k, l] for (i, j) in links if i == m) - pulp.lpSum(x[i, j, k, l] for (i, j) in links if j == m) == data_rates[sources.index(k)], f"FlowConservation_Src_{k}_Dest_{l}_Node_{m}"
            elif m == l:
                problem += pulp.lpSum(x[i, j, k, l] for (i, j) in links if i == m) - pulp.lpSum(x[i, j, k, l] for (i, j) in links if j == m) == -data_rates[sources.index(k)], f"FlowConservation_Src_{k}_Dest_{l}_Node_{m}"
            else:
                problem += pulp.lpSum(x[i, j, k, l] for (i, j) in links if i == m) - pulp.lpSum(x[i, j, k, l] for (i, j) in links if j == m) == 0, f"FlowConservation_Src_{k}_Dest_{l}_Node_{m}"

# Capacity Constraints
for (i, j) in links:
    problem += pulp.lpSum(x[i, j, k, l] for k in sources for l in destinations) <= capacities[start_nodes.index(i)], f"Capacity_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')