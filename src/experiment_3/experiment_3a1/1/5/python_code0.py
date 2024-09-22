import pulp
import json

# Data provided in JSON format
data = json.loads('{"NumLinks": 4, "StartNode": [1, 2, 2, 3], "EndNode": [2, 3, 4, 4], "Capacity": [50, 40, 60, 50], "Cost": [2, 3, 1, 1], "NumFlowReqs": 2, "Source": [1, 2], "Destination": [4, 3], "DataRate": [40, 30]}')

# Extracting data from the parsed JSON
num_links = data['NumLinks']
start_nodes = data['StartNode']
end_nodes = data['EndNode']
capacities = data['Capacity']
costs = data['Cost']
num_flow_reqs = data['NumFlowReqs']
sources = data['Source']
destinations = data['Destination']
data_rates = data['DataRate']

# Create the optimization problem
problem = pulp.LpProblem("Minimize_Communication_Cost", pulp.LpMinimize)

# Create decision variables
x = pulp.LpVariable.dicts("x", range(num_links), lowBound=0)

# Objective Function
problem += pulp.lpSum(costs[i] * x[i] for i in range(num_links)), "Total_Cost"

# Capacity Constraints
for i in range(num_links):
    problem += x[i] <= capacities[i], f"Capacity_Constraint_{i}"

# Flow Conservation Constraints
for k in range(num_flow_reqs):
    # For source nodes
    problem += pulp.lpSum(x[i] for i in range(num_links) if start_nodes[i] == sources[k]) - \
                       pulp.lpSum(x[i] for i in range(num_links) if end_nodes[i] == sources[k]) == data_rates[k], \
                       f"Flow_Conservation_Source_{sources[k]}"

    # For destination nodes
    problem += pulp.lpSum(x[i] for i in range(num_links) if end_nodes[i] == destinations[k]) - \
                       pulp.lpSum(x[i] for i in range(num_links) if start_nodes[i] == destinations[k]) == -data_rates[k], \
                       f"Flow_Conservation_Destination_{destinations[k]}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')