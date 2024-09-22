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

# Parameters
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100  # Convert percentage to a fraction
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Problem
problem = pulp.LpProblem('Electricity_Capacity_Planning', pulp.LpMinimize)

# Decision variables
coal_cap_added = [pulp.LpVariable(f'CoalCapAdded_{t}', lowBound=0, cat='Continuous') for t in range(T)]
nuke_cap_added = [pulp.LpVariable(f'NukeCapAdded_{t}', lowBound=0, cat='Continuous') for t in range(T)]

# Objective
total_cost = pulp.lpSum(coal_cost * coal_cap_added[t] + nuke_cost * nuke_cap_added[t] for t in range(T))
problem += total_cost

# Constraints
for t in range(T):
    # Capacity constraints
    coal_capacity = pulp.lpSum(coal_cap_added[i] for i in range(max(0, t - coal_life + 1), t + 1))
    nuke_capacity = pulp.lpSum(nuke_cap_added[i] for i in range(max(0, t - nuke_life + 1), t + 1))
    total_capacity = oil_cap[t] + coal_capacity + nuke_capacity
    problem += total_capacity >= demand[t]

    # Nuclear capacity constraint
    problem += nuke_capacity <= max_nuke * total_capacity

# Solve the problem
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

# Display results
print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')