import pulp
import json

# Input data
data = {
    'T': 12,
    'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35],
    'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5],
    'CoalCost': 10,
    'NukeCost': 5,
    'MaxNuke': 20,
    'CoalLife': 5,
    'NukeLife': 10
}

# Extracting data from the input
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal_added = [pulp.LpVariable(f'coal_added_{t}', lowBound=0, cat='Continuous') for t in range(T)]
nuke_added = [pulp.LpVariable(f'nuke_added_{t}', lowBound=0, cat='Continuous') for t in range(T)]

# Objective Function: Minimize total cost
problem += pulp.lpSum(coal_cost * coal_added[t] for t in range(T)) + pulp.lpSum(nuke_cost * nuke_added[t] for t in range(T))

# Constraints
for t in range(T):
    total_capacity = oil_cap[t] + pulp.lpSum(coal_added[max(0, t - coal_life + 1):t + 1]) + pulp.lpSum(nuke_added[max(0, t - nuke_life + 1):t + 1])
    problem += total_capacity >= demand[t], f'demand_constraint_{t}'

# Nuclear capacity constraint
for t in range(T):
    total_coal_capacity = pulp.lpSum(coal_added[max(0, t - coal_life + 1):t + 1])
    total_nuke_capacity = pulp.lpSum(nuke_added[max(0, T - nuke_life + 1):t + 1])
    problem += total_nuke_capacity <= max_nuke * total_capacity, f'nuke_limit_constraint_{t}'

# Solve the problem
problem.solve()

# Prepare the output
coal_cap_added = [pulp.value(coal_added[t]) for t in range(T)]
nuke_cap_added = [pulp.value(nuke_added[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

# Output
output = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost,
}

# Printing the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')