import pulp
import json

# Data input
data = json.loads("{'NumLinks': 4, 'StartNode': [1, 2, 2, 3], 'EndNode': [2, 3, 4, 4], 'Capacity': [50, 40, 60, 50], 'Cost': [2, 3, 1, 1], 'NumFlowReqs': 2, 'Source': [1, 2], 'Destination': [4, 3], 'DataRate': [40, 30]}")

# Parameters
n_links = data['NumLinks']
start_nodes = data['StartNode']
end_nodes = data['EndNode']
capacities = data['Capacity']
costs = data['Cost']
num_flow_reqs = data['NumFlowReqs']
sources = data['Source']
destinations = data['Destination']
data_rates = data['DataRate']

# Create a problem instance
problem = pulp.LpProblem("Communication_Network", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("flow", ((start_nodes[i], end_nodes[i]) for i in range(n_links)), lowBound=0)

# Objective function
problem += pulp.lpSum(costs[i] * x[(start_nodes[i], end_nodes[i])] for i in range(n_links)), "Total_Cost"

# Capacity constraints
for i in range(n_links):
    problem += x[(start_nodes[i], end_nodes[i])] <= capacities[i], f"CapConstraint_{i}"

# Flow conservation constraints for each source-destination pair
for flow_req in range(num_flow_reqs):
    source = sources[flow_req]
    destination = destinations[flow_req]
    problem += (pulp.lpSum(x[(source, j)] for j in end_nodes if (source, j) in x) -
                 pulp.lpSum(x[(i, source)] for i in start_nodes if (i, source) in x) == data_rates[flow_req]), f"FlowConservation_{flow_req}"

# Solve the problem
problem.solve()

# Output results
for i in range(n_links):
    if pulp.value(x[(start_nodes[i], end_nodes[i])]) > 0:
        print(f"Link ({start_nodes[i]}, {end_nodes[i]}): Flow = {pulp.value(x[(start_nodes[i], end_nodes[i])])}, Cost = {pulp.value(x[(start_nodes[i], end_nodes[i])]) * costs[i]}")

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')