import pulp
import json

# Data input
data = json.loads('{"T": 12, "Demand": [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], "OilCap": [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], "CoalCost": 10, "NukeCost": 5, "MaxNuke": 20, "CoalLife": 5, "NukeLife": 10}')
T = data['T']
demand = data['Demand']
oil_capacity = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100  # Convert to a fraction
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision variables
coal_vars = pulp.LpVariable.dicts("Coal", range(1, T + 1), lowBound=0)
nuke_vars = pulp.LpVariable.dicts("Nuke", range(1, T + 1), lowBound=0)

# Objective function
problem += pulp.lpSum(coal_cost * coal_vars[t] + nuke_cost * nuke_vars[t] for t in range(1, T + 1)), "Total_Cost"

# Constraints
for t in range(1, T + 1):
    capacity_constraint = (oil_capacity[t - 1] +
                          pulp.lpSum(coal_vars[j] for j in range(max(1, t - coal_life + 1), t + 1)) +
                          pulp.lpSum(nuke_vars[j] for j in range(max(1, t - nuke_life + 1), t + 1)))
    
    problem += (capacity_constraint >= demand[t - 1]), f"Capacity_Constraint_{t}"

for t in range(1, T + 1):
    total_capacity = pulp.lpSum(coal_vars[j] for j in range(1, T + 1)) + pulp.lpSum(nuke_vars[j] for j in range(1, T + 1)) + oil_capacity[t - 1]
    problem += (pulp.lpSum(nuke_vars[j] for j in range(1, T + 1)) <= max_nuke * total_capacity), f"Nuclear_Capacity_Limit_{t}"

# Solve the problem
problem.solve()

# Prepare the output
coal_cap_added = [pulp.value(coal_vars[t]) for t in range(1, T + 1)]
nuke_cap_added = [pulp.value(nuke_vars[t]) for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

# Print results
print(f'Coal Capacity Added: {coal_cap_added}')
print(f'Nuclear Capacity Added: {nuke_cap_added}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')