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

# Extract data from input
num_links = data['NumLinks']
start_node = data['StartNode']
end_node = data['EndNode']
capacity = data['Capacity']
cost = data['Cost']
num_flow_reqs = data['NumFlowReqs']
source = data['Source']
destination = data['Destination']
data_rate = data['DataRate']

# Set of arcs and flow requirements
A = range(num_links)
F = range(num_flow_reqs)

# Initialize the problem
problem = pulp.LpProblem("Network Flow Minimization", pulp.LpMinimize)

# Decision variable: flow on link (i,j) for flow requirement (k,l)
flow_vars = pulp.LpVariable.dicts(
    "flow",
    ((i, j, k, l) for i in A for j in F for k in F for l in F),
    lowBound=0,
    cat='Continuous'
)

# Objective function
problem += pulp.lpSum(cost[i] * flow_vars[i, j, k, l]
                      for i in A for j in F for k in F for l in F)

# Capacity constraints
for i in A:
    problem += pulp.lpSum(flow_vars[i, j, k, l] for j in F for k in F for l in F) <= capacity[i], f"Capacity_Constraint_{i}"

# Flow conservation constraints
for k in F:
    for l in F:
        for m in set(start_node + end_node):
            if m != source[k] and m != destination[k]:
                incoming = pulp.lpSum(flow_vars[i, m_index, k, l]
                                      for i, m_index in enumerate(end_node) if m_index == m)
                outgoing = pulp.lpSum(flow_vars[m_index, j, k, l]
                                      for j, m_index in enumerate(start_node) if m_index == m)
                problem += incoming - outgoing == 0, f"Flow_Conservation_{m}_{k}_{l}"

# Demand constraints
for k in F:
    problem += pulp.lpSum(flow_vars[i, j, k, l]
                          for i, j in enumerate(start_node) if i == source[k] - 1) - \
               pulp.lpSum(flow_vars[j, i, k, l]
                          for i, j in enumerate(end_node) if j == source[k] - 1) == data_rate[k], \
               f"Demand_Constraint_Source_{source[k]}_{k}"

    problem += pulp.lpSum(flow_vars[j, i, k, l]
                          for i, j in enumerate(end_node) if j == destination[k] - 1) - \
               pulp.lpSum(flow_vars[i, j, k, l]
                          for i, j in enumerate(start_node) if i == destination[k] - 1) == -data_rate[k], \
               f"Demand_Constraint_Destination_{destination[k]}_{k}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')