import pulp
import json

# Load the data
data = json.loads("{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}")

# Extract parameters from the data
T = data['T']
demand = data['Demand']
oil_capacity = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100  # Convert percentage to a fraction
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Initialize the problem
problem = pulp.LpProblem("Capacity_Addition_Problem", pulp.LpMinimize)

# Define decision variables
coal_added = [pulp.LpVariable(f'coal_added_{t}', lowBound=0) for t in range(1, T + 1)]
nuke_added = [pulp.LpVariable(f'nuke_added_{t}', lowBound=0) for t in range(1, T + 1)]

# Objective function
problem += pulp.lpSum(coal_cost * coal_added[t] + nuke_cost * nuke_added[t] for t in range(T)), "Total_Cost"

# Constraints
# Total capacity constraint
for t in range(T):
    total_capacity = oil_capacity[t]
    for k in range(max(1, t + 1 - coal_life), t + 2):  # k is 1-indexed
        total_capacity += coal_added[k - 1]
    for k in range(max(1, t + 1 - nuke_life), t + 2):
        total_capacity += nuke_added[k - 1]
    problem += total_capacity >= demand[t], f"Total_Capacity_Constraint_{t + 1}"

# Nuclear capacity constraint
for t in range(T):
    total_capacity = oil_capacity[t]
    coal_total = sum(coal_added[k - 1] for k in range(max(1, t + 1 - coal_life), t + 2))
    nuke_total = sum(nuke_added[k - 1] for k in range(max(1, t + 1 - nuke_life), t + 2))
    problem += nuke_total / (total_capacity + coal_total + nuke_total) <= max_nuke, f"Nuclear_Capacity_Constraint_{t + 1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')