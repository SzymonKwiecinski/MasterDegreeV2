import pulp

# Data
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

# Initialize problem
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100.0
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Decision Variables
coal_cap_added = [pulp.LpVariable(f"coal_cap_added_{t}", lowBound=0) for t in range(T)]
nuke_cap_added = [pulp.LpVariable(f"nuke_cap_added_{t}", lowBound=0) for t in range(T)]

# Objective Function
total_cost = pulp.lpSum(coal_cost * coal_cap_added[t] + nuke_cost * nuke_cap_added[t] for t in range(T))
problem += total_cost

# Constraints

# Demand constraints
for t in range(T):
    coal_capacity_active = pulp.lpSum(coal_cap_added[max(0, t-coal_life+1):t+1])
    nuke_capacity_active = pulp.lpSum(nuke_cap_added[max(0, t-nuke_life+1):t+1])
    problem += oil_cap[t] + coal_capacity_active + nuke_capacity_active >= demand[t]

# Nuclear capacity constraints
for t in range(T):
    nuke_capacity_active = pulp.lpSum(nuke_cap_added[max(0, t-nuke_life+1):t+1])
    coal_capacity_active = pulp.lpSum(coal_cap_added[max(0, t-coal_life+1):t+1])
    total_capacity_active = oil_cap[t] + coal_capacity_active + nuke_capacity_active
    problem += nuke_capacity_active <= max_nuke * total_capacity_active

# Solve problem
problem.solve()

# Extract results
coal_cap_added_result = [pulp.value(coal_cap_added[t]) for t in range(T)]
nuke_cap_added_result = [pulp.value(nuke_cap_added[t]) for t in range(T)]
total_cost_result = pulp.value(problem.objective)

# Output
output = {
    "coal_cap_added": coal_cap_added_result,
    "nuke_cap_added": nuke_cap_added_result,
    "total_cost": total_cost_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')