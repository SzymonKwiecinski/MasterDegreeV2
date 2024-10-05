import pulp

# Data from the JSON input
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

# Number of links and flow requests
num_links = data['NumLinks']
num_flow_reqs = data['NumFlowReqs']

# Defining the problem
problem = pulp.LpProblem("NetworkFlowOptimization", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts(
    "flow",
    ((i, j, k, l) for i in range(num_links) for j in range(num_flow_reqs)
     for k in range(data['Source'][j], data['Destination'][j] + 1)
     for l in range(data['Source'][j], data['Destination'][j] + 1)),
    lowBound=0,
    cat='Continuous'
)

# Objective function: Minimize the total cost
problem += pulp.lpSum(
    data['Cost'][i] * x[i, j, data['StartNode'][i], data['EndNode'][i]]
    for i in range(num_links) for j in range(num_flow_reqs)
)

# Capacity constraints
for i in range(num_links):
    problem += pulp.lpSum(
        x[i, j, data['StartNode'][i], data['EndNode'][i]]
        for j in range(num_flow_reqs)
    ) <= data['Capacity'][i], f"Capacity_constraint_{i}"

# Flow conservation constraints
for i in range(num_links):
    for j in range(num_flow_reqs):
        for k in range(num_links):
            if data['StartNode'][k] == data['Source'][j]:
                problem += (
                    pulp.lpSum(x[k, j, data['StartNode'][k], m]
                               for m in range(data['NumLinks'])
                               if m == data['EndNode'][k]) -
                    pulp.lpSum(x[m, j, data['StartNode'][m], data['EndNode'][m]]
                               for m in range(num_links)
                               if m == data['StartNode'][k])
                    == data['DataRate'][j], f"Flow_src_constraint_{k}_{j}"
                )
            elif data['EndNode'][k] == data['Destination'][j]:
                problem += (
                    pulp.lpSum(x[m, j, data['StartNode'][m], data['EndNode'][m]]
                               for m in range(num_links)
                               if m == data['EndNode'][k]) -
                    pulp.lpSum(x[k, j, data['StartNode'][k], m]
                               for m in range(data['NumLinks'])
                               if m == data['StartNode'][k])
                    == -data['DataRate'][j], f"Flow_dest_constraint_{k}_{j}"
                )
            else:
                problem += (
                    pulp.lpSum(x[m, j, data['StartNode'][m], data['EndNode'][m]]
                               for m in range(num_links)
                               if m == data['EndNode'][k]) -
                    pulp.lpSum(x[k, j, data['StartNode'][k], m]
                               for m in range(data['NumLinks'])
                               if m == data['StartNode'][k])
                    == 0, f"Flow_mid_constraint_{k}_{j}"
                )

# Solve the problem
problem.solve()

# Print the status of the solution
print(f"Status: {pulp.LpStatus[problem.status]}")

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')