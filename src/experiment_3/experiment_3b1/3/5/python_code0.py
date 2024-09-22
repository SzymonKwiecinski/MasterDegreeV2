import pulp
import json

# Data in JSON format
data = json.loads('{"NumLinks": 4, "StartNode": [1, 2, 2, 3], "EndNode": [2, 3, 4, 4], "Capacity": [50, 40, 60, 50], "Cost": [2, 3, 1, 1], "NumFlowReqs": 2, "Source": [1, 2], "Destination": [4, 3], "DataRate": [40, 30]}')

# Extracting data
num_links = data['NumLinks']
start_node = data['StartNode']
end_node = data['EndNode']
capacity = data['Capacity']
cost = data['Cost']
num_flow_reqs = data['NumFlowReqs']
source = data['Source']
destination = data['Destination']
data_rate = data['DataRate']

# Create the linear programming problem
problem = pulp.LpProblem("Communication_Network_Optimization", pulp.LpMinimize)

# Decision Variables: x[i][j] for flow from node i to node j
x = pulp.LpVariable.dicts("flow", [(start_node[i], end_node[i]) for i in range(num_links)], lowBound=0)

# Objective Function: Minimize total cost
problem += pulp.lpSum(cost[i] * x[(start_node[i], end_node[i])] for i in range(num_links)), "Total_Cost"

# Constraints: Flow Conservation and Capacity constraints
for req in range(num_flow_reqs):
    k = source[req]
    l = destination[req]
    
    # Flow Conservation
    flow_out = pulp.lpSum(x[(k, j)] for j in end_node if (k, j) in x)
    flow_in = pulp.lpSum(x[(i, k)] for i in start_node if (i, k) in x)
    problem += flow_out - flow_in == data_rate[req], f"Flow_Conservation_{k}_{l}"

# Flow Capacity Constraints
for i in range(num_links):
    problem += x[(start_node[i], end_node[i])] <= capacity[i], f"Cap_Constraint_{start_node[i]}_{end_node[i]}"

# Solve the problem
problem.solve()

# Output the results
for v in problem.variables():
    print(f"{v.name}: {v.varValue}")

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')