import pulp

# Data from JSON format
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
start_nodes = data['StartNode']
end_nodes = data['EndNode']
capacities = data['Capacity']
costs = data['Cost']
num_flow_reqs = data['NumFlowReqs']
sources = data['Source']
destinations = data['Destination']
data_rates = data['DataRate']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Transmission_Cost", pulp.LpMinimize)

# Decision variables
flow_vars = {}
for k in range(num_flow_reqs):
    for i in range(num_links):
        flow_vars[(k, i)] = pulp.LpVariable(f'f_{sources[k]}_{start_nodes[i]}_{end_nodes[i]}_{destinations[k]}', lowBound=0)

# Objective function
problem += pulp.lpSum(costs[i] * flow_vars[(k, i)] for k in range(num_flow_reqs) for i in range(num_links)), "Total_Cost"

# Flow Conservation Constraints
for k in range(num_flow_reqs):
    for node in set(start_nodes + end_nodes):
        if node == sources[k]:
            problem += (pulp.lpSum(flow_vars[(k, i)] for i in range(num_links) if start_nodes[i] == node) -
                         pulp.lpSum(flow_vars[(k, i)] for i in range(num_links) if end_nodes[i] == node) == data_rates[k], 
                         f"Flow_Conservation_Source_{k}_Node_{node}")
        elif node == destinations[k]:
            problem += (pulp.lpSum(flow_vars[(k, i)] for i in range(num_links) if start_nodes[i] == node) -
                         pulp.lpSum(flow_vars[(k, i)] for i in range(num_links) if end_nodes[i] == node) == -data_rates[k], 
                         f"Flow_Conservation_Destination_{k}_Node_{node}")
        else:
            problem += (pulp.lpSum(flow_vars[(k, i)] for i in range(num_links) if start_nodes[i] == node) -
                         pulp.lpSum(flow_vars[(k, i)] for i in range(num_links) if end_nodes[i] == node) == 0, 
                         f"Flow_Conservation_Intermediate_{k}_Node_{node}")

# Capacity Constraints
for i in range(num_links):
    problem += (pulp.lpSum(flow_vars[(k, i)] for k in range(num_flow_reqs)) <= capacities[i], 
                          f"Capacity_Constraint_Link_{i}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')